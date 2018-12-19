import matplotlib.pyplot as plt
from mpl_finance import candlestick_ohlc
from matplotlib.dates import date2num
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import matplotlib.ticker as ticker
import datetime
import numpy as np

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
import matplotlib.patches as patches
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Rectangle

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt5.QtCore import pyqtSignal

from model.Defintion import BAR_DICT


def plot_candlestick(data_in):
    """
    Add volume: https://stackoverflow.com/questions/13128647/matplotlib-finance-volume-overlay
    :param data_in: list of list [[bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume], [...], ...]
    :return:
    """
    # Loop over all candles
    # data_in = [1,1]
    ohlc_data = []
    self.axes.cla()
    for i in range(0, len(data_in)):
        date = data_in[i][BAR_DICT['Date']]
        conv_date = datetime.datetime.strptime(date, '%Y%m%d')

        # data_in[i][1] = data_in[i][1].astype(float)
        # data_in[i][2] = data_in[i][2].astype(float)
        # data_in[i][3] = data_in[i][3].astype(float)
        # data_in[i][4] = data_in[i][4].astype(float)
        # data_in[i][5] = data_in[i][5].astype(float)
        ohlc = []
        ohlc.append(date2num(conv_date))
        ohlc.append(float(data_in[i][1]))
        ohlc.append(float(data_in[i][2]))
        ohlc.append(float(data_in[i][3]))
        ohlc.append(float(data_in[i][4]))
        ohlc.append(float(data_in[i][5]))
        ohlc_data.append(ohlc)

    candlestick_ohlc(self.axes, ohlc_data, width=0.4, colorup='#77d879', colordown='#db3f3f')
    self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    self.axes.xaxis.set_major_locator(mticker.MaxNLocator(10))
    self.fig.autofmt_xdate()
    self.axes.grid(True)
    self.draw()


class PricePlot(Canvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        Canvas.__init__(self, self.fig)
        self.axes = self.fig.add_subplot(111)
        self.setParent(parent)

        # data_in = [['20180423', 267.29, 267.83, 265.36, 266.56, 5781],
        #                 ['20180424', 267.73, 267.94, 261.29, 263.07, 15653],
        #                 ['20180425', 262.98, 264.12, 260.86, 263.59, 15960],
        #                 ['20180426', 264.81, 267.24, 264.33, 266.3, 11205],
        #                 ['20180427', 267.03, 267.33, 265.51, 266.58, 11160],
        #                 ['20180430', 267.26, 267.88, 264.5, 264.53, 19268],
        #                 ['20180501', 263.86, 265.1, 262.12, 265.0, 11051],
        #                 ['20180502', 264.81, 265.67, 262.77, 263.18, 15367],
        #                 ['20180503', 261.87, 263.36, 259.08, 262.64, 9024],
        #                 ['20180504', 261.52, 266.78, 261.16, 266.0, 20176]]
        # self.plot_candlestick(data_in)

    def plot_candlestick(self, data_in):
        """
        Add volume: https://stackoverflow.com/questions/13128647/matplotlib-finance-volume-overlay
        :param data_in: list of list [[bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume], [...], ...]
        :return:
        """
        # Loop over all candles
        # data_in = [1,1]
        ohlc_data = []
        self.axes.cla()
        for i in range(0, len(data_in)):
            date = data_in[i][BAR_DICT['Date']]
            conv_date = datetime.datetime.strptime(date, '%Y%m%d')

            # data_in[i][1] = data_in[i][1].astype(float)
            # data_in[i][2] = data_in[i][2].astype(float)
            # data_in[i][3] = data_in[i][3].astype(float)
            # data_in[i][4] = data_in[i][4].astype(float)
            # data_in[i][5] = data_in[i][5].astype(float)
            ohlc = []
            ohlc.append(date2num(conv_date))
            ohlc.append(float(data_in[i][1]))
            ohlc.append(float(data_in[i][2]))
            ohlc.append(float(data_in[i][3]))
            ohlc.append(float(data_in[i][4]))
            ohlc.append(float(data_in[i][5]))
            ohlc_data.append(ohlc)

        candlestick_ohlc(self.axes, ohlc_data, width=0.4, colorup='#77d879', colordown='#db3f3f')
        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.axes.xaxis.set_major_locator(mticker.MaxNLocator(10))
        self.fig.autofmt_xdate()
        self.axes.grid(True)
        self.draw()

    def plot_line(self, data_in_1, data_in_2=None):
        self.axes.cla()

        for data_in in [data_in_1, data_in_2]:
            for i in range(0, len(data_in)):
                date = data_in[i][BAR_DICT['Date']]
                conv_date = datetime.datetime.strptime(date, '%Y%m%d')
                data_in[i][BAR_DICT['Date']] = conv_date# date2num(conv_date)
                data_in[i][1] = float(data_in[i][1])

            x = data_in[:, BAR_DICT['Date']]
            y = data_in[:, 1]

            self.axes.plot(x, y)

        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.axes.xaxis.set_major_locator(mticker.MaxNLocator(10))

        self.fig.autofmt_xdate()

        self.axes.grid(True)
        self.draw()


class PriceNavPlot(QWidget):
    def __init__(self, parent=None, mw=None, width=5, height=4, dpi=100):
        super(QWidget, self).__init__(parent)
        self.fig = Figure()
        self.canvas = Canvas(self.fig)
        self.canvas.setParent(parent)
        self.toolbar = NavigationToolbar(self.canvas, self)
        # set the layout
        l1 = QVBoxLayout(parent)
        l1.addWidget(self.toolbar)
        l1.addWidget(self.canvas)

        self.axes = self.fig.add_subplot(111)
        self.axes2 = self.axes.twinx()
        self.fig.sca(self.axes)

        self.setParent(parent)

        self.data_list = []
        self.legend_list = []
        self.data_list_2 = []
        self.legend_list_2 = []
        self.title = ''

        self.left_lim = None
        self.right_lim = None

        self.plot_type = ''

    def set_xlim(self, left_lim, right_lim):
        self.left_lim = left_lim
        self.right_lim = right_lim
        if self.plot_type == 'line':
            self._plot_line()
        if self.plot_type == 'candlestick':
            self._plot_candlestick()

    def plot_candlestick(self, data_in, legend=' ', title=' '):
        self.plot_type = 'candlestick'
        self.data_list.append(data_in)
        self.legend_list.append(legend)
        self.title = title
        self._plot_candlestick()

    def _plot_candlestick(self):
        """
        Add volume: https://stackoverflow.com/questions/13128647/matplotlib-finance-volume-overlay
        :param data_in: list of list [[bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume], [...], ...]
        :return:
        """
        # Loop over all candles
        # data_in = [1,1]
        ohlc_data = []
        self.axes.cla()
        for data_in in self.data_list:
            for i in range(0, len(data_in)):
                ohlc = []
                ohlc.append(date2num(data_in[i][BAR_DICT['Date']]))
                ohlc.append(float(data_in[i][1]))
                ohlc.append(float(data_in[i][2]))
                ohlc.append(float(data_in[i][3]))
                ohlc.append(float(data_in[i][4]))
                ohlc.append(float(data_in[i][5]))
                ohlc_data.append(ohlc)

            candlestick_ohlc(self.axes, ohlc_data, width=0.4, colorup='#77d879', colordown='#db3f3f')
        if self.right_lim is not None and self.left_lim is not None:
            self.axes.set_xlim(self.left_lim, self.right_lim)
        self.axes.set_title(self.title)
        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.axes.xaxis.set_major_locator(mticker.MaxNLocator(10))
        self.fig.autofmt_xdate()
        self.axes.grid(True)
        self.canvas.draw()

    def clear(self):
        self.data_list = []
        self.data_list_2 = []
        self.legend_list = []
        self.legend_list_2 = []
        self.title = ''

    def plot_line(self, data_in, legend=' ', title=' ', twin=False):
        self.plot_type = 'line'
        self.title = title
        if twin is False:
            self.data_list.append(data_in)
        else:
            self.data_list_2.append(data_in)
            self.legend_list_2.append(legend)
        self.legend_list.append(legend)
        self._plot_line()

    def _plot_line(self):
        self.axes.cla()
        self.axes2.cla()

        for data in self.data_list:
            x = data[:, BAR_DICT['Date']]
            y = data[:, 1]
            self.axes.plot(x, y)
        for data in self.data_list_2:
            x = data[:, BAR_DICT['Date']]
            y = data[:, 1]
            self.axes2.plot(x, y, color=(1, 0, 0))
        self.axes2.set_ylabel(self.legend_list_2, color=(1, 0, 0))
        # self.axes2.legend(self.legend_list_2)

        if self.right_lim is not None and self.left_lim is not None:
            self.axes.set_xlim(self.left_lim, self.right_lim)
            self.axes2.set_xlim(self.left_lim, self.right_lim)

        self.axes.set_title(self.title)
        self.axes.legend(self.legend_list)
        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        self.axes.xaxis.set_major_locator(mticker.MaxNLocator(10))
        self.fig.autofmt_xdate()
        self.axes.grid(True)
        self.canvas.draw()


class RankPlotOld(Canvas, QWidget):
    cell_select = pyqtSignal(int, int)

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        Canvas.__init__(self, self.fig)
        self.axes = self.fig.add_subplot(111)
        self.setParent(parent)
        self.text_list = None
        self.cbar = None
        self.i = None
        self.j = None

        cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.sel_rect = None

    def get_clicked_symbol(self):
        if self.i is None:
            return -1
        else:
            return self.i

    def get_clicked_iv_rank(self):
        return self.j

    def heatmap(self, data, row_labels, col_labels, ax=None,
                cbar_kw={}, cbarlabel="", **kwargs):
        """
        Create a heatmap from a numpy array and two lists of labels.

        Arguments:
            data       : A 2D numpy array of shape (N,M)
            row_labels : A list or array of length N with the labels
                         for the rows
            col_labels : A list or array of length M with the labels
                         for the columns
        Optional arguments:
            ax         : A matplotlib.axes.Axes instance to which the heatmap
                         is plotted. If not provided, use current axes or
                         create a new one.
            cbar_kw    : A dictionary with arguments to
                         :meth:`matplotlib.Figure.colorbar`.
            cbarlabel  : The label for the colorbar
        All other arguments are directly passed on to the imshow call.
        """

        if not ax:
            ax = plt.gca()

        # Plot the heatmap
        im = ax.imshow(data, **kwargs, vmin=0, vmax=100)

        # Create colorbar
        cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
        cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

        # We want to show all ticks...
        ax.set_xticks(np.arange(data.shape[1]))
        ax.set_yticks(np.arange(data.shape[0]))
        # ... and label them with the respective list entries.
        ax.set_xticklabels(col_labels)
        ax.set_yticklabels(row_labels)

        # Let the horizontal axes labeling appear on top.
        ax.tick_params(top=False, bottom=True,
                       labeltop=False, labelbottom=True)

        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=0, ha="right",
                 rotation_mode="anchor")

        # Turn spines off and create white grid.
        for edge, spine in ax.spines.items():
            spine.set_visible(False)

        ax.set_xticks(np.arange(data.shape[1] + 1) - .5, minor=True)
        ax.set_yticks(np.arange(data.shape[0] + 1) - .5, minor=True)
        ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
        ax.tick_params(which="minor", bottom=False, left=False)

        return im, cbar

    def annotate_heatmap(self, im, data=None, valfmt="{x:.2f}",
                         textcolors=["black", "black"],
                         threshold=None, **textkw):
        """
        A function to annotate a heatmap.

        Arguments:
            im         : The AxesImage to be labeled.
        Optional arguments:
            data       : Data used to annotate. If None, the image's data is used.
            valfmt     : The format of the annotations inside the heatmap.
                         This should either use the string format method, e.g.
                         "$ {x:.2f}", or be a :class:`matplotlib.ticker.Formatter`.
            textcolors : A list or array of two color specifications. The first is
                         used for values below a threshold, the second for those
                         above.
            threshold  : Value in data units according to which the colors from
                         textcolors are applied. If None (the default) uses the
                         middle of the colormap as separation.

        Further arguments are passed on to the created text labels.
        """

        if not isinstance(data, (list, np.ndarray)):
            data = im.get_array()

        # Normalize the threshold to the images color range.
        if threshold is not None:
            threshold = im.norm(threshold)
        else:
            threshold = im.norm(data.max()) / 2.

        # Set default alignment to center, but allow it to be
        # overwritten by textkw.
        kw = dict(horizontalalignment="center",
                  verticalalignment="center")
        kw.update(textkw)

        # Get the formatter in case a string is supplied
        if isinstance(valfmt, str):
            valfmt = ticker.StrMethodFormatter(valfmt)

        # Loop over the data and create a `Text` for each "pixel".
        # Change the text's color depending on the data.
        texts = []

        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                kw.update(color=textcolors[im.norm(data[i, j]) > threshold])
                text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
                texts.append(text)

        return texts

    def plot(self, data_in, x_labels, y_labels, title):
        """
        Add volume: https://stackoverflow.com/questions/13128647/matplotlib-finance-volume-overlay
        :param data_in: list of list [[bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume], [...], ...]
        :return:
        """
        self.axes.clear()
        if self.cbar is not None:
            self.cbar.remove()
        self.axes.set_title(title)

        im, self.cbar = self.heatmap(data_in, y_labels, x_labels, ax=self.axes,
                           cmap="YlGn", cbarlabel=title)
        self.text_list = self.annotate_heatmap(im, valfmt="{x:.0f}")

        self.fig.autofmt_xdate()
        self.fig.tight_layout()
        self.draw()

    def highlight_selection(self, row, col):
        if self.sel_rect is None:
            self.sel_rect = Rectangle((col-0.5+0.1, row-0.5+0.1), width=0.8, height=0.8, edgecolor='red', fill=False,
                                      linewidth=4)
            self.axes.add_patch(self.sel_rect)
        else:
            self.sel_rect.set_xy((col-0.5+0.1, row-0.5+0.1))
        self.draw()

    def onclick(self, event):
        if event.ydata is not None and event.xdata is not None:
            self.i = int(round(event.ydata))     # Rows (1. Index = 0)
            self.j = int(round(event.xdata))     # Columns (1. Index = 0)
            self.cell_select.emit(self.i, self.j)
            # self.highlight_selection(self.i, self.j)


class RankPlot(QWidget):
    cell_select = pyqtSignal(int, int)

    def __init__(self, parent=None, show_bar='False', width=5, height=4, dpi=100):
        super(QWidget, self).__init__(parent)
        self.fig = Figure()
        self.canvas = Canvas(self.fig)
        self.canvas.setParent(parent)
        # set the layout
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.layout().setSpacing(0)

        self.canvas.draw()
        self.scroll = QScrollArea(self)
        self.scroll.setWidget(self.canvas)
        self.layout().addWidget(self.scroll)

        # l1 = QVBoxLayout(parent)
        # l1.setContentsMargins(0, 0, 0, 0)
        # l1.setSpacing(0)
        # l1.addWidget(self.canvas)

        # self.scroll = QScrollArea(self)
        # self.scroll.setWidget(self.canvas)
        #
        # l1.addWidget(self.scroll)

        self.axes = self.fig.add_subplot(111)
        self.fig.sca(self.axes)

        # self.setParent(parent)

        self.text_list = None
        self.show_bar = show_bar
        self.cbar = None
        self.i = None
        self.j = None

        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.fig.canvas.mpl_connect('scroll_event', self._on_mousewheel)
        self.sel_rect = None

        ############################################################################
        #
        # self.fig = Figure(figsize=(width, height), dpi=dpi)
        # Canvas.__init__(self, self.fig)
        # self.axes = self.fig.add_subplot(111)
        # self.setParent(parent)
        # self.text_list = None
        # self.cbar = None
        # self.i = None
        # self.j = None
        #
        # self.scroll = QScrollArea(self)
        # self.scroll.setWidget(self)
        #
        # cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        # self.sel_rect = None

    def get_clicked_symbol(self):
        if self.i is None:
            return -1
        else:
            return self.i

    def get_clicked_iv_rank(self):
        return self.j

    def heatmap(self, data, row_labels, col_labels, ax=None,
                cbar_kw={}, cbarlabel="", **kwargs):
        """
        Create a heatmap from a numpy array and two lists of labels.

        Arguments:
            data       : A 2D numpy array of shape (N,M)
            row_labels : A list or array of length N with the labels
                         for the rows
            col_labels : A list or array of length M with the labels
                         for the columns
        Optional arguments:
            ax         : A matplotlib.axes.Axes instance to which the heatmap
                         is plotted. If not provided, use current axes or
                         create a new one.
            cbar_kw    : A dictionary with arguments to
                         :meth:`matplotlib.Figure.colorbar`.
            cbarlabel  : The label for the colorbar
        All other arguments are directly passed on to the imshow call.
        """

        if not ax:
            ax = plt.gca()

        # Plot the heatmap
        im = ax.imshow(data, **kwargs, vmin=0, vmax=100)
        # Create colorbar
        if self.show_bar is True:
            cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
            cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")
        else:
            cbar = None
        # We want to show all ticks...
        ax.set_xticks(np.arange(data.shape[1]))
        ax.set_yticks(np.arange(data.shape[0]))
        # ... and label them with the respective list entries.
        ax.set_xticklabels(col_labels)
        ax.xaxis.set_ticks_position('top')
        ax.set_yticklabels(row_labels)

        # Let the horizontal axes labeling appear on top.
        ax.tick_params(top=False, bottom=True,
                       labeltop=False, labelbottom=True)

        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=0, ha="right",
                 rotation_mode="anchor")

        # Turn spines off and create white grid.
        for edge, spine in ax.spines.items():
            spine.set_visible(False)

        ax.set_xticks(np.arange(data.shape[1] + 1) - .5, minor=True)
        ax.set_yticks(np.arange(data.shape[0] + 1) - .5, minor=True)
        ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
        ax.tick_params(which="minor", bottom=False, left=False)

        return im, cbar

    def annotate_heatmap(self, im, data=None, valfmt="{x:.2f}",
                         textcolors=["black", "black"],
                         threshold=None, **textkw):
        """
        A function to annotate a heatmap.

        Arguments:
            im         : The AxesImage to be labeled.
        Optional arguments:
            data       : Data used to annotate. If None, the image's data is used.
            valfmt     : The format of the annotations inside the heatmap.
                         This should either use the string format method, e.g.
                         "$ {x:.2f}", or be a :class:`matplotlib.ticker.Formatter`.
            textcolors : A list or array of two color specifications. The first is
                         used for values below a threshold, the second for those
                         above.
            threshold  : Value in data units according to which the colors from
                         textcolors are applied. If None (the default) uses the
                         middle of the colormap as separation.

        Further arguments are passed on to the created text labels.
        """

        if not isinstance(data, (list, np.ndarray)):
            data = im.get_array()

        # Normalize the threshold to the images color range.
        if threshold is not None:
            threshold = im.norm(threshold)
        else:
            threshold = im.norm(data.max()) / 2.

        # Set default alignment to center, but allow it to be
        # overwritten by textkw.
        kw = dict(horizontalalignment="center",
                  verticalalignment="center")
        kw.update(textkw)

        # Get the formatter in case a string is supplied
        if isinstance(valfmt, str):
            valfmt = ticker.StrMethodFormatter(valfmt)

        # Loop over the data and create a `Text` for each "pixel".
        # Change the text's color depending on the data.
        texts = []

        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                kw.update(color=textcolors[im.norm(data[i, j]) > threshold])
                text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
                texts.append(text)

        return texts

    def plot(self, data_in, x_labels, y_labels, title):
        """
        Add volume: https://stackoverflow.com/questions/13128647/matplotlib-finance-volume-overlay
        :param data_in: list of list [[bar.date, bar.open, bar.high, bar.low, bar.close, bar.volume], [...], ...]
        :return:
        """
        self.axes.clear()
        if self.cbar is not None:
            self.cbar.remove()
        self.axes.set_title(title)

        if self.show_bar is False:
            im, self.cbar = self.heatmap(data_in, y_labels, x_labels, ax=self.axes,
                                         cbarlabel=title)
        else:
            im, self.cbar = self.heatmap(data_in, y_labels, x_labels, ax=self.axes,
                               cmap="YlGn", cbarlabel=title)
        self.text_list = self.annotate_heatmap(im, valfmt="{x:.0f}")

        self.fig.autofmt_xdate()
        self.fig.tight_layout()
        self.canvas.draw()

    def highlight_selection(self, row, col):
        if self.sel_rect is None:
            self.sel_rect = Rectangle((col-0.5+0.1, row-0.5+0.1), width=0.8, height=0.8, edgecolor='red', fill=False,
                                      linewidth=4)
            self.axes.add_patch(self.sel_rect)
        else:
            self.sel_rect.set_xy((col-0.5+0.1, row-0.5+0.1))
        self.canvas.draw()

    def onclick(self, event):
        print('Event')
        if event.ydata is not None and event.xdata is not None:
            self.i = int(round(event.ydata))     # Rows (1. Index = 0)
            self.j = int(round(event.xdata))     # Columns (1. Index = 0)
            self.cell_select.emit(self.i, self.j)
            # self.highlight_selection(self.i, self.j)
            print('{}, {} '.format(self.i, self.j))

    def _on_mousewheel(self, event):
        vbar = self.scroll.verticalScrollBar()
        cur_val = vbar.value()
        max_val = vbar.maximum()

        if event.button == 'up':
            new_val = cur_val - max_val/10
        else:
            new_val = cur_val + max_val/10
        vbar.setValue(new_val)


