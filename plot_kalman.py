import numpy as np
import pyqtgraph as pg
from PyQt6 import QtWidgets, QtCore



class PlotKalman(QtWidgets.QMainWindow):

     def __init__(self, actual, measurements, filtered, x_range, y_range, update_interval, full_plot=False):
          super(PlotKalman, self).__init__()

          self.full_plot = full_plot
          self.count = 0

          self.graphWidget = pg.PlotWidget()
          self.graphWidget.setXRange(x_range[0], x_range[1])
          self.graphWidget.setYRange(y_range[0], y_range[1])
          self.setCentralWidget(self.graphWidget)

          self.actual = actual
          self.measurements = measurements
          self.filtered = filtered

          self.actual_plot = np.array([[actual[0, 0], actual[0, 1]]])
          self.measurement_plot = np.array([[measurements[0, 0], measurements[0, 1]]])
          self.filtered_plot = np.array([[filtered[0, 0], filtered[0, 1]]])

          self.graphWidget.setBackground('k')

          self.graphWidget.addLegend(offset=(-1, 1))

          self.measurement_scatter = self.graphWidget.plot(self.measurement_plot[:, 0], self.measurement_plot[:, 1], 
                                                       pen=None, symbol='x', name='Measurement')
          
          self.filtered_line = self.graphWidget.plot(self.filtered_plot[:, 0], self.filtered_plot[:, 1], 
                                                     name='Filtered', pen='g')
          
          self.actual_line =  self.graphWidget.plot(self.actual_plot[:, 0], self.actual_plot[:, 1], 
                                                    name='Actual', pen='w')

          self.timer = QtCore.QTimer()
          self.timer.setInterval(update_interval)
          self.timer.timeout.connect(self.update_plot_data)
          self.timer.start()

     def update_plot_data(self):
          try:
               self.actual = self.actual[1:, :]
               self.filtered = self.filtered[1:, :]
               self.measurements = self.measurements[1:, :]

               self.actual_plot = np.concatenate((self.actual_plot, [self.actual[0, :]]))
               self.filtered_plot = np.concatenate((self.filtered_plot, [self.filtered[0, :]]))
               self.measurement_plot = np.concatenate((self.measurement_plot, [self.measurements[0, :]]))
               
               self.actual_line.setData(self.actual_plot[:, 0], self.actual_plot[:, 1])
               self.filtered_line.setData(self.filtered_plot[:, 0], self.filtered_plot[:, 1])
               self.measurement_scatter.setData(self.measurement_plot[:, 0], self.measurement_plot[:, 1])

               if self.count >= 50 and self.full_plot == False:
                    self.actual_plot = self.actual_plot[1:]
                    self.filtered_plot = self.filtered_plot[1:]
                    self.measurement_plot = self.measurement_plot[1:]
               
               self.count += 1

          except:
               pass
          


def animated_plot_kalman(actual, measurements, filtered, x_range=[-30,130], y_range=[-4000,500], update_interval=10, full_plot=False):
     app = QtWidgets.QApplication([])
     w = PlotKalman(actual, measurements, filtered, x_range, y_range, update_interval, full_plot)
     w.show()
     app.exec()