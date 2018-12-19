from __future__ import print_function

# import matplotlib.pyplot as plt
# import numpy as np
# import numpy as np
# import matplotlib
# import matplotlib.pyplot as plt
# import matplotlib.pyplot as plt
# from matplotlib.lines import Line2D
# from matplotlib.patches import Rectangle
# from matplotlib.text import Text
# from matplotlib.image import AxesImage
# import numpy as np
# from numpy.random import rand


# # # ####################################################################################################
# # # # IV Rank plot 1
# # # ####################################################################################################
# # sphinx_gallery_thumbnail_number = 2
#
# vegetables = ["cucumber", "tomato", "lettuce", "asparagus",
#               "potato", "wheat", "barley"]
# farmers = ["Farmer Joe", "Upland Bros.", "Smith Gardening",
#            "Agrifun", "Organiculture", "BioGoods Ltd.", "Cornylee Corp."]
#
# harvest = np.array([[0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
#                     [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0],
#                     [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0],
#                     [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0],
#                     [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0],
#                     [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1],
#                     [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3]])
#
#
# fig, ax = plt.subplots()
# im = ax.imshow(harvest)
#
# # We want to show all ticks...
# ax.set_xticks(np.arange(len(farmers)))
# ax.set_yticks(np.arange(len(vegetables)))
# # ... and label them with the respective list entries
# ax.set_xticklabels(farmers)
# ax.set_yticklabels(vegetables)
#
# # Rotate the tick labels and set their alignment.
# plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
#          rotation_mode="anchor")
#
# # Loop over data dimensions and create text annotations.
# for i in range(len(vegetables)):
#     for j in range(len(farmers)):
#         text = ax.text(j, i, harvest[i, j],
#                        ha="center", va="center", color="w")
#
# ax.set_title("Harvest of local farmers (in tons/year)")
# fig.tight_layout()
# plt.show()
#
#
#
#
# # # ####################################################################################################
# # # # IV Rank plot 2
# # # ####################################################################################################
#
# def heatmap(data, row_labels, col_labels, ax=None,
#             cbar_kw={}, cbarlabel="", **kwargs):
#     """
#     Create a heatmap from a numpy array and two lists of labels.
#
#     Arguments:
#         data       : A 2D numpy array of shape (N,M)
#         row_labels : A list or array of length N with the labels
#                      for the rows
#         col_labels : A list or array of length M with the labels
#                      for the columns
#     Optional arguments:
#         ax         : A matplotlib.axes.Axes instance to which the heatmap
#                      is plotted. If not provided, use current axes or
#                      create a new one.
#         cbar_kw    : A dictionary with arguments to
#                      :meth:`matplotlib.Figure.colorbar`.
#         cbarlabel  : The label for the colorbar
#     All other arguments are directly passed on to the imshow call.
#     """
#
#     if not ax:
#         ax = plt.gca()
#
#     # Plot the heatmap
#     im = ax.imshow(data, **kwargs)
#
#     # Create colorbar
#     cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
#     cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")
#
#     # We want to show all ticks...
#     ax.set_xticks(np.arange(data.shape[1]))
#     ax.set_yticks(np.arange(data.shape[0]))
#     # ... and label them with the respective list entries.
#     ax.set_xticklabels(col_labels)
#     ax.set_yticklabels(row_labels)
#
#     # Let the horizontal axes labeling appear on top.
#     ax.tick_params(top=True, bottom=False,
#                    labeltop=True, labelbottom=False)
#
#     # Rotate the tick labels and set their alignment.
#     plt.setp(ax.get_xticklabels(), rotation=-30, ha="right",
#              rotation_mode="anchor")
#
#     # Turn spines off and create white grid.
#     for edge, spine in ax.spines.items():
#         spine.set_visible(False)
#
#     ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
#     ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
#     ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
#     ax.tick_params(which="minor", bottom=False, left=False)
#
#     return im, cbar
#
#
# def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
#                      textcolors=["black", "white"],
#                      threshold=None, **textkw):
#     """
#     A function to annotate a heatmap.
#
#     Arguments:
#         im         : The AxesImage to be labeled.
#     Optional arguments:
#         data       : Data used to annotate. If None, the image's data is used.
#         valfmt     : The format of the annotations inside the heatmap.
#                      This should either use the string format method, e.g.
#                      "$ {x:.2f}", or be a :class:`matplotlib.ticker.Formatter`.
#         textcolors : A list or array of two color specifications. The first is
#                      used for values below a threshold, the second for those
#                      above.
#         threshold  : Value in data units according to which the colors from
#                      textcolors are applied. If None (the default) uses the
#                      middle of the colormap as separation.
#
#     Further arguments are passed on to the created text labels.
#     """
#
#     if not isinstance(data, (list, np.ndarray)):
#         data = im.get_array()
#
#     # Normalize the threshold to the images color range.
#     if threshold is not None:
#         threshold = im.norm(threshold)
#     else:
#         threshold = im.norm(data.max())/2.
#
#     # Set default alignment to center, but allow it to be
#     # overwritten by textkw.
#     kw = dict(horizontalalignment="center",
#               verticalalignment="center")
#     kw.update(textkw)
#
#     # Get the formatter in case a string is supplied
#     if isinstance(valfmt, str):
#         valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)
#
#     # Loop over the data and create a `Text` for each "pixel".
#     # Change the text's color depending on the data.
#     texts = []
#     for i in range(data.shape[0]):
#         for j in range(data.shape[1]):
#             kw.update(color=textcolors[im.norm(data[i, j]) > threshold])
#             text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
#             texts.append(text)
#
#     return texts
#
#
# if __name__ == '__main__':
#     fig, ax = plt.subplots()
#
#     vegetables = ["cucumber", "tomato", "lettuce", "asparagus",
#                   "potato", "wheat", "barley"]
#     farmers = ["Farmer Joe", "Upland Bros.", "Smith Gardening",
#                "Agrifun", "Organiculture", "BioGoods Ltd.", "Cornylee Corp."]
#
#     harvest = np.array([[0.8, 2.4, 2.5, 3.9, 0.0, 4.0, 0.0],
#                         [2.4, 0.0, 4.0, 1.0, 2.7, 0.0, 0.0],
#                         [1.1, 2.4, 0.8, 4.3, 1.9, 4.4, 0.0],
#                         [0.6, 0.0, 0.3, 0.0, 3.1, 0.0, 0.0],
#                         [0.7, 1.7, 0.6, 2.6, 2.2, 6.2, 0.0],
#                         [1.3, 1.2, 0.0, 0.0, 0.0, 3.2, 5.1],
#                         [0.1, 2.0, 0.0, 1.4, 0.0, 1.9, 6.3]])
#
#     im, cbar = heatmap(harvest, vegetables, farmers, ax=ax,
#                        cmap="YlGn", cbarlabel="IV Ranks")
#     texts = annotate_heatmap(im, valfmt="{x:.1f} t")
#
#     fig.tight_layout()
#     plt.show()



# # # ####################################################################################################
# # # # Matplotlib mouse callback
# # # ####################################################################################################
#
# if 1:  # simple picking, lines, rectangles and text
#     fig, (ax1, ax2) = plt.subplots(2, 1)
#     ax1.set_title('click on points, rectangles or text', picker=True)
#     ax1.set_ylabel('ylabel', picker=True, bbox=dict(facecolor='red'))
#     line, = ax1.plot(rand(100), 'o', picker=5)  # 5 points tolerance
#
#     # pick the rectangle
#     bars = ax2.bar(range(10), rand(10), picker=True)
#     for label in ax2.get_xticklabels():  # make the xtick labels pickable
#         label.set_picker(True)
#
#     def onpick1(event):
#         if isinstance(event.artist, Line2D):
#             thisline = event.artist
#             xdata = thisline.get_xdata()
#             ydata = thisline.get_ydata()
#             ind = event.ind
#             print('onpick1 line:', zip(np.take(xdata, ind), np.take(ydata, ind)))
#         elif isinstance(event.artist, Rectangle):
#             patch = event.artist
#             print('onpick1 patch:', patch.get_path())
#         elif isinstance(event.artist, Text):
#             text = event.artist
#             print('onpick1 text:', text.get_text())
#
#     fig.canvas.mpl_connect('pick_event', onpick1)
#
# if 1:  # picking with a custom hit test function
#     # you can define custom pickers by setting picker to a callable
#     # function.  The function has the signature
#     #
#     #  hit, props = func(artist, mouseevent)
#     #
#     # to determine the hit test.  if the mouse event is over the artist,
#     # return hit=True and props is a dictionary of
#     # properties you want added to the PickEvent attributes
#
#     def line_picker(line, mouseevent):
#         """
#         find the points within a certain distance from the mouseclick in
#         data coords and attach some extra attributes, pickx and picky
#         which are the data points that were picked
#         """
#         if mouseevent.xdata is None:
#             return False, dict()
#         xdata = line.get_xdata()
#         ydata = line.get_ydata()
#         maxd = 0.05
#         d = np.sqrt((xdata - mouseevent.xdata)**2. + (ydata - mouseevent.ydata)**2.)
#
#         ind = np.nonzero(np.less_equal(d, maxd))
#         if len(ind):
#             pickx = np.take(xdata, ind)
#             picky = np.take(ydata, ind)
#             props = dict(ind=ind, pickx=pickx, picky=picky)
#             return True, props
#         else:
#             return False, dict()
#
#     def onpick2(event):
#         print('onpick2 line:', event.pickx, event.picky)
#
#     fig, ax = plt.subplots()
#     ax.set_title('custom picker for line data')
#     line, = ax.plot(rand(100), rand(100), 'o', picker=line_picker)
#     fig.canvas.mpl_connect('pick_event', onpick2)
#
#
# if 1:  # picking on a scatter plot (matplotlib.collections.RegularPolyCollection)
#
#     x, y, c, s = rand(4, 100)
#
#     def onpick3(event):
#         ind = event.ind
#         print('onpick3 scatter:', ind, np.take(x, ind), np.take(y, ind))
#
#     fig, ax = plt.subplots()
#     col = ax.scatter(x, y, 100*s, c, picker=True)
#     #fig.savefig('pscoll.eps')
#     fig.canvas.mpl_connect('pick_event', onpick3)
#
# if 1:  # picking images (matplotlib.image.AxesImage)
#     fig, ax = plt.subplots()
#     im1 = ax.imshow(rand(10, 5), extent=(1, 2, 1, 2), picker=True)
#     im2 = ax.imshow(rand(5, 10), extent=(3, 4, 1, 2), picker=True)
#     im3 = ax.imshow(rand(20, 25), extent=(1, 2, 3, 4), picker=True)
#     im4 = ax.imshow(rand(30, 12), extent=(3, 4, 3, 4), picker=True)
#     ax.axis([0, 5, 0, 5])
#
#     def onpick4(event):
#         artist = event.artist
#         if isinstance(artist, AxesImage):
#             im = artist
#             A = im.get_array()
#             print('onpick4 image', A.shape)
#
#     fig.canvas.mpl_connect('pick_event', onpick4)
#
#
# plt.show()






















# # # ####################################################################################################
# # # # Matplotlib Navigation Bar
# # # ####################################################################################################
#
# import sys
# from PyQt5 import QtGui
# from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout
#
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# from matplotlib.figure import Figure
#
# import random
#
# class Window(QDialog):
#     def __init__(self, parent=None):
#         super(Window, self).__init__(parent)
#
#         # a figure instance to plot on
#         self.figure = Figure()
#
#         # this is the Canvas Widget that displays the `figure`
#         # it takes the `figure` instance as a parameter to __init__
#         self.canvas = FigureCanvas(self.figure)
#
#         # this is the Navigation widget
#         # it takes the Canvas widget and a parent
#         self.toolbar = NavigationToolbar(self.canvas, self)
#
#         # Just some button connected to `plot` method
#         self.button = QPushButton('Plot')
#         self.button.clicked.connect(self.plot)
#
#         # set the layout
#         layout = QVBoxLayout()
#         layout.addWidget(self.toolbar)
#         layout.addWidget(self.canvas)
#         layout.addWidget(self.button)
#         self.setLayout(layout)
#
#     def plot(self):
#         ''' plot some random stuff '''
#         # random data
#         data = [random.random() for i in range(10)]
#
#         # create an axis
#         ax = self.figure.add_subplot(111)
#
#         # discards the old graph
#         ax.clear()
#
#         # plot data
#         ax.plot(data, '*-')
#
#         # refresh canvas
#         self.canvas.draw()
#
# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#
#     main = Window()
#     main.show()
#
#     sys.exit(app.exec_())












# # # ####################################################################################################
# # # # Matplotlib Scroll Window
# # # ####################################################################################################
# import matplotlib
# # Make sure that we are using QT5
# matplotlib.use('Qt5Agg')
# import matplotlib.pyplot as plt
# from PyQt5 import QtWidgets
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
#
#
# class ScrollableWindow(QtWidgets.QMainWindow):
#     def __init__(self, fig):
#         self.qapp = QtWidgets.QApplication([])
#
#         QtWidgets.QMainWindow.__init__(self)
#         self.widget = QtWidgets.QWidget()
#         self.setCentralWidget(self.widget)
#         self.widget.setLayout(QtWidgets.QVBoxLayout())
#         self.widget.layout().setContentsMargins(0,0,0,0)
#         self.widget.layout().setSpacing(0)
#
#         self.fig = fig
#         self.canvas = FigureCanvas(self.fig)
#         self.canvas.draw()
#         self.scroll = QtWidgets.QScrollArea(self.widget)
#         self.scroll.setWidget(self.canvas)
#
#         self.nav = NavigationToolbar(self.canvas, self.widget)
#         self.widget.layout().addWidget(self.nav)
#         self.widget.layout().addWidget(self.scroll)
#
#         self.show()
#         exit(self.qapp.exec_())
#
#
# # create a figure and some subplots
# fig, axes = plt.subplots(ncols=4, nrows=5, figsize=(16,16))
# for ax in axes.flatten():
#     ax.plot([2,3,5,1])
#
# # pass the figure to the custom window
# a = ScrollableWindow(fig)













# # # ####################################################################################################
# # # # Matplotlib 2 Y axes
# # # ####################################################################################################
# import numpy as np
# import matplotlib.pyplot as plt
#
# # Create some mock data
# t = np.arange(0.01, 10.0, 0.01)
# data1 = np.exp(t)
# data2 = np.sin(2 * np.pi * t)
#
# fig, ax1 = plt.subplots()
#
# color = 'tab:red'
# ax1.set_xlabel('time (s)')
# ax1.set_ylabel('exp', color=color)
# ax1.plot(t, data1, color=color)
# ax1.tick_params(axis='y', labelcolor=color)
#
# ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
#
# # color = 'tab:blue'
# # ax2.set_ylabel('sin', color=color)  # we already handled the x-label with ax1
# ax2.plot(t, data2, color=color)
# # ax2.tick_params(axis='y', labelcolor=color)
#
# # fig.tight_layout()  # otherwise the right y-label is slightly clipped
# plt.show()






# # # # ####################################################################################################
# # # # # Historical Volatility
# # # # ####################################################################################################
# from __future__ import division
# from pandas_datareader import data
# from datetime import datetime, timedelta
# import numpy as np
# import matplotlib.pyplot as plt
#
# # get stock ticker symbol from user
# stock_symbol = raw_input(
#     'Enter ticker symbol for stock: ').upper()
#
# returns = [];
# stds = []
# for days in [31, 92, 365]:
#     # set time period for historical prices
#     end_time = datetime.today(
#     ).strftime('%m/%d/%Y')  # current date
#     start_time = (datetime.today() -
#                   timedelta(days=days)
#                   ).strftime('%m/%d/%Y')
#
#     # retreive historical prices for stock
#     prices = data.DataReader(stock_symbol,
#                              data_source='yahoo',
#                              start=start_time, end=end_time)
#
#     # sort dates in descending order
#     prices.sort_index(ascending=False, inplace=True)
#
#     # calculate daily logarithmic return
#     prices['Return'] = (np.log(prices['Close'] /
#                                prices['Close'].shift(-1)))
#
#     # calculate daily standard deviation of returns
#     d_std = np.std(prices.Return)
#
#     # annualize daily standard deviation
#     std = d_std * 252 ** 0.5
#
#     returns.append(list(prices.Return))
#     stds.append(std)
#
# # Plot histograms
# fig, ax = plt.subplots(1, 1, figsize=(7, 5))
# n, bins, patches = ax.hist(returns[2][:-1],
#                            bins=50, alpha=0.65, color='blue',
#                            label='12-month')
# n, bins, patches = ax.hist(returns[1][:-1],
#                            bins=50, alpha=0.65, color='green',
#                            label='3-month')
# n, bins, patches = ax.hist(returns[0][:-1],
#                            bins=50, alpha=0.65, color='magenta',
#                            label='1-month')
# ax.set_xlabel('log return of stock price')
# ax.set_ylabel('frequency of log return')
# ax.set_title('Historical Volatility for ' +
#              stock_symbol)
#
# # get x and y coordinate limits
# x_corr = ax.get_xlim()
# y_corr = ax.get_ylim()
#
# # make room for text
# header = y_corr[1] / 5
# y_corr = (y_corr[0], y_corr[1] + header)
# ax.set_ylim(y_corr[0], y_corr[1])
#
# # print historical volatility on plot
# x = x_corr[0] + (x_corr[1] - x_corr[0]) / 30
# y = y_corr[1] - (y_corr[1] - y_corr[0]) / 15
# ax.text(x, y, 'Annualized Volatility: ',
#         fontsize=11, fontweight='bold')
# x = x_corr[0] + (x_corr[1] - x_corr[0]) / 15
# y -= (y_corr[1] - y_corr[0]) / 20
# ax.text(x, y, '1-month  = ' + str(np.round(stds[0], 3)),
#         fontsize=10)
# y -= (y_corr[1] - y_corr[0]) / 20
# ax.text(x, y, '3-month  = ' + str(np.round(stds[1], 3)),
#         fontsize=10)
# y -= (y_corr[1] - y_corr[0]) / 20
# ax.text(x, y, '12-month = ' + str(np.round(stds[2], 3)),
#         fontsize=10)
#
# # add legend
# ax.legend(loc='upper center',
#           bbox_to_anchor=(0.5, -0.1),
#           ncol=3, fontsize=11)
#
# # display plot
# fig.tight_layout()
# fig.show()
















# # # ####################################################################################################
# # # # Scrollbar (QMainWindow)
# # # ####################################################################################################

import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication, QVBoxLayout, QScrollArea
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as Canvas
from matplotlib.figure import Figure
import matplotlib.patches as patches
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import Rectangle

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QScrollArea
from PyQt5.QtCore import pyqtSignal

from model.Defintion import BAR_DICT
import numpy as np
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

class ScrollableWindow(QMainWindow):
    cell_select = pyqtSignal(int, int)

    def __init__(self):
        self.qapp = QApplication([])

        QMainWindow.__init__(self)
        self.widget = QWidget()
        self.setCentralWidget(self.widget)
        self.widget.setLayout(QVBoxLayout())
        # self.widget.layout().setContentsMargins(0,0,0,0)
        # self.widget.layout().setSpacing(0)

        self.fig = Figure(dpi=200)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.draw()
        self.scroll = QScrollArea(self.widget)
        self.scroll.setWidget(self.canvas)

        # self.nav = NavigationToolbar(self.canvas, self.widget)
        # self.widget.layout().addWidget(self.nav)
        self.widget.layout().addWidget(self.scroll)

        self.axes = self.fig.add_subplot(111)

        self.fig.sca(self.axes)

        self.text_list = None
        self.cbar = None
        self.i = None
        self.j = None

        self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.sel_rect = None

        self.fig.canvas.mpl_connect('scroll_event', self._on_mousewheel)

        # self.canvas.Bind("<Button-4>", self._on_mousewheel)
        # self.canvas.Bind("<Button-5>", self._on_mousewheel)



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
    def _on_mousewheel(self, event):
        vbar = self.scroll.verticalScrollBar()
        cur_val = vbar.value()
        max_val = vbar.maximum()

        if event.button == 'up':
            new_val = cur_val - max_val/10
        else:
            new_val = cur_val + max_val/10
        vbar.setValue(new_val)

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
        # cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
        # cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")
        cbar = None

        # We want to show all ticks...
        ax.set_xticks(np.arange(data.shape[1]))
        ax.set_yticks(np.arange(data.shape[0]))
        # ... and label them with the respective list entries.
        ax.xaxis.set_ticks_position('top')
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
        # self.fig.tight_layout()
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


# # create a figure and some subplots
# fig, axes = plt.subplots(ncols=4, nrows=5, figsize=(16,16))
# for ax in axes.flatten():
#     ax.plot([2,3,5,1])

# pass the figure to the custom window
a = ScrollableWindow()
duration_list_str = ['20', '40', '60', '80', '100', '100', '100']
symbol_list = ['SPY', 'QQQ', 'IWM', 'FXI']
iv_rank_array = np.asarray([[1,2,3,1,2,3], [3,4,5,1,2,3], [6,7,8,1,2,3], [1,17,18,1,2,3]])
a.plot(iv_rank_array, duration_list_str, symbol_list, 'IV Rank')

a.show()
exit(a.qapp.exec_())