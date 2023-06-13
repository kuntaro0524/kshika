import sys
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMainWindow, QApplication, QVBoxLayout, QLabel, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class HeatmapWindow(QMainWindow):
    def __init__(self, data, title='Heatmap'):
        super().__init__()
        self.data = data

        self.figure = plt.figure()
        self.ax = self.figure.add_subplot(111)

        self.heatmap = sns.heatmap(self.data, ax=self.ax)

        self.heatmap.set_yticklabels([])
        self.heatmap.set_xticklabels([])

        self.canvas = FigureCanvas(self.figure)
        self.canvas.mpl_connect('button_press_event', self.on_click)

        self.setCentralWidget(self.canvas)
        self.setWindowTitle(title)

    def on_click(self, event):
        #if event.inaxes == self.heatmap.ax:
        if event.inaxes == self.ax:
            x, y = int(event.xdata + 0.5), int(event.ydata + 0.5)
            print(f'({x}, {y}) value: {self.data[y][x]}')

if __name__ == '__main__':
    data = np.random.rand(10, 10)
    app = QApplication(sys.argv)
    window = HeatmapWindow(data)
    window.show()
    sys.exit(app.exec_())
