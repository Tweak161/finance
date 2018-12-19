# Gist example of IB wrapper ...
#
# Download API from http://interactivebrokers.github.io/#
#
# Install python API code /IBJts/source/pythonclient $ python3 setup.py install
#
# Note: The test cases, and the documentation refer to a python package called IBApi,
#    but the actual package is called ibapi. Go figure.
#
# Get the latest version of the gateway:
# https://www.interactivebrokers.com/en/?f=%2Fen%2Fcontrol%2Fsystemstandalone-ibGateway.php%3Fos%3Dunix
#    (for unix: windows and mac users please find your own version)
#
# Run the gateway
#
# user: edemo
# pwd: demo123
#

from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.contract import Contract as IBcontract
from threading import Thread
import queue
import datetime
import numpy as np
from time import sleep

from model.Plot import plot_candlestick


DEFAULT_HISTORIC_DATA_ID=47
IV_HISTORIC_DATA_ID = 46
DEFAULT_GET_CONTRACT_ID=43

## marker for when queue is finished
FINISHED = object()
STARTED = object()
TIME_OUT = object()

class finishableQueue(object):

    def __init__(self, queue_to_finish):

        self._queue = queue_to_finish
        self.status = STARTED

    def get(self, timeout):
        """
        Returns a list of queue elements once timeout is finished, or a FINISHED flag is received in the queue
        :param timeout: how long to wait before giving up
        :return: list of queue elements
        """
        contents_of_queue=[]
        finished=False

        while not finished:
            try:
                current_element = self._queue.get(timeout=timeout)
                if current_element is FINISHED:
                    finished = True
                    self.status = FINISHED
                else:
                    contents_of_queue.append(current_element)
                    ## keep going and try and get more data

            except queue.Empty:
                ## If we hit a time out it's most probable we're not getting a finished element any time soon
                ## give up and return what we have
                finished = True
                self.status = TIME_OUT


        return contents_of_queue

    def timed_out(self):
        return self.status is TIME_OUT





class TestWrapper(EWrapper):
    """
    The wrapper deals with the action coming back from the IB gateway or TWS instance
    We override methods in EWrapper that will get called when this action happens, like currentTime
    Extra methods are added as we need to store the results in this object
    """

    def __init__(self):
        self._my_contract_details = {}
        self._my_historic_data_dict = {}
        self._my_position_dict = {}
        self._my_searched_contracts_dict = {}
        self._my_errors = queue.Queue()

    ## error handling code
    def init_error(self):
        error_queue = queue.Queue()
        self._my_errors = error_queue

    def get_error(self, timeout=5):
        if self.is_error():
            try:
                return self._my_errors.get(timeout=timeout)
            except queue.Empty:
                return None

        return None

    def is_error(self):
        an_error_if=not self._my_errors.empty()
        return an_error_if

    def error(self, id, errorCode, errorString):
        ## Overriden method
        errormsg = "IB error id %d errorcode %d string %s" % (id, errorCode, errorString)
        self._my_errors.put(errormsg)


    ## get contract details code
    def init_contractdetails(self, reqId):
        contract_details_queue = self._my_contract_details[reqId] = queue.Queue()

        return contract_details_queue

    def contractDetails(self, reqId, contractDetails):
        ## overridden method

        if reqId not in self._my_contract_details.keys():
            self.init_contractdetails(reqId)

        self._my_contract_details[reqId].put(contractDetails)

    def contractDetailsEnd(self, reqId):
        ## overriden method
        if reqId not in self._my_contract_details.keys():
            self.init_contractdetails(reqId)

        self._my_contract_details[reqId].put(FINISHED)

    ## Historic data code
    def init_historicprices(self, tickerid):
        historic_data_queue = self._my_historic_data_dict[tickerid] = queue.Queue()

        return historic_data_queue


    def historicalData(self, tickerid , bar):

        ## Overriden method
        ## Note I'm choosing to ignore barCount, WAP and hasGaps but you could use them if you like
        bardata=[bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume]

        historic_data_dict=self._my_historic_data_dict

        ## Add on to the current data
        if tickerid not in historic_data_dict.keys():
            self.init_historicprices(tickerid)

        historic_data_dict[tickerid].put(bardata)

    def historicalDataEnd(self, tickerid, start:str, end:str):
        ## overriden method

        if tickerid not in self._my_historic_data_dict.keys():
            self.init_historicprices(tickerid)

        self._my_historic_data_dict[tickerid].put(FINISHED)

    # Request Positions Code
    def init_position(self):
        pos_data_queue = self._my_position_dict[IV_HISTORIC_DATA_ID] = queue.Queue()

        return pos_data_queue

    def position(self, account, contract, position, avgCost):
        super().position(account, contract, position, avgCost)

        pos_data = {'Contract': contract,
                    'Position': position,
                    'AvgCost': avgCost}

        position_dict=self._my_position_dict

        ## Add on to the current data
        if IV_HISTORIC_DATA_ID not in position_dict.keys():
            self.init_position(IV_HISTORIC_DATA_ID)

        position_dict[IV_HISTORIC_DATA_ID].put(pos_data)

    def positionEnd(self):
        super().positionEnd()
        print("PositionEnd")

    # Search string
    def init_search(self):
        searched_contracts_queue = self._my_searched_contracts_dict[DEFAULT_HISTORIC_DATA_ID] = queue.Queue()
        return searched_contracts_queue

    def symbolSamples(self, reqId, contractDescriptions):
        super().symbolSamples(reqId, contractDescriptions)
        print("Symbol Samples. Request Id: ", reqId)

        for contractDescription in contractDescriptions:
            derivSecTypes = ""
            for derivSecType in contractDescription.derivativeSecTypes:
                derivSecTypes += derivSecType
                derivSecTypes += " "
            print("Contract: conId:%s, symbol:%s, secType:%s primExchange:%s, " "currency:%s, derivativeSecTypes:%s" % (
                contractDescription.contract.conId,
                contractDescription.contract.symbol,
                contractDescription.contract.secType,
                contractDescription.contract.primaryExchange,
                contractDescription.contract.currency, derivSecTypes))
        searched_contracts_data_dict=self._my_searched_contracts_dict

        ## Add on to the current data
        if reqId not in searched_contracts_data_dict.keys():
            self.init_search(DEFAULT_HISTORIC_DATA_ID)

        searched_contracts_data_dict[reqId].put(contractDescriptions)

class TestClient(EClient):
    """
    The client method
    We don't override native methods, but instead call them from our own wrappers
    """
    def __init__(self, wrapper):
        ## Set up with a wrapper inside
        EClient.__init__(self, wrapper)

    def resolve_ib_contract(self, ibcontract, reqId=DEFAULT_GET_CONTRACT_ID):
        """
        From a partially formed contract, returns a fully fledged version
        :returns fully resolved IB contract
        """

        ## Make a place to store the data we're going to return
        contract_details_queue = finishableQueue(self.init_contractdetails(reqId))

        print("Getting full contract details from the server... ")

        self.reqContractDetails(reqId, ibcontract)

        ## Run until we get a valid contract(s) or get bored waiting
        MAX_WAIT_SECONDS = 4.2
        new_contract_details = contract_details_queue.get(timeout=MAX_WAIT_SECONDS)

        while self.wrapper.is_error():
            print(self.get_error())

        if contract_details_queue.timed_out():
            print("Exceeded maximum wait for wrapper to confirm finished - seems to be normal behaviour")

        if len(new_contract_details)==0:
            print("Failed to get additional contract details: returning unresolved contract")
            return ibcontract

        if len(new_contract_details)>1:
            print("got multiple contracts using first one")
            print("new_contract_details[0] = {}".format(new_contract_details[0]))
            print("new_contract_details = {}".format(new_contract_details))

        # new_contract_details=new_contract_details[0]

        # resolved_ibcontract=new_contract_details.contract

        return new_contract_details


    # def create_contract(self, sec_type, symbol, exchange, last_trade_data=None):
    #     """
    #     Creates contract with given parameters
    #     :param sec_type:
    #     :param symbol:
    #     :param exchange:
    #     :param last_trade_data:
    #     :return: (IBcontract)
    #     """
    #     ibcontract = IBcontract()
    #     ibcontract.secType = sec_type
    #     ibcontract.symbol = symbol
    #     ibcontract.exchange = exchange
    #     if last_trade_data:
    #         ibcontract.lastTradeDateOrContractMonth = last_trade_data
    #
    #     resolved_ibcontract = app.resolve_ib_contract(ibcontract)
    #
    #     return resolved_ibcontract

    def get_IB_historical_data(self, ibcontract, durationStr="1 Y", barSizeSetting="1 day",
                               tickerid=DEFAULT_HISTORIC_DATA_ID, show="Trades"):
        """
        https://interactivebrokers.github.io/tws-api/historical_bars.html#hd_what_to_show

        :param ibcontract:
        :param durationStr: {'x S', 'x D', 'x W', 'x M', 'x Y'}
        :param barSizeSetting:
        :param tickerid: {HISTORICAL_VOLATILITY, OPTION_IMPLIED_VOLATILITY}
        :param show:
        :return: [Type	Open	High	Low	Close	Volume]
        """

        ## Make a place to store the data we're going to return
        historic_data_queue = finishableQueue(self.init_historicprices(tickerid))

        # Request some historical data. Native method in EClient
        self.reqHistoricalData(
            tickerid,  # tickerId,
            ibcontract,  # contract,
            datetime.datetime.today().strftime("%Y%m%d %H:%M:%S %Z"),  # endDateTime,
            durationStr,  # durationStr,
            barSizeSetting,  # barSizeSetting,
            show,  # whatToShow,
            1,  # useRTH,
            1,  # formatDate
            False,  # KeepUpToDate <<==== added for api 9.73.2
            [] ## chartoptions not used
        )

        ## Wait until we get a completed data, an error, or get bored waiting
        MAX_WAIT_SECONDS = 10.2
        print("Getting historical data from the server... could take %d seconds to complete " % MAX_WAIT_SECONDS)

        historic_data = historic_data_queue.get(timeout = MAX_WAIT_SECONDS)

        while self.wrapper.is_error():
            print(self.get_error())

        if historic_data_queue.timed_out():
            print("Exceeded maximum wait for wrapper to confirm finished - seems to be normal behaviour")

        self.cancelHistoricalData(tickerid)

        historic_data = np.asarray(historic_data)

        return historic_data

    def get_IB_portfolio_info(self, tickerid=DEFAULT_HISTORIC_DATA_ID):

        ## Make a place to store the data we're going to return
        # historic_data_queue = finishableQueue(self.init_historicprices(tickerid))
        req_pos_queue = finishableQueue(self.init_position())

        # Request some position details. Native method in EClient
        self.reqPositions()

        ## Wait until we get a completed data, an error, or get bored waiting
        MAX_WAIT_SECONDS = 0.2
        print("Getting position info from the server... could take %d seconds to complete " % MAX_WAIT_SECONDS)

        pos_data = req_pos_queue.get(timeout = MAX_WAIT_SECONDS)

        while self.wrapper.is_error():
            print(self.get_error())

        if req_pos_queue.timed_out():
            print("Exceeded maximum wait for wrapper to confirm finished - seems to be normal behaviour")

        self.cancelPositions()

        return pos_data

    def search_IB_contract(self, search_string):
        """
        Search IB for contracts matching the search string. The search string can e.g. be the ticker symbol. All
        contracts (options, futures, ...) matching the search string are returned.
        :param search_string:
        :return:
        """
        ## Make a place to store the data we're going to return
        # historic_data_queue = finishableQueue(self.init_historicprices(tickerid))
        queue = finishableQueue(self.init_search())

        # Request some position details. Native method in EClient
        self.reqMatchingSymbols(DEFAULT_HISTORIC_DATA_ID, search_string)

        ## Wait until we get a completed data, an error, or get bored waiting
        MAX_WAIT_SECONDS = 0.2
        print("Getting position info from the server... could take %d seconds to complete " % MAX_WAIT_SECONDS)

        data = queue.get(timeout = MAX_WAIT_SECONDS)

        while self.wrapper.is_error():
            print(self.get_error())

        if queue.timed_out():
            print("Exceeded maximum wait for wrapper to confirm finished - seems to be normal behaviour")

        return data

    def get_IB_option_chain(self, symbol, exchange, sec_type, contract_id):
        """
        Search IB for contracts matching the search string. The search string can e.g. be the ticker symbol. All
        contracts (options, futures, ...) matching the search string are returned.
        :param search_string:
        :return:
        """
        ## Make a place to store the data we're going to return
        # historic_data_queue = finishableQueue(self.init_historicprices(tickerid))
        queue = finishableQueue(self.init_search())

        # Request some position details. Native method in EClient
        self.reqSecDefOptParams(DEFAULT_HISTORIC_DATA_ID, symbol, exchange, sec_type, contract_id)

        ## Wait until we get a completed data, an error, or get bored waiting
        MAX_WAIT_SECONDS = 10
        print("Getting position info from the server... could take %d seconds to complete " % MAX_WAIT_SECONDS)

        data = queue.get(timeout=MAX_WAIT_SECONDS)

        while self.wrapper.is_error():
            print(self.get_error())

        if queue.timed_out():
            print("Exceeded maximum wait for wrapper to confirm finished - seems to be normal behaviour")

        return data


class TestApp(TestWrapper, TestClient):
    def __init__(self, ipaddress, portid, clientid):
        TestWrapper.__init__(self)
        TestClient.__init__(self, wrapper=self)

        self.connect(ipaddress, portid, clientid)
        sleep(3)
        thread = Thread(target = self.run)
        thread.start()

        setattr(self, "_thread", thread)

        self.init_error()

    def is_connected(self):
        return True

    def get_hist_data(self, contract, duration="1 Y", show="OPTION_IMPLIED_VOLATILITY"):
        """
        Returns historical option implied volatitlity
        Example: get_hist_iv('STK', 'SPY', 'NYSE', '10')
        :return: (iv)
        """
        data = self.get_IB_historical_data(contract, duration, "1 day",
                                         IV_HISTORIC_DATA_ID, show=show)
        return data

    def create_contract(self, symbol, secType=None, exchange=None, primary_exchange=None, currency=None, lastTradeDate=None):
        """
        Returns List with Contract. If multiple contracts are possible, a list with all contracts is returned
        :param secType:
        :param lastTradeDate:
        :param symbol:
        :param exchange:
        :return:
        """
        ibcontract = IBcontract()
        ibcontract.symbol = symbol
        if secType is not None:
            ibcontract.secType = secType
        if currency is not None:
            ibcontract.currency = currency
        if exchange is not None:
            ibcontract.exchange = exchange
        if primary_exchange is not None:
            ibcontract.primaryExchange = primary_exchange
        if lastTradeDate is not None:
            ibcontract.lastTradeDateOrContractMonth = lastTradeDate
        resolved_contract = self.resolve_ib_contract(ibcontract)

        return resolved_contract

    def get_option_chain(self, symbol, exchange, sec_type, contract_id):
        data = self.get_IB_option_chain(symbol, exchange, sec_type, contract_id)
        return data


if __name__ == '__main__':
    pass
    # # ####################################################################################################
    # # # Get historical data
    # # ####################################################################################################
    # app = TestApp("127.0.0.1", 7498, 4)
    #
    # contract_details_list = app.create_contract('SPY', 'STK')
    # contract_details = contract_details_list[0]
    # contract = contract_details.contract
    #
    # historic_data = app.get_IB_historical_data(contract)
    #
    # np.save('./../data/temp.npy', historic_data)
    # historic_data = np.load('./../data/temp.npy')
    #
    # plot_candlestick(historic_data)
    #
    # print(historic_data)
    #
    # app.disconnect()



    # # ####################################################################################################
    # # # Historical IV
    # # ####################################################################################################
    # app = TestApp("127.0.0.1", 7498, 5)
    #
    # contract_details_list = app.create_contract('SPY', 'STK')
    # contract_details = contract_details_list[0]
    # contract = contract_details.contract
    # data = iv_data = app.get_IB_historical_data(contract, durationStr="2 Y", barSizeSetting="1 day",
    #                                              show="HISTORICAL_VOLATILITY")
    #
    # print('######################################################## Hist IV')
    # print(data.shape)
    # app.disconnect()


    # ####################################################################################################
    # # Historical IV of continous Futures
    # ####################################################################################################
    app = TestApp("127.0.0.1", 7498, 3)

    contract1 = IBcontract()
    contract1.symbol = "ES"
    contract1.secType = "CONTFUT"
    contract1.exchange = "GLOBEX"

    data = iv_data = app.get_IB_historical_data(contract1, durationStr="3 Y", barSizeSetting="1 day",
                                                show="Trades")
    print(data.shape)

    print('++++++++++++++')
    contract_details_list = app.create_contract('SPY', 'STK')
    contract_details = contract_details_list[0]
    contract = contract_details.contract

    data = iv_data = app.get_IB_historical_data(contract, durationStr="3 Y", barSizeSetting="1 day",
                                                show="Trades")

    print('######################################################## IV')
    print(data.shape)

    app.disconnect()


    # # ####################################################################################################
    # # # Get portfolio data
    # # ####################################################################################################
    # app = TestApp("127.0.0.1", 7498, 7)
    # data = app.get_IB_portfolio_info()
    #
    # print('######################################################## pose data')
    # print(data)
    # app.disconnect()



    # # ####################################################################################################
    # # # Search IB contract
    # # ####################################################################################################
    # app = TestApp("127.0.0.1", 7498, 7)
    # data = app.search_IB_contract('QQQ')
    #
    # print('######################################################## pose data')
    # print(data)
    # app.disconnect()



    # # # ####################################################################################################
    # # # # Request Option Chain
    # # # ####################################################################################################
    # app = TestApp("127.0.0.1", 7498, 6)
    #
    # contract_id = 0
    # data = app.get_option_chain('SPY', '', 'STK', contract_id)
    # print('######################################################## IV')
    # print(data.shape)
    #
    # app.disconnect()


