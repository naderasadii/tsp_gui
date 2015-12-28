import sys
import numpy as np
import matplotlib as mpl
mpl.use('Qt5Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import NullLocator
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()
        self.show()

    def init_ui(self):
        self.setWindowTitle('TSP')
        self.setGeometry(100, 100, 1500, 1000)
        self.canvas = CityMap(self)
        self.button1 = QPushButton('Clear all')
        self.button1.clicked.connect(self.clear_fig)
        self.button2 = QPushButton('Nearest neighbor method')
        self.button3 = QPushButton('2-opt method')
        self.button3.setEnabled(False)
        self.layout1 = QVBoxLayout()
        self.layout1.addWidget(self.canvas)
        self.layout_button = QHBoxLayout()
        self.layout_button.addWidget(self.button1)
        self.layout_button.addWidget(self.button2)
        self.layout_button.addWidget(self.button3)
        self.layout1.addLayout(self.layout_button)
        self.setLayout(self.layout1)

    def clear_fig(self):
        self.canvas.clear_all()
        self.button3.setEnabled(False)
        
    def exec_nn(self):
        X = self.canvas.getx()
        Y = self.canvas.gety()
        city_pos = np.vstack((X, Y)).transpose()
        print(city_pos)


class CityMap(FigureCanvasQTAgg):
    def __init__(self, parent=None):
        self.fig = plt.figure()
        super(CityMap, self).__init__(self.fig)
        self.setParent(parent)
        self.init_axes()
        self.cid_putdot = self.fig.canvas.mpl_connect('button_press_event', self.put_city)
        self.cid_remove = self.fig.canvas.mpl_connect('pick_event', self.remove_city)
        self.cid_clear = self.fig.canvas.mpl_connect('button_press_event', self.clear_dots)

    def init_axes(self):
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(0.0, 1.0)
        self.ax.set_ylim(0.0, 1.0)
        self.ax.set_aspect('equal')
        self.ax.xaxis.set_major_locator(NullLocator())
        self.ax.yaxis.set_major_locator(NullLocator())

    def put_city(self, event):
        if event.inaxes != self.ax: return
        if event.button != 1: return
        x = event.xdata
        y = event.ydata
        self.ax.plot(x, y, 'bo', markersize=10, picker=5)
        self.draw()

    def remove_city(self, event):
        mouseevent = event.mouseevent
        if mouseevent.button != 3: return
        thisline = event.artist
        thisline.remove()
        self.draw()

    def getx(self):
        lines = self.ax.lines
        return np.array([line.get_xdata() for line in lines]).flatten()

    def gety(self):
        lines = self.ax.lines
        return np.array([line.get_ydata() for line in lines]).flatten()

    def clear_dots(self, event=False):
        if not event: return
        if event.inaxes != self.ax: return
        if event.button != 2: return
        self.clear_all()

    def clear_all(self):
        self.ax.cla()
        self.init_axes()
        self.draw()

    def disconnect(self):
        self.fig.canvas.mpl_disconnect(self.cid_putdot)
        self.fig.canvas.mpl_disconnect(self.cid_remove)
        self.fig.canvas.mpl_disconnect(self.cid_clear)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    # sys.exit(app.exec_())
    app.exec_()
    print(window.canvas.getx())
