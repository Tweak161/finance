# PyQt
import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QLabel, QGridLayout, QWidget, QVBoxLayout, QMessageBox, QComboBox, QLineEdit, QCheckBox

from PyQt5.QtCore import QSize, pyqtSignal

# Views
from view import MainWindow

# Model
from model.Application import TestApp
from model.Database import Database
from model.Defintion import BAR_DICT, dur_2_str

# Plots
from model.Plot import PricePlot, RankPlot, PriceNavPlot
from model.Models import IV
from model.Models import Utils
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar

# API Modules
from ibapi.contract import Contract as IBcontract

# Standard Modules
import numpy as np
from time import sleep
import inspect


__version__ = "1.0"


DEFAULT_HISTORIC_DATA_ID=50


class MainWindowClass(QMainWindow, MainWindow.Ui_MainWindow):

    def __init__(self):
        super(MainWindowClass, self).__init__()
        self.setupUi(self)
        self.tws = None
        self.status_message = QLabel()
        self.statusbar.addPermanentWidget(self.status_message)

        self.db = Database(self.tws)

        self.tab2 = None
        self.tab3 = None
        self.tab4 = None

        # Connect to TWS
        connection_established = self.connect()
        if not connection_established:
            QMessageBox.Warning('Couldn\'t connect to TWS API')


        # #############################################################################################################
        # Signals
        # #############################################################################################################
        # QAction
        # self.connect(self.connectPB, SIGNAL("triggered()"), self.connect)

        # QButton
        # self.connect(self.connectPB, SIGNAL("clicked()"), self.connect)

        self.init_gui()
        self.guisave(self.ui, QtCore.QSettings('saved.ini', QtCore.QSettings.IniFormat))
        self.guirestore(self.ui, QtCore.QSettings('saved.ini', QtCore.QSettings.IniFormat))


        # QTableWidget
        # self.connect(self.appliedFilterTableWidget, SIGNAL("itemSelectionChanged()"),
        #              self.filter_selection_cb)

        # QComboBox
        # self.connect(self.chooseAlgoComboBox, SIGNAL("currentIndexChanged(int)"), self.set_algo)

    # #################################################################################################################
    # Init
    # #################################################################################################################
    def init_gui(self):
        # #################################################################################################################
        # Tabs
        # #################################################################################################################
        self.tab2 = Tab2(self)
        self.tab3 = Tab3(self, self.db)
        # self.tab4 = Tab4(self, self.db)

        # #################################################################################################################
        # QButton
        # #################################################################################################################
        self.connectPB.clicked.connect(self.connect)


        self.statusbar.showMessage(' was clicked')
        self.set_status_bar('Not connected', 'red')

    def closeEvent(self, evnt):
        super(QMainWindow, self).closeEvent(evnt)

        reply = QMessageBox.question(self, 'Message', "Are you sure to quit?", QMessageBox.Yes,
                                           QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.tws.disconnect()
            evnt.accept()
        else:
            evnt.ignore()

    # #################################################################################################################
    # Callbacks
    # #################################################################################################################
    # QAction

    # QButton
    def connect(self):
        if self.tws is None:
            self.tws = TestApp("127.0.0.1", 7498, 4)
            if self.tws.is_connected():
                self.connectionLL.setStyleSheet("QLabel { background-color : green}")
                self.set_status_bar('Connected to 127.0.0.1', 'green')
                self.db.set_tws(self.tws)
                return True
            else:
                self.connectionLL.setStyleSheet("QLabel { background-color : red}")
                self.set_status_bar('Not connected', 'red')
                return False
        else:
            if self.tws.is_connected():
                self.connectionLL.setStyleSheet("QLabel { background-color : green}")
                self.db.set_tws(self.tws)

            else:
                self.connectionLL.setStyleSheet("QLabel { background-color : red}")


    # #################################################################################################################
    # Utilities
    # #################################################################################################################
    def set_status_bar(self, text, color):
        self.status_message.setStyleSheet("background-color:{};".format(color))
        self.status_message.setText(text)

    def plot_heatmap(self):
        """
        Plot Heatmap
        :return:
        """
        contract = self.tws.create_contract("FUT", "201809", "GE", "GLOBEX")
        self.tws.get_IB_historical_data()

    def guisave(self, ui, settings):

        # for child in ui.children():  # works like getmembers, but because it traverses the hierarachy, you would have to call guisave recursively to traverse down the tree

        for name, obj in inspect.getmembers(ui):
            # if type(obj) is QComboBox:  # this works similar to isinstance, but missed some field... not sure why?
            if isinstance(obj, QComboBox):
                name = obj.objectName()  # get combobox name
                index = obj.currentIndex()  # get current index from combobox
                text = obj.itemText(index)  # get the text for current index
                settings.setValue(name, text)  # save combobox selection to registry

            if isinstance(obj, QLineEdit):
                name = obj.objectName()
                value = obj.text()
                settings.setValue(name, value)  # save ui values, so they can be restored next time

            if isinstance(obj, QCheckBox):
                name = obj.objectName()
                state = obj.checkState()
                settings.setValue(name, state)

    # ===================================================================
    # restore "ui" controls with values stored in registry "settings"
    # currently only handles comboboxes, editlines &checkboxes
    # ui = QMainWindow object
    # settings = QSettings object
    # ===================================================================

    def guirestore(self, ui, settings):

        for name, obj in inspect.getmembers(ui):
            if isinstance(obj, QComboBox):
                index = obj.currentIndex()  # get current region from combobox
                # text   = obj.itemText(index)   # get the text for new selected index
                name = obj.objectName()

                value = str(settings.value(name), 'utf-8')

                if value == "":
                    continue

                index = obj.findText(value)  # get the corresponding index for specified string in combobox

                if index == -1:  # add to list if not found
                    obj.insertItems(0, [value])
                    index = obj.findText(value)
                    obj.setCurrentIndex(index)
                else:
                    obj.setCurrentIndex(index)  # preselect a combobox value by index

            if isinstance(obj, QLineEdit):
                name = obj.objectName()
                value = str(settings.value(name), 'utf-8')  # get stored value from registry
                obj.setText(value)  # restore lineEditFile

            if isinstance(obj, QCheckBox):
                name = obj.objectName()
                value = settings.value(name)  # get stored value from registry
                if value != None:
                    obj.setCheckState(value)  # restore checkbox


            # if isinstance(obj, QRadioButton):


class Tab2(QWidget):
    def __init__(self, mw):
        super(QWidget, self).__init__()
        self.mw = mw

        self.price_plot = PriceNavPlot(self.mw.plotLabel1)

        # #################################################################################################################
        # QButton
        # #################################################################################################################
        self.mw.pltPricePB.clicked.connect(self.plt_price)
        self.mw.searchContractPB.clicked.connect(self.search_contract)

        # #################################################################################################################
        # Line Edits
        # #################################################################################################################
        self.type = ''
        self.symbol = ''
        self.exchange = ''
        self.search_string = ''
        self.mw.secTypeLE.textChanged.connect(self.sync_secTypeLE)
        self.mw.symbolLE.textChanged.connect(self.sync_symbolLE)
        self.mw.exchangeLE.textChanged.connect(self.sync_exchangeLE)
        self.mw.searchContractLE.textChanged.connect(self.sync_searchContractLE)

    # #################################################################################################################
    # Line Edit Callbacks
    # #################################################################################################################
    def sync_secTypeLE(self, text):
        self.type = text

    def sync_symbolLE(self, text):
        self.symbol = text

    def sync_exchangeLE(self, text):
        self.exchange = text

    def sync_searchContractLE(self, text):
        self.search_string = text
    # #################################################################################################################
    # Button Callbacks
    # #################################################################################################################
    def plt_price(self):
        print(self.type)
        contract_details_list = self.mw.tws.create_contract(self.symbol, 'STK', exchange=self.exchange)
        contract_details = contract_details_list[0]
        contract = contract_details.contract

        data = self.mw.db.get_hist_data(contract, durationStr="1 Y", barSizeSetting="1 day", show="OPTION_IMPLIED_VOLATILITY")
        if len(data) != 0:
            self.price_plot.plot_candlestick(data)

    def search_contract(self):
        self.mw.searchContractTE.clear()
        contract_description_list = self.mw.tws.search_IB_contract(self.search_string)[0]
        for contract_description in contract_description_list:
            contract = contract_description.contract
            string = ('ConID: ' + str(contract.conId) +
            ' Symbol: ' + str(contract.symbol) +
            ' SecType: ' + str(contract.secType) +
            ' PrimExchange: ' + str(contract.primaryExchange) +
            ' Currency: ' + str(contract.currency))

            string += ' DerivativesSecType: '
            for sec_type in contract_description.derivativeSecTypes:
                string += sec_type + ' '
            self.mw.searchContractTE.append(string)
            self.mw.searchContractTE.append('')


class Tab3(QWidget):
    def __init__(self, mw, db):
        super(QWidget, self).__init__()
        self.mw = mw
        self.db = db

        # l1 = QVBoxLayout(self.mw.plotLabel31)
        # self.iv_rank_plot = RankPlot(self.mw.plotLabel31)
        # l1.addWidget(self.iv_rank_plot)
        #
        # l2 = QVBoxLayout(self.mw.plotLabel32)
        # self.iv_rv_diff_plot = RankPlot(self.mw.plotLabel32)
        # l2.addWidget(self.iv_rv_diff_plot)

        self.iv_rank_plot = RankPlot(self.mw.plotLabel31, show_bar='False')

        self.iv_rv_diff_plot = RankPlot(self.mw.plotLabel32, show_bar='False')

        self.iv_rank_chart_plot = PriceNavPlot(self.mw.plotLabel33)

        self.iv_chart_plot = PriceNavPlot(self.mw.plotLabel34)

        self.is_checked_ivr = True
        self.mw.plot33IvrCB.setCheckState(2)
        self.is_checked_rvr = True
        self.mw.plot33RvrCB.setCheckState(2)
        self.is_checked_iv_rv_spread = False
        self.mw.plot3IvRvSpreadCB.setCheckState(0)
        self.is_checked_iv_rv_spread_rank = True
        self.mw.plot33IvRvSpreadRankCB.setCheckState(2)

        self.sel_symbol_row_index = None
        self.sel_duration_col_index = None
        self.iv_rv_rank_diff_array = None
        self.iv_rank_array = None
        self.rv_rank_array = None

        rank_data = self.db.get_iv_rank()

        self.symbol_list = rank_data['Symbol']
        self.sec_type_list = rank_data['SecType']
        self.duration_list = [20, 65, 125, 250, 2 * 250, 3 * 250, 4 * 250, 5 * 250, 10 * 250]
        self.contract_list = rank_data['ContractDetailsList']
        self.watchlist_list = self.db.get_watchlist_list()

        self.init_gui()
        self.plot()

        # #################################################################################################################
        # Variables
        # #################################################################################################################

        # #################################################################################################################
        # QButton
        # #################################################################################################################
        self.mw.add3PB.clicked.connect(self.add)
        self.mw.remove3PB.clicked.connect(self.remove)

        # #################################################################################################################
        # Line Edits
        # #################################################################################################################
        self.symbol = ''
        self.mw.symbol3LE.textChanged.connect(self.sync_symbolLE)

        # #################################################################################################################
        # Checkbox
        # #################################################################################################################
        self.mw.plot33IvrCB.clicked.connect(self.check_ivr)
        self.mw.plot33RvrCB.clicked.connect(self.check_rvr)
        self.mw.plot3IvRvSpreadCB.clicked.connect(self.check_iv_rv_spread)
        self.mw.plot33IvRvSpreadRankCB.clicked.connect(self.check_iv_rv_spread_rank)

        # #################################################################################################################
        # Combobox
        # #################################################################################################################
        # self.mw.

        # #################################################################################################################
        # Signals
        # #################################################################################################################
        self.iv_rank_plot.cell_select.connect(self.ivr_cell_select_callback)

    # #################################################################################################################
    # Button Callbacks
    # #################################################################################################################
    def add(self):
        iv_data = self.db.get_iv_rank()
        symbol_list = iv_data['Symbol']
        if self.symbol is not '':
            pass
            # contract_details_list = self.mw.tws.create_contract(self.symbol, 'STK')
            # if isinstance(contract_details_list, list):
            #     symbol_list.append(self.symbol)
            #     iv_data['Symbol'] = symbol_list
            #     self.db.set_iv_rank(iv_data)
            self.plot()
            # if isinstance(contract_details_list, list):
            #     pass
            # else:
            #     QMessageBox.warning(self.mw, "Invalid Ticker Symbol", "Please enter a valid Ticker Symbol."
            #                                                           " {} doesn't exist".format(self.symbol))
        else:
            QMessageBox.warning(self.mw, "Symbol doesn't exist")

    def remove(self):
        pass
        # iv_data = self.db.get_iv_rank()
        # symbol_list = iv_data['Symbol']
        # index_del_symbol = self.iv_rank_plot.get_clicked_symbol()
        # if index_del_symbol != -1:
        #     del symbol_list[index_del_symbol]
        #     self.db.set_iv_rank(iv_data)
        #     self.plot()
        # else:
        #     QMessageBox.warning(self.mw, "No Selection", "Please select the symbol you want to delete by clicking on it")

    # #################################################################################################################
    # Line Edit Callbacks
    # #################################################################################################################
    def sync_symbolLE(self, text):
        self.symbol = text

    # #################################################################################################################
    # Signal Callbacks
    # #################################################################################################################
    def ivr_cell_select_callback(self, symbol_row, duration_col):
        self.sel_symbol_row_index = symbol_row
        self.sel_duration_col_index = duration_col
        self.plot_iv(symbol_row, duration_col)
        self.iv_rv_diff_plot.highlight_selection(symbol_row, duration_col)
        self.iv_rank_plot.highlight_selection(symbol_row, duration_col)

    # #################################################################################################################
    # Checkbox Callbacks
    # #################################################################################################################
    def check_ivr(self, state):
        self.is_checked_ivr = state
        if self.sel_duration_col_index is not None and self.sel_duration_col_index is not None:
            self.plot_iv(self.sel_duration_col_index, self.sel_symbol_row_index)

    def check_rvr(self, state):
        self.is_checked_rvr = state
        if self.sel_duration_col_index is not None and self.sel_duration_col_index is not None:
            self.plot_iv(self.sel_duration_col_index, self.sel_symbol_row_index)

    def check_iv_rv_spread(self, state):
        self.is_checked_iv_rv_spread = state
        if self.sel_duration_col_index is not None and self.sel_duration_col_index is not None:
            self.plot_iv(self.sel_duration_col_index, self.sel_symbol_row_index)

    def check_iv_rv_spread_rank(self, state):
        self.is_checked_iv_rv_spread_rank = state
        if self.sel_duration_col_index is not None and self.sel_duration_col_index is not None:
            self.plot_iv(self.sel_duration_col_index, self.sel_symbol_row_index)

    # #################################################################################################################
    # Combobox Callbacks
    # #################################################################################################################
    def watchlist(self):
        pass

    # #################################################################################################################
    # Functions
    # #################################################################################################################
    def init_gui(self):
        pass
        watchlist_list = self.db.get_watchlist_list()
        self.mw.watchlist3CB.addItems(watchlist_list)
        # sel_watchlist = self.db.get_sel_watchlist

    def plot(self):
        # rank_data = self.db.get_iv_rank()
        self.watchlist_list = self.db.get_watchlist_list()
        self.wachlist_sel = self.mw.watchlist3CB.getValue()
        # self.symbol_list = rank_data['Symbol']
        self.symbol_list = watchlist
        # self.contract_list = rank_data['ContractDetailsList']
        self.contract_list = self.db.get_contract_list(watchlist)

        self.iv_rank_array = np.zeros((len(self.contract_list), len(self.duration_list)))
        self.rv_rank_array = np.zeros((len(self.contract_list), len(self.duration_list)))
        self.iv_rv_rank_diff_array = np.zeros((len(self.contract_list), len(self.duration_list)))

        symbol_list = []
        for i, contract_details in enumerate(self.contract_list):
            contract = contract_details.contract
            symbol = contract.symbol
            symbol_list.append(symbol)
            iv_data = self.db.get_hist_data(contract, durationStr="22 Y", barSizeSetting="1 day",
                                            show="OPTION_IMPLIED_VOLATILITY")
            price_data = self.db.get_hist_data(contract, durationStr="22 Y", barSizeSetting="1 day",
                                               show="Trades")

            for j, duration in enumerate(self.duration_list):
                rv_data = IV.calc_hist_vol_chart(price_data, duration=252, bar_value='Close')
                if isinstance(rv_data, int) or isinstance(iv_data, int):
                    break

                duration = int(duration)
                iv_rank = IV.calc_rank(iv_data, duration, bar_value='Low')
                iv_chart, rv_chart = Utils.match_timeline(iv_data, rv_data)
                # iv_rv_diff = iv_chart[:, 1:] - rv_chart[:, 1:]
                # iv_rv_rank = IV.calc_rank(iv_rv_diff, duration, 'High')

                iv_rv_diff_chart = np.copy(iv_chart)
                iv_rv_diff_chart[:, 1:] = iv_chart[:, 1:] - rv_chart[:, 1:]
                iv_rv_diff_rank_chart = IV.calc_rank(iv_rv_diff_chart, duration, bar_value='Low')

                self.iv_rv_rank_diff_array[i, j] = iv_rv_diff_rank_chart
                self.iv_rank_array[i, j] = iv_rank
                # self.rv_rank_array[i, j] = rv_rank

        duration_list_str = dur_2_str(self.duration_list)
        self.iv_rank_plot.plot(self.iv_rank_array, duration_list_str, symbol_list, 'IV Rank')
        self.iv_rv_diff_plot.plot(self.iv_rv_rank_diff_array, duration_list_str, symbol_list, 'IVR-RVR Diff')

    def plot_iv(self, contract_row, duration_col):
        contract_details = self.contract_list[contract_row]
        contract = contract_details.contract
        symbol = contract.symbol
        duration = self.duration_list[duration_col]
        duration_string = dur_2_str(duration)[0]

        iv_data = self.db.get_hist_data(contract, durationStr="22 Y", barSizeSetting="1 day",
                                        show="OPTION_IMPLIED_VOLATILITY")
        price_data = self.db.get_hist_data(contract, durationStr="22 Y", barSizeSetting="1 day",
                                           show="Trades")
        rv_data = IV.calc_hist_vol_chart(price_data, duration=duration, bar_value='Close')

        ivr_chart = IV.calc_rank_chart(iv_data, duration, bar_value='Low')
        rvr_chart = IV.calc_rank_chart(rv_data, duration, bar_value='Low')

        iv_rank = IV.calc_rank(iv_data, duration, 'Low')
        rv_rank = IV.calc_rank(rv_data, duration, 'Low')

        iv_chart, rv_chart = Utils.match_timeline(iv_data, rv_data)
        # ivr_chart, rvr_chart = Utils.match_timeline(ivr_chart, rvr_chart)

        # ivr_rvr_diff_chart = np.empty((ivr_chart.shape[0], ivr_chart.shape[1]),
        #                               dtype=([('datetime64[s]', 'datetime64[s]'),
        #                                       ('data', 'float')]))
        iv_rv_spread_chart = np.copy(iv_chart)
        iv_rv_spread_chart[:, 1:] = iv_chart[:, 1:] - rv_chart[:, 1:]

        iv_rv_spread_rank_chart = IV.calc_rank_chart(iv_rv_spread_chart, duration, bar_value='Low')

        self.iv_rank_chart_plot.clear()
        xlim = min(duration, ivr_chart.shape[0])
        self.iv_rank_chart_plot.set_xlim(ivr_chart[-xlim, BAR_DICT['Date']], ivr_chart[-1, BAR_DICT['Date']])
        if self.is_checked_ivr:
            self.iv_rank_chart_plot.plot_line(ivr_chart, 'IV Rank', 'Symbol: {}, Duration: {}'.format(symbol, duration_string))
        if self.is_checked_rvr:
            self.iv_rank_chart_plot.plot_line(rvr_chart, 'RV Rank', 'Symbol: {}, Duration: {}'.format(symbol, duration_string))
        if self.is_checked_iv_rv_spread_rank:
            self.iv_rank_chart_plot.plot_line(iv_rv_spread_rank_chart, 'IV/RV Spread Rank', 'Symbol: {}, Duration: {}'.format(symbol, duration_string))
        if self.is_checked_iv_rv_spread:
            self.iv_rank_chart_plot.plot_line(iv_rv_spread_chart[:, [BAR_DICT['Date'], BAR_DICT['High']]], 'IV/RV Spread', 'Symbol: {}, Duration: {}'.format(symbol, duration_string))

        self.iv_chart_plot.clear()
        xlim = min(duration, iv_data.shape[0])
        self.iv_chart_plot.set_xlim(iv_data[-xlim, BAR_DICT['Date']], iv_data[-1, BAR_DICT['Date']])
        self.iv_chart_plot.plot_candlestick(iv_data, 'RV Rank', 'Symbol: {}, Duration: {}'.format(symbol, duration_string))


# class Tab4(QWidget):
#     def __init__(self, mw, db):
#         super(QWidget, self).__init__()
#         self.mw = mw
#         self.db = db
#
#         # l2 = QVBoxLayout(self.mw.plotLabel41)
#         # self.plot1 = RankPlot(self.mw.plotLabel32)
#         # l2.addWidget(self.plot1)
#
#         self.plot1 = RankPlot(self.mw.plotLabel32)
#
#         # self.plot1 = RankPlot(self.mw.plotLabel41)
#         self.plot2 = RankPlot(self.mw.plotLabel42)
#         self.plot3 = PriceNavPlot(self.mw.plotLabel43)
#         self.plot4 = RankPlot(self.mw.plotLabel44)
#
#         self.spread_list = [['SPY', 'QQQ'], ['SPY', 'IWM'], ['GLD', 'SLV']]
#         self.duration_list = [30, 60, 125, 250, 2 * 250, 3 * 250, 4 * 250, 5 * 250, 10 * 250]
#
#         self.sel_spread_row_index = None
#         self.sel_duration_col_index = None
#
#         self.plot_1()
#
#         # #################################################################################################################
#         # Variables
#         # #################################################################################################################
#
#         # #################################################################################################################
#         # QButton
#         # #################################################################################################################
#
#         # #################################################################################################################
#         # Line Edits
#         # #################################################################################################################
#
#         # #################################################################################################################
#         # Checkbox
#         # #################################################################################################################
#
#         # #################################################################################################################
#         # Signals
#         # #################################################################################################################
#         self.plot1.cell_select.connect(self.plot1_callback)
#
#     # #################################################################################################################
#     # Button Callbacks
#     # #################################################################################################################
#
#     # #################################################################################################################
#     # Line Edit Callbacks
#     # #################################################################################################################
#
#     # #################################################################################################################
#     # Signal Callbacks
#     # #################################################################################################################
#     def plot1_callback(self, spread_row, duration_col):
#         self.sel_spread_row_index = spread_row
#         self.sel_duration_col_index = duration_col
#         self.plot1.highlight_selection(spread_row, duration_col)
#         self.plot_3(spread_row, duration_col)
#
#     # #################################################################################################################
#     # Checkbox Callbacks
#     # #################################################################################################################
#
#     # #################################################################################################################
#     # Functions
#     # #################################################################################################################
#     def plot_1(self):
#         spread_rank_array = np.zeros((len(self.spread_list), len(self.duration_list)))
#         for i, spread in enumerate(self.spread_list):
#
#             contract1_details = self.db.create_contract(spread[0], 'STK')
#             contract2_details = self.db.create_contract(spread[1], 'STK')
#             contract1 = contract1_details.contract
#             contract2 = contract2_details.contract
#
#             hist_data1 = self.db.get_hist_data(contract1, durationStr="12 Y", barSizeSetting="1 day",
#                                             show="Trades")
#             hist_data2 = self.db.get_hist_data(contract2, durationStr="12 Y", barSizeSetting="1 day",
#                                               show="Trades")
#
#             for j, duration in enumerate(self.duration_list):
#                 if isinstance(hist_data1, int):
#                     break
#                 hist_data1, hist_data2 = Utils.match_timeline(hist_data1, hist_data2)
#                 duration = int(duration)
#                 spread_chart = np.copy(hist_data1)
#                 spread_chart[:, 1:] = hist_data1[:, 1:] - hist_data2[:, 1:]
#                 spread_rank = IV.calc_rank(spread_chart, duration, bar_value='Low')
#                 spread_rank_array[i, j] = spread_rank
#
#         spread_string_list = []
#         for spread in self.spread_list:
#             spread_string = "/".join(spread)
#             spread_string_list.append(spread_string)
#         self.plot1.plot(spread_rank_array, self.duration_list, spread_string_list, 'IV Rank')
#
#     def plot_3(self, spread_row, duration_col):
#         self.plot3.clear()
#         spread = self.spread_list[spread_row]
#         duration = self.duration_list[duration_col]
#         duration_string = dur_2_str(duration)[0]
#         hist_data1 = self.db.get_hist_data(spread[0], 'STK', durationStr="22 Y", barSizeSetting="1 day",
#                                            show="Trades")
#         hist_data2 = self.db.get_hist_data(spread[1], 'STK', durationStr="22 Y", barSizeSetting="1 day",
#                                            show="Trades")
#         hist_data1, hist_data2 = Utils.match_timeline(hist_data1, hist_data2)
#         duration = int(duration)
#         spread_bp_chart = np.copy(hist_data1)
#         spread_bp_chart[:, 1:] = hist_data1[:, 1:] - hist_data2[:, 1:]
#         spread_percent_chart = np.copy(spread_bp_chart)
#         spread_percent_chart[:, 1:] = 100*(spread_percent_chart[:, 1:] / hist_data1[:, 1:])
#         spread_rank_chart = IV.calc_rank_chart(spread_bp_chart, duration, bar_value='Low')
#         # xlim = min(duration, iv_data.shape[0])
#         # self.iv_chart_plot.set_xlim(iv_data[-xlim, BAR_DICT['Date']], iv_data[-1, BAR_DICT['Date']])
#
#         spread_string = "/".join(self.spread_list[spread_row])
#         self.plot3.plot_line(spread_rank_chart, 'Spread Rank', 'Spread: {}, Duration: {}'.format(spread_string, duration_string))
#         self.plot3.plot_line(spread_percent_chart[:, [BAR_DICT['Date'], BAR_DICT['High']]], 'Spread [In percent of {}]', 'Spread: {}, Duration: {}'.format(self.spread_list[spread_row][0], spread_string, duration_string))
#         self.plot3.plot_line(spread_bp_chart[:, [BAR_DICT['Date'], BAR_DICT['High']]], 'Spread [Basis Points]',
#                                           'Spread: {}, Duration: {}'.format(spread_string, duration_string), twin=True)


class TemplateTab(QWidget):
    def __init__(self, mw, db):
        super(QWidget, self).__init__()

    # #################################################################################################################
    # Button Callbacks
    # #################################################################################################################


    # #################################################################################################################
    # Line Edit Callbacks
    # #################################################################################################################

    # #################################################################################################################
    # Signal Callbacks
    # #################################################################################################################

    # #################################################################################################################
    # Checkbox Callbacks
    # #################################################################################################################

    # #################################################################################################################
    # Functions
    # #################################################################################################################
