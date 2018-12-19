import math
import os
import sys
import datetime
import random
from model.Application import TestApp
import json
import ast
import pickle
import numpy as np
from model.Defintion import BAR_DICT
from time import sleep

DATETIME_FORMAT = "yyyy-MM-dd hh:mm"
DEFAULT_HISTORIC_DATA_ID = 33


# class DatabaseConnection():
#     def __init__(self):
#         pass
#         self.app = None
#         # self.query = QSqlQuery()
#         # self.app = None
#
#     def create_app(self):
#         self.app = TestApp("127.0.0.1", 7498, 10)
#
#     def init_database(self):
#         """
#         Function checks if all necessary tables exist. Missing tables are created
#         :return:
#         """
#         query = QSqlQuery()
#         query_status = query.exec_("DROP TABLE charts")
#
#         query_status = query.exec_("""CREATE TABLE charts (
#                         modified DATETIME NOT NULL,
#                         type VARCHAR(40) NOT NULL,
#                         symbol VARCHAR(40) NOT NULL,
#                         exchange VARCHAR(40) NOT NULL,
#                         expiration DATETIME NOT NULL,
#                         iv BLOB NOT NULL,
#                         historical BLOB NOT NULL)""") # historical JSON NOT NULL)
#         print("CREATE TABLE charts: {}".format(query_status))
#         query_status = query.exec_("""CREATE TABLE favorites (
#                                 added DATETIME NOT NULL,
#                                 type VARCHAR(40) NOT NULL,
#                                 symbol VARCHAR(40) NOT NULL,
#                                 exchange VARCHAR(40) NOT NULL)""")  # historical JSON NOT NULL)
#         print("CREATE TABLE favorites: {}".format(query_status))
#         query.prepare("INSERT INTO charts (modified, type, symbol, exchange, "
#                       "expiration, iv, historical) VALUES (?, ?, ?, ?, ?, ?, ?)")
#         now = QDateTime.currentDateTime()
#         modified = now.addYears(-20)
#         x = []
#         xb = pickle.dumps(x)
#         xbb = QByteArray(xb)
#         query.addBindValue(QVariant(modified))
#         query.addBindValue(QVariant("FUT"))
#         query.addBindValue(QVariant("CL"))
#         query.addBindValue(QVariant("NYMEX"))
#         query.addBindValue(QVariant(modified))
#         query.addBindValue(xbb)
#         query.addBindValue(xbb)
#         query_status = query.exec_()
#         print("INSERT INTO charts (BindValue): {}".format(query_status))
#         query.addBindValue(QVariant(modified))
#         query.addBindValue(QVariant(("STK")))
#         query.addBindValue(QVariant("SPY"))
#         query.addBindValue(QVariant("ARCA"))
#         query.addBindValue(QVariant(modified))
#         query.addBindValue(xbb)
#         query.addBindValue(xbb)
#         query_status = query.exec_()
#         print("INSERT INTO charts (BindValue): {}".format(query_status))
#         query.prepare("INSERT INTO favorites (added, type, symbol, exchange) VALUES (?, ?, ?, ?)")
#         query.addBindValue(QVariant((now)))
#         query.addBindValue(QVariant(("FUT")))
#         query.addBindValue(QVariant("CL"))
#         query.addBindValue(QVariant("NYMEX"))
#         query_status = query.exec_()
#         print("INSERT INTO favorites (BindValue): {}".format(query_status))
#
#     def update_data(self):
#         """
#         Function updates chart data in SQL database
#         :return: (bool). True for success, false for failure
#         """
#         query = QSqlQuery()
#         query2 = QSqlQuery()
#         query_success = query.exec("SELECT * FROM charts")
#         # Loop through all entries in CHARTS
#         if query_success:
#             # Entry for underlying was found
#             # Loop Through FAVORITES
#             while query.next():
#                 modified = query.value(0)
#                 modified = QDateTime().fromString(modified, Qt.ISODate)
#                 sec_type = query.value(1)
#                 symbol = query.value(2)
#                 exchange = query.value(3)
#                 expiration = query.value(4)
#                 iv = query.value(5)
#                 price = query.value(6)
#
#                 if iv is not None and iv is not "":
#                     iv = pickle.loads(iv)
#                 else:
#                     # No iv field is empty
#                     iv = []
#                 # historical_chart = query2.value(6)
#                 now = QDateTime.currentDateTime()
#                 if modified.date() == now.date():
#                     # Chart data is up to date > updated the same day > do nothing
#                     pass
#                 else:
#                     # Subtract number of days that need to be updated
#                     timespan_in_days = now.secsTo(modified) / (60 * 60 * 24)
#                     timespan_in_days = abs(math.ceil(timespan_in_days))
#                     timespan = (str(timespan_in_days) + " D")
#                     if timespan_in_days >= 365:
#                         timespan_in_years = now.secsTo(modified) / (60 * 60 * 24 * 365)
#                         timespan_in_years = abs(math.ceil(timespan_in_years))
#                         timespan = (str(timespan_in_years) + " Y")
#
#                     # Get missing iv data from server
#                     # Get new data from Server
#                     iv_new_list = self.app.get_hist_iv(sec_type, symbol, exchange, timespan)
#
#                     if iv_new_list is not None and iv is not None:
#                         # Join old with new iv
#                         for iv_new in iv_new_list:
#                             if iv_new not in iv:        # Make sure there are no duplicates
#                                 iv.append(iv_new)
#
#                         # Convert list to binary
#                         iv_bin = QByteArray(pickle.dumps(iv))
#
#                         query2.prepare("UPDATE charts SET iv=? WHERE symbol=? AND type=?")
#                         query2.addBindValue(iv_bin)
#                         query2.addBindValue(symbol)
#                         query2.addBindValue(sec_type)
#                         query_success = query2.exec_()
#
#                         # Update date
#                         now = now.toString()
#                         query2.prepare("UPDATE charts SET modified=? WHERE symbol=? AND type=?")
#                         query2.addBindValue(now)
#                         query2.addBindValue(QVariant(symbol))
#                         query2.addBindValue(QVariant(sec_type))
#                         query_success = query2.exec_()
#
#     def update_hist_date(self, ib_contract, bar_size="1 D"):
#         pass
#
#
#
#
#     def display_data(self):
#         query = QSqlQuery()
#         print("###########################################################################################")
#         print("display_data()")
#         print("###########################################################################################")
#         print("Display charts")
#         query_success = query.exec("SELECT * FROM charts")
#         # Loop through all entries in CHARTS
#         if query_success:
#             # Loop Through charts
#             while query.next():
#                 modified = query.value(0)
#                 modified = QDateTime().fromString(modified, Qt.ISODate)
#                 sec_type = query.value(1)
#                 symbol = query.value(2)
#                 exchange = query.value(3)
#                 expiration = query.value(4)
#                 iv = query.value(5)
#                 price = query.value(6)
#                 print("Entry: {} ### {} ### {} ### {} ### {}".format(modified, sec_type, symbol, exchange, expiration))
#                 if iv is not None and iv is not "":
#                     print("iv = {}".format(iv))
#                     print("type(iv) = {}".format(type(iv)))
#                     iv = pickle.loads(iv)
#                     print("pickle.loads(iv) = {}".format(iv))
#                 else:
#                     iv = []
#
#     def get_hist_data(self, symbol, time_interval):
#         """
#         Function returns dict with daily historical data for the specified underlying
#         :param underlying: (dict)
#         {'iv_daily', 'price_daily', 'volume_daily', 'iv_'}
#         :param time_interval:
#         :return:
#         """
#         if time_interval == 'D':
#             pass
#
#     # def get_hist_data(self):
#     #     """
#     #     Function sets initial data
#     #     :return:
#     #     """
#     #     if self.app is not None:
#     #         query1 = QSqlQuery()
#     #         query2 = QSqlQuery()
#     #         query3 = QSqlQuery()
#     #
#     #         # Get FAVORITES from MySQL Database > Loop through FAVORITES
#     #         query_success = query1.exec("SELECT added, type, symbol, exchange FROM favorites")
#     #
#     #         if query_success:
#     #             # Loop Through FAVORITES
#     #             while query1.next():
#     #                 added = query1.value(0)
#     #                 sec_type = query1.value(1)
#     #                 symbol = query1.value(2)
#     #                 exchange = query1.value(3)
#     #
#     #                 # Get existing data from CHARTS > Check how old data is > Update if necessary
#     #                 query_success = query2.exec(
#     #                     "SELECT * FROM charts WHERE symbol='{}' AND type='{}'".format(symbol, sec_type))
#     #                 if query_success:
#     #                     # Loop through CHARTS
#     #                     while query2.next():
#     #                         modified = query2.value(0)
#     #                         modified = QDateTime.fromString(modified)
#     #                         type_chart = query2.value(1)
#     #                         symbol_chart = query2.value(2)
#     #                         exchange_chart = query2.value(3)
#     #                         expiration_chart = query2.value(4)
#     #                         iv_chart = query2.value(5)
#     #                         if iv_chart is not None:
#     #                             iv_chart = json.loads(iv_chart)         # String to json
#     #                         else:
#     #                             # No iv field is empty
#     #                             iv_chart = []
#     #                         # historical_chart = query2.value(6)
#     #                         now = QDateTime.currentDateTime()
#     #                         if modified.date() == now.date():
#     #                             pass
#     #                             # Chart data was updated the same day > do nothing
#     #                             print("Historical iv already updated today")
#     #                         else:
#     #                             # Subtract number of days that need to be updated
#     #                             timespan_in_days = now.secsTo(modified)/(60*60*24)
#     #                             timespan_in_days_str = (str(timespan_in_days) + " D")
#     #                             print("timespan = {}".format(timespan_in_days_str))
#     #                             # Get missin iv data from server
#     #                             # Get new data from Server
#     #                             iv_new_list = self.app.get_hist_iv(sec_type, symbol, exchange, timespan_in_days_str)
#     #
#     #                             if iv_new_list is not None and iv_chart is not None:
#     #                                 iv_new_serialized = json.dumps(iv_new_list)
#     #
#     #                                 # Get old iv entry
#     #                                 query_success = query3.exec(
#     #                                     "UPDATE charts SET iv='{}' WHERE symbol='{}' AND type='{}'".
#     #                                     format(iv_new_serialized, symbol, sec_type))
#     #                                 # Append new iv entry to old
#     #
#     #                                 iv_chart.append(iv_new_serialized)
#     #
#     #
#     #                         # print("added = {}, type(added) = {}".format(added, type(added)))
#     #                         # added_list = json.loads(added)
#     #                         #
#     #                         # print("added_list = {}, type(added_list) = {}".format(added_list, type(added_list)))
#     #
#     #
#     #                 # query_success = query3.exec("UPDATE charts SET iv='{}'")
#     #
#     #                 print("query_success UPDATE Charts SET= {}".format(query_success))
#     #
#
#
#     def open(self):
#         """
#         Open a new database connection.
#         :return:
#         """
#         filename = os.path.join(os.path.dirname(__file__), "../data/data.db")
#         db = QSqlDatabase.addDatabase("QSQLITE")
#         db.setDatabaseName(filename)
#         open_success = db.open()
#         print("open_success = {}".format(open_success))
#         if not open_success:
#             QMessageBox.warning(None, "Phone Log",
#                                 QString("Database Error: %1").arg(db.lastError().text()))
#             sys.exit(1)


class Database:
    def __init__(self, tws):
        self.tws = tws
        self.data = self.load('HistData')
        # self.symbol_list = ['SPY', 'QQQ', 'IWM', 'VXX', 'GLD', 'SLV', 'USO', 'ES',
        #                     'TSLA', 'NFLX', 'EWZ', 'FXI', 'MSFT', 'TWTR', 'X', 'XLE', 'XOP', 'GLD', 'SLV']
        # self.sec_type_list = ['STK', 'STK', 'STK', 'STK', 'STK', 'STK', 'STK', 'CONTFUT',
        #                       'STK', 'STK', 'STK', 'STK', 'STK', 'STK', 'STK', 'STK', 'STK', 'STK', 'STK', ]
        # self.expiration_list = [' ', ' ', ' ', ' ', ' ', ' ', ' ', "201809",
        #                         ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ]
        self.symbol_list = ['SPY', 'QQQ', 'IWM', 'VXX', 'GLD', 'SLV', 'USO', 'ES',
                            'TSLA', 'NFLX', 'EWZ', 'MSFT', 'TWTR', 'X']
        self.sec_type_list = ['STK', 'STK', 'STK', 'STK', 'STK', 'STK', 'STK', 'CONTFUT',
                              'STK', 'STK', 'STK', 'STK', 'STK', 'STK', 'STK']
        self.expiration_list = [' ', ' ', ' ', ' ', ' ', ' ', ' ', '201809',
                                ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.duration_list = [20, 65, 125, 250, 2 * 250, 3 * 250, 4 * 250, 5 * 250, 10 * 250]

        self.watchlist_list = {'Test': ['SPY', 'QQQ', '/CL'],
                               'Market': ['SPY', 'QQQ', 'IWM', 'VXX', 'GLD', 'SLV', 'USO', 'ES',
                               'TSLA', 'NFLX', 'EWZ', 'MSFT', 'TWTR', 'X']}

    def create_contract(self, symbol, type, exchange=None, primary_exchange=None, currency=None, lastTradeDate=None):
        contract_details_list = self.tws.create_contract(symbol, secType=type, exchange=None,
                                                         primary_exchange=None, currency=None,
                                                         lastTradeDate=None)

        if isinstance(contract_details_list, list):
            contract_details_list = contract_details_list[0]
        return contract_details_list
        # else:
        #     return contraontract_details_list, list):
        #     return contract_details_list[0]
        # else:
        #     return contract_details_list

    def get_contract(self, contract):
        pass

    def get_contract_list(self, contract_list):
        pass

    def get_hist_data(self, contract, durationStr='10 D', barSizeSetting='1 day', show='TRADES'):
        """

        :param symbol: e.g. 'SPY'
        :param type: e.g. 'STK', 'FUT', 'OPT'
        :param durationStr: [S	Seconds, D	Day, W	Week, M	Month, Y	Year ]
        :param barSizeSetting: [1 secs, 5 secs, 10 secs, 15 secs, 30 secs, 1 min, 2 mins, 3 mins, 5 mins, 10 mins ,15 mins,
        20 mins, 30 mins, 1 hour, 2 hours, 3 hours, 4 hours, 8 hours, 1 day, 1 week, 1 month]
        :param show: [OPTION_IMPLIED_VOLATILITY, TRADES]
        :return:
        :return:
        """
        # k = 0
        # while k < 10:
        #     contract_details_list = self.tws.resolve_ib_contract(symbol, type)
        #     try:
        #         contract_details = contract_details_list[0]
        #         break
        #     except TypeError:
        #         sleep(2)
        #     k = k + 1
        # if k == 10:
        #     return -1
        #
        # contract = contract_details.contract

        id = str(contract.symbol) + str(contract.secType) + str(contract.exchange) + str(contract.primaryExchange) + show + barSizeSetting
        if id in self.data.keys():
            date_updated = self.data[id]['UpdateDate']
            hist_data_old = self.data[id]['Data']
            if date_updated.date() == datetime.datetime.today().date():
                hist_data = hist_data_old
            else:
                if hist_data_old.size > 0:
                    # date_last_str = hist_data_old[-1][BAR_DICT['Date']]
                    date_last_date = hist_data_old[-1][BAR_DICT['Date']]
                    date_now = datetime.datetime.now()
                    date_delta = date_now - date_last_date
                    date_delta_days = date_delta.days

                    if date_delta_days > 0:
                        hist_data_new = self.tws.get_IB_historical_data(contract,
                                                                        durationStr='{} D'.format(date_delta_days),
                                                                        barSizeSetting=barSizeSetting,
                                                                        show=show)
                        hist_data_new = Database.convert_hist_data(hist_data_new)
                        z = np.where(hist_data_old[:, 0] == date_last_date)[0][0] - 1

                        if z is not None and hist_data_new.size > 0:
                            hist_data_old = hist_data_old[:z]
                            hist_data = np.concatenate((hist_data_old, hist_data_new), axis=0)
                        else:
                            hist_data = hist_data_old
                    else:
                        hist_data = hist_data_old
                else:
                    hist_data = self.tws.get_IB_historical_data(contract, durationStr=durationStr,
                                                                barSizeSetting=barSizeSetting, show=show)
                    hist_data = Database.convert_hist_data(hist_data)
                    sleep(2)
                self.data[id]['Data'] = hist_data
                self.data[id]['UpdateDate'] = datetime.datetime.now()
                self.save(self.data, 'HistData')
        else:
            hist_data = self.tws.get_IB_historical_data(contract, durationStr=durationStr,
                                                        barSizeSetting=barSizeSetting, show=show)
            hist_data = Database.convert_hist_data(hist_data)
            sleep(5)
            if hist_data.size != 0:
                self.data[id] = {'Data': None, 'UpdateDate': None}
                self.data[id]['Data'] = hist_data
                self.data[id]['UpdateDate'] = datetime.datetime.now()
                self.save(self.data, 'HistData')
            else:
                return -1

        # self.data[id]['Data'] = hist_data
        # self.data[id]['UpdateDate'] = datetime.datetime.now()
        return hist_data

    # @staticmethod
    # def _convert_bar_size_setting(bar_size_string):
    #     """
    #     Converts bar size settings into minutes
    #     :param bar_size_string:
    #     :return:
    #     """
    #     num = bar_size_string.split[0]
    #     if 'days' in bar_size_string:
    #         return num * (60*24)

    @staticmethod
    def convert_hist_data(hist_data_numpy):
        hist_data_list = []
        for i in range(0, hist_data_numpy.shape[0]):
            hist_data_sample = []
            date = datetime.datetime.strptime(hist_data_numpy[i, BAR_DICT['Date']], '%Y%m%d')
            hist_data_sample.append(date)
            for j in range(1, hist_data_numpy.shape[1]):
                hist_data_sample.append(float(hist_data_numpy[i, j]))
            hist_data_list.append(hist_data_sample)
        hist_data_list = np.asarray(hist_data_list)
        return hist_data_list

    def set_tws(self, tws):
        self.tws = tws

    def get_watchlist_list(self):
        # watchlist_name_list = []
        # for watchlist_name, underlying_list in self.watchlist_list.items():
        #     watchlist_name_list.append(watchlist_name)

        return self.watchlist_list

    def get_iv_rank(self):
        if os.path.isfile('data/' + 'ivranks' + '.pkl'):
            with open('data/' + 'ivranks' + '.pkl', 'rb') as f:
                return pickle.load(f)
        else:
            rank_data = {}
            contract_list = []

            for i, _ in enumerate(self.symbol_list):
                symbol = self.symbol_list[i]
                sec_type = self.sec_type_list[i]
                contract = self.create_contract(symbol, sec_type)
                contract_list.append(contract)
            rank_data['Symbol'] = self.symbol_list
            rank_data['SecType'] = self.sec_type_list
            rank_data['Duration'] = self.duration_list
            rank_data['ContractDetailsList'] = contract_list
            self.set_iv_rank(rank_data)

            return rank_data

    @staticmethod
    def set_iv_rank(data):
        with open('data/' + 'ivranks' + '.pkl', 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

    @staticmethod
    def load(file_name):
        if os.path.isfile(os.path.abspath('./data/' + file_name + '.pkl')):
            with open('data/' + file_name + '.pkl', 'rb') as f:
                return pickle.load(f)
        else:
            return {}

    @staticmethod
    def save(data, file_name):
        with open('data/' + file_name + '.pkl', 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

# if __name__ == '__main__':
#     db = DatabaseConnection()
#     # db.create_app()
#     db.open()
#     db.display_data()
#
#     # query2 = QSqlQuery()
#     # query2.prepare("UPDATE charts SET iv=?")
#     # y = [1,2,3,4]
#     # x = json.dumps(y)
#     # query2.addBindValue(x)
#     # query_success = query2.exec_()
#     #
#     # query3 = QSqlQuery()
#     # query3.prepare("SELECT iv FROM charts")
#     # query_success = query3.exec_()
#     # if query_success:
#     #     while query3.next():
#     #         iv = query3.value(0)
#     #         iv = json.loads(iv)
#     #         print("iv = {}".format(iv))
#
#     # db.init_database()
#
#     # db.update_data()
#
#     # db.get_hist_data()
#     # query = QSqlQuery()
#     # query_status = query.exec_("DROP TABLE charts")
#     # print("DROP TABLE charts success = {}".format(query_status))
#     #
#     # # WRITE TO Databse
#     # liste = [["20161101", 0.3191sys.exit(app.exec_())8873, 0.35936711, 0.29531347, 0.35916074, 1], ["20161102", 0.32312561, 0.42418272, 0.3114261, 0.33288843,["20161116", 0.3547635, 0.36193878, 0.31787115, 0.33588871, 1]]]
#     # print("type(list) = {}, list = {}".format(type(liste), liste))
#     # serialized_list = json.dumps(liste)
#     # print("type(serialized_list = {}, seriailzed_list = {})".format(type(serialized_list), serialized_list))
#     # query_success = query.exec("UPDATE charts SET iv='{}'".format(serialized_list))
#     # print("query_success = {}".format(query_success))
#     #
#     # # READ FROM Database
#     # query_success = query.exec("SELECT iv FROM charts")
#     # print("SELECT iv FROM charts success = {}".format(query_success))
#     # if query_success:
#     #     while query.next():
#     #         added = query.value(0)
#     #         print("added = {}, type(added) = {}".format(added, type(added)))
#     #         added_list = json.loads(added)
#     #         print("added_list = {}, type(added_list) = {}".format(added_list, type(added_list)))