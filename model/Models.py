from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure

import numpy as np
from model.Defintion import BAR_DICT
from model.Application import TestApp
import datetime
from scipy.stats import pearsonr
from math import sqrt
from time import sleep


class IV:
    def __init__(self):
        pass

    @staticmethod
    def calc_rank(hist_iv, duration, bar_value='High'):
        # Resize hist_iv to duration
        hist_iv_new = hist_iv[-duration:]

        # Select bar value
        hist_iv_new = hist_iv_new[:, BAR_DICT[bar_value]]
        hist_iv_new = hist_iv_new.astype(float)

        max_iv = np.amax(hist_iv_new)
        min_iv = np.amin(hist_iv_new)

        last = hist_iv_new[-1]

        iv_rank = 100 * (last-min_iv) / (max_iv-min_iv)

        return iv_rank

    @staticmethod
    def calc_rank_chart(hist_iv, duration, bar_value='High'):
        ivr_chart = np.zeros((len(hist_iv) - duration + 1, 2), dtype=object)
        for i in range(0, len(hist_iv) - duration + 1):
            hist_iv_new = hist_iv[i:i+duration]
            ivr_chart[i, BAR_DICT['Date']] = hist_iv_new[-1, BAR_DICT['Date']]
            ivr_chart[i, 1] = (IV.calc_rank(hist_iv_new, duration=duration, bar_value=bar_value))

        return ivr_chart

    @staticmethod
    def calc_hist_vol2(data, duration, bar_value='High'):
        """
        Calculates realized variance (https://en.wikipedia.org/wiki/Realized_variance) and takes the square root
        to get realized volatility.
        Calculate Historical volatility as standard deviation of logarithmic returns.
        Calculation according to http://www.macroption.com/historical-volatility-excel/
        :param data:
        :param duration:
        :param bar_value:
        :return:
        """
        data = data[-duration:]

        # Select bar value
        price_list = data[:, BAR_DICT[bar_value]]

        # Calculate daily logarithmic returns (also called continuously compounded returns)
        log_return_list = []
        for i in range(0, len(price_list) - 1):
            p1 = float(price_list[i])
            p2 = float(price_list[i+1])
            log_return = np.log(p2/p1)
            log_return_list.append(log_return)
        # Calculate standard deviation
        hist_vol_daily = np.std(log_return_list)

        # Anualize
        hist_vol_yearly = hist_vol_daily*sqrt(252)

        return hist_vol_yearly

    @staticmethod
    def calc_hist_vol(data, duration, bar_value='High'):
        """
        Calculates historical volatility according to "Option Trading Pricing and Volatility Strategies and Tehcniques"
        by Euen Sinclaire
        :param data:
        :param duration:
        :param bar_value:
        :return:
        """
        data = data[-duration:]

        # Select bar value
        price_list = data[:, BAR_DICT[bar_value]]

        # Calculate daily logarithmic returns (also called continuously compounded returns)
        log_return_list = []
        for i in range(0, len(price_list) - 1):
            p1 = float(price_list[i])
            p2 = float(price_list[i+1])
            log_return = np.log(p2/p1)
            log_return_list.append(log_return)
        # Calculate standard deviation
        volatility_daily = np.sqrt(np.sum(np.asarray(log_return_list) ** 2))

        # Anualize
        hist_vol_yearly = volatility_daily*sqrt(252)

        return hist_vol_yearly


    @staticmethod
    def calc_hist_vol_chart2(data, duration=252, bar_value='High'):
        """
        Calculates realized variance (https://en.wikipedia.org/wiki/Realized_variance) and takes the square root
        to get realized volatility.
        Calculate Historical volatility as standard deviation of logarithmic returns.
        Calculation according to http://www.macroption.com/historical-volatility-excel/
        :param data:
        :param duration:
        :param bar_value:
        :return:
        """
        # Select bar value
        # price_list = data[:, [BAR_DICT['Date'], BAR_DICT[bar_value]]]

        # Calculate daily logarithmic returns (also called continuously compounded returns)
        log_return_list = []
        for i in range(0, len(data) - 1):
            p1 = float(data[i, BAR_DICT[bar_value]])
            p2 = float(data[i + 1, BAR_DICT[bar_value]])
            log_return = np.log(p2 / p1)
            log_return_list.append([data[i + 1, BAR_DICT['Date']], log_return])
        log_return_list = np.asarray(log_return_list, dtype=object)
        hist_vol_chart = np.zeros((len(log_return_list) - duration + 1, 6), dtype=object)
        for i in range(0, len(log_return_list) - duration + 1):
            # Calculate standard deviation
            hist_vol_daily = np.std(log_return_list[i: duration+i, 1])
            # Anualize
            hist_vol_yearly = hist_vol_daily * sqrt(252)
            hist_vol_chart[i, 0] = data[duration+i, BAR_DICT['Date']]
            hist_vol_chart[i, 1:5] = hist_vol_yearly

        return hist_vol_chart

    @staticmethod
    def calc_hist_vol_chart(data, duration=252, bar_value='High'):
        """
        Calculates historical volatility according to "Option Trading Pricing and Volatility Strategies and Tehcniques"
        by Euen Sinclaire
        :param data:
        :param duration:
        :param bar_value:
        :return:
        """
        # Select bar value
        # price_list = data[:, [BAR_DICT['Date'], BAR_DICT[bar_value]]]

        # Calculate daily logarithmic returns (also called continuously compounded returns)
        log_return_list = []
        for i in range(0, len(data) - 1):
            p1 = float(data[i, BAR_DICT[bar_value]])
            p2 = float(data[i + 1, BAR_DICT[bar_value]])
            log_return = np.log(p2 / p1)
            log_return_list.append([data[i + 1, BAR_DICT['Date']], log_return])
        log_return_list = np.asarray(log_return_list, dtype=object)
        hist_vol_chart = np.zeros((len(log_return_list) - duration + 1, 6), dtype=object)
        for i in range(0, len(log_return_list) - duration + 1):
            # Calculate standard deviation from population variance. Following formula is the same as:
            # hist_vol_daily = np.std(log_return_list[i: duration+i, 1])
            hist_vol_yearly = np.sqrt((1/(duration-1) * np.sum(np.asarray(log_return_list[i: duration+i, 1]) ** 2))) * sqrt(252)

            # Anualize
            hist_vol_chart[i, 0] = data[duration + i, BAR_DICT['Date']]
            hist_vol_chart[i, 1:5] = hist_vol_yearly
            # hist_vol_chart[i, 2] = hist_vol_yearly
            # hist_vol_chart[i, 3] = hist_vol_yearly
            # hist_vol_chart[i, 4] = hist_vol_yearly
            # hist_vol_chart[i, 5] = hist_vol_yearly

        return hist_vol_chart

class Utils:
    def __init__(self):
        pass

    @staticmethod
    def match_timeline(chart1, chart2):

        chart1_datetime_list = chart1[:, BAR_DICT['Date']]
        chart2_datetime_list = chart2[:, BAR_DICT['Date']]

        start_date_chart1 = chart1_datetime_list[0]
        start_date_chart2 = chart2_datetime_list[0]
        end_date_chart1 = chart1_datetime_list[-1]
        end_date_chart2 = chart2_datetime_list[-1]
        start_date = max([start_date_chart1, start_date_chart2])
        end_date = min([end_date_chart1, end_date_chart2])

        # i_s_1 = chart1_datetime_list.index(start_date)
        # i_e_1 = chart1_datetime_list.index(end_date)+1
        #
        # i_s_2 = chart2_datetime_list.index(start_date)
        # i_e_2 = chart2_datetime_list.index(end_date)+1

        try:
            i_s_1 = np.where(chart1_datetime_list == start_date)[0][0]
            i_e_1 = np.where(chart1_datetime_list == end_date)[0][0]+1
        except IndexError:
            pass
        i_s_2 = np.where(chart2_datetime_list == start_date)[0][0]
        i_e_2 = np.where(chart2_datetime_list == end_date)[0][0]+1

        chart1_out = chart1[i_s_1: i_e_1, :]
        chart2_out = chart2[i_s_2: i_e_2, :]

        i = 0
        while i < min([chart1_out.shape[0], chart2_out.shape[0]]):
            if chart1_out[i][BAR_DICT['Date']] != chart2_out[i][BAR_DICT['Date']]:
                # Delete smaller date
                date1 = chart1_out[i][BAR_DICT['Date']]
                date2 = chart2_out[i][BAR_DICT['Date']]

                if date1 > date2:
                    chart2_out = np.delete(chart2_out, i, axis=0)
                else:
                    chart1_out = np.delete(chart1_out, i, axis=0)
                i = i - 1
            i = i + 1

        assert chart1_out.shape[0] == chart2_out.shape[0]
        assert chart1_out.shape[1] == chart2_out.shape[1]

        return chart1_out, chart2_out

    @staticmethod
    def calc_correlation(data1, data2, method='pearson'):
        if method == 'pearson':
            correlation = pearsonr(data1, data2)
        else:
            raise Exception('spam', 'Invalid argument for method {}'.format(method))

        return correlation

    @staticmethod
    def numpy_to_list(chart_numpy):
        chart_list = chart_numpy.tolist()
        for i in range(0, chart_numpy.shape[0]):
            chart_list[i][BAR_DICT['Date']] = datetime.datetime.strptime(chart_numpy[i, BAR_DICT['Date']], '%Y%m%d')
            for j in range(0, chart_numpy.shape[1]):
                chart_list[i][j] = float(chart_numpy[i, j])
        return chart_list

    @staticmethod
    def numpy_to_datetime_list(chart_numpy):
        chart_datetime_list = []
        for i in range(0, chart_numpy.shape[0]):
            date = datetime.datetime.strptime(chart_numpy[i, BAR_DICT['Date']], '%Y%m%d')
            chart_datetime_list.append(date)
        return chart_datetime_list

if __name__ == '__main__':
    print("Hallo")

    # # ####################################################################################################
    # # # Test calc_rank()
    # # ####################################################################################################
    # app = TestApp("127.0.0.1", 7498, 3)
    #
    # contract_details_list = app.create_contract('SPY', 'STK')
    # contract_details = contract_details_list[0]
    # contract = contract_details.contract
    # hist_iv = iv_data = app.get_IB_historical_data(contract, durationStr="20 D", barSizeSetting="1 day",
    #                                              show="OPTION_IMPLIED_VOLATILITY")
    #
    # app.disconnect()
    #
    # hist_iv = hist_iv[0:-8]
    # hist_ivr = IV.calc_rank(hist_iv, 15, bar_value='High')
    # print('######################################################## Hist IV')
    # print(hist_iv[:, [BAR_DICT['Date'], BAR_DICT['High']]])
    # print('######################################################## Max/Min')
    # print('max: {}, min: {}'.format(max(hist_iv[:, BAR_DICT['High']]), min(hist_iv[:, BAR_DICT['High']])))
    # print('######################################################## IVR')
    # print(hist_ivr)



    # # ####################################################################################################
    # # # Test calc_rank_chart()
    # # ####################################################################################################
    # app = TestApp("127.0.0.1", 7498, 3)
    #
    # contract_details_list = app.create_contract('SPY', 'STK')
    # contract_details = contract_details_list[0]
    # contract = contract_details.contract
    # hist_iv = iv_data = app.get_IB_historical_data(contract, durationStr="20 D", barSizeSetting="1 day",
    #                                              show="OPTION_IMPLIED_VOLATILITY")
    #
    # app.disconnect()
    #
    # hist_iv = hist_iv[0:-8]
    # hist_ivr = IV.calc_rank_chart(hist_iv, 3, bar_value='High')
    # print('######################################################## Hist IV')
    # print(hist_iv[:, [BAR_DICT['Date'], BAR_DICT['High']]])
    # print('######################################################## Hist IVR')
    # print(hist_ivr)



    # # ####################################################################################################
    # # # Test match_timeline()
    # # ####################################################################################################
    # app = TestApp("127.0.0.1", 7498, 3)
    #
    # contract_details_list = app.create_contract('SPY', 'STK')
    # contract_details = contract_details_list[0]
    # contract = contract_details.contract
    # chart1 = app.get_IB_historical_data(contract, durationStr="10 D", barSizeSetting="1 day",
    #                                              show="OPTION_IMPLIED_VOLATILITY")
    # chart2 = app.get_IB_historical_data(contract, durationStr="10 D", barSizeSetting="1 day",
    #                                              show="OPTION_IMPLIED_VOLATILITY")
    #
    # # Chart 1: ########
    # # Chart 2: ##########
    # chart1_out, chart2_out = Utils.match_timeline(chart1[:-2], chart2)
    #
    # # Chart 1:   ########
    # # Chart 2: ##########
    # chart1_out, chart2_out = Utils.match_timeline(chart1[2:], chart2)
    #
    # # Chart 1:  ########
    # # Chart 2: ##########
    # chart1_out, chart2_out = Utils.match_timeline(chart1[1:-2], chart2)
    #
    # # Chart 1: ##########
    # # Chart 2: ########
    # chart1_out, chart2_out = Utils.match_timeline(chart1[:-2], chart2)
    #
    # # Chart 1: ##########
    # # Chart 2:  ########
    # chart1_out, chart2_out = Utils.match_timeline(chart1[1:-2], chart2)
    #
    # # Chart 1: ##########
    # # Chart 2:   ########
    # chart1_out, chart2_out = Utils.match_timeline(chart1[2:], chart2)
    #
    # print(chart1)
    # print(chart2)
    # print(chart1_out)
    # print(chart2_out)






    # # ####################################################################################################
    # # # Test if calc_rank_chart() and calc_rank() are the same
    # # ####################################################################################################
    # app = TestApp("127.0.0.1", 7498, 3)
    #
    # contract_details_list = app.create_contract('SPY', 'STK')
    # contract_details = contract_details_list[0]
    # contract = contract_details.contract
    # hist_iv = iv_data = app.get_IB_historical_data(contract, durationStr="20 D", barSizeSetting="1 day",
    #                                              show="OPTION_IMPLIED_VOLATILITY")
    #
    # app.disconnect()
    #
    # hist_ivr = IV.calc_rank(hist_iv, 3, bar_value='High')
    # print('######################################################## Hist IV')
    # print(hist_iv[:, [BAR_DICT['Date'], BAR_DICT['High']]])
    # print('######################################################## Max/Min')
    # print('max: {}, min: {}'.format(max(hist_iv[:, BAR_DICT['High']]), min(hist_iv[:, BAR_DICT['High']])))
    # print('######################################################## IVR')
    # print(hist_ivr)
    #
    #
    # # hist_iv = iv_data = app.get_IB_historical_data(contract, durationStr="20 D", barSizeSetting="1 day",
    # #                                              show="OPTION_IMPLIED_VOLATILITY")
    #
    #
    # hist_ivr_chart = IV.calc_rank_chart(hist_iv, 3, bar_value='High')
    # print('######################################################## Hist IV')
    # print(hist_iv[:, [BAR_DICT['Date'], BAR_DICT['High']]])
    # print('######################################################## Hist IVR')
    # print(hist_ivr)
    # print('##########################################')
    # print(hist_ivr_chart)

    # # ####################################################################################################
    # # # Test calc_hist_vol()
    # # ####################################################################################################
    app = TestApp("127.0.0.1", 7498, 5)

    contract_details_list = app.create_contract('TSLA', 'STK')
    contract_details = contract_details_list[0]
    contract = contract_details.contract
    hist_price = app.get_IB_historical_data(contract, durationStr="2 Y", barSizeSetting="1 day",
                                            show="Trades")
    sleep(3)
    hist_vol_ib = app.get_IB_historical_data(contract, durationStr="300 D", barSizeSetting="1 day",
                                          show="HISTORICAL_VOLATILITY")
    app.disconnect()

    hist_vol = IV.calc_hist_vol(hist_price, duration=252, bar_value='Close')
    hist_vol_chart1 = IV.calc_hist_vol_chart(hist_price, duration=252, bar_value='Close')
    hist_vol_chart2 = IV.calc_hist_vol_chart2(hist_price, duration=252, bar_value='Close')

    print('Hist price \n################################')
    print(hist_price)
    print('Hist vol CALC\n################################')
    print(hist_vol)
    print('Hist vol IB\n################################')
    print(hist_vol_ib[-1])
    print('Hist vol chart CALC 1\n################################')
    print(hist_vol_chart1[-10:, :])
    print('Hist vol chart CALC 2\n################################')
    print(hist_vol_chart2[-10:, :])
    print('Hist vol chart IB\n################################')
    print(hist_vol_ib[-10:, :])
