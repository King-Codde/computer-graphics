import sys
import random
from PySide6.QtCore import Slot
from PySide6.QtWidgets import (QApplication,QHBoxLayout, QMainWindow,QVBoxLayout,QWidget, QPushButton)
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure


class ApplicationWindow(QMainWindow):
    def __init__(self, parent=None):
        self.INSIDE = 0 # 0000
        self.LEFT = 8 # 1000
        self.RIGHT = 4 # 0100
        self.BOTTOM = 2 # 0010
        self.TOP = 1 # 0001

        self.x_max = 5
        self.y_max = 5
        self.x_min = 1
        self.y_min = 1

        QMainWindow.__init__(self, parent)

        self.column_names = ["X", "Y", "Z"]
        # Central widget
        self._main = QWidget()
        self.setCentralWidget(self._main)


        # Main menu bar
        self.menu = self.menuBar()

        # Figure (Left)
        self.fig = Figure(figsize=(50, 50))
        self.canvas = FigureCanvas(self.fig)

        self.button = QPushButton(
        text='Сгенерировать и отрисовать отрезки')

        self.result = QPushButton(
        text='Выделить пересечение')

        # Right layout
        rlayout = QVBoxLayout()
        rlayout.setContentsMargins(1, 1, 1, 1)
        rlayout.addWidget(self.button)
        rlayout.addWidget(self.result
        )
        rlayout.setContentsMargins(1, 1, 1, 1)
        # Left layout
        llayout = QVBoxLayout()
        llayout.addWidget(self.canvas, 88)
        # Main layout
        layout = QHBoxLayout(self._main)
        layout.addLayout(llayout, 70)

        layout.addLayout(rlayout, 30)

        self.button.clicked.connect(self.generate_lines)
        self.result.clicked.connect(self.draw_intersection)

        self.set_canvas_table_configuration()

    def set_canvas_table_configuration(self, data=[]):
        self.fig.set_canvas(self.canvas)
        self._ax = self.canvas.figure.add_subplot()


    @Slot()
    def generate_lines(self):
        self.lines = []
        for i in range(5):
            self.lines.append([
                [random.randrange(-10, 10), random.randrange(-10, 10)],
                [random.randrange(-10, 10), random.randrange(-10, 10)]])
        self.lines = np.array(self.lines)
        # print (self.lines)
        self.draw_lines()

    @Slot()
    def draw_intersection(self):
        self._ax.clear()

        self.draw_lines()
        intersect = []
        for i in self.lines:
            print(i)
            inter = self.check_line(i)
            if inter:
                intersect.append(inter)
        intersect = np.array(intersect)
        for i in intersect:
            self._ax.plot(i[:, 0], i[:, 1], 'g')

        self.fig.set_canvas(self.canvas)

        self.canvas.draw()

    def draw_lines(self):
        self._ax.clear()
        for i in self.lines:
            self._ax.plot(i[:, 0], i[:, 1], 'r')
        self._ax.plot([1, 1, 5, 5, 1], [1, 5, 5, 1, 1], 'k')
        self._ax.grid(True, which='both')
        self._ax.set_ylim(-10, 10)


        self._ax.set_xlim(-10, 10)
        self.fig.set_canvas(self.canvas)

        self.canvas.draw()

    def get_code(self, x, y):
    # Определим код точки
        code = self.INSIDE
        if x < self.x_min:
            code |= self.LEFT
        elif x > self.x_max:
            code |= self.RIGHT
        if y < self.y_min:
            code |= self.BOTTOM
        elif y > self.y_max:
            code |= self.TOP
        return code

    def check_line(self, coord):
        code1 = self.get_code(coord[0][0], coord[0][1])
        code2 = self.get_code(coord[1][0], coord[1][1])
        x1 = coord[0][0]
        y1 = coord[0][1]

        x2 = coord[1][0]
        y2 = coord[1][1]
        accept = False

        while True:
            print('codes', code1, code2)
            # обе точки в прямоугольнике
            if code1 == 0 and code2 == 0:
                accept = True
                break

        # обе точки вне прямоугольника

            elif (code1 & code2) != 0:
                break

        # лежит частично
            else:
                x = -20
                y = -20
                if code1 != 0:
                    code_out = code1
                else:
                    code_out = code2

            if code_out & self.TOP:
                x = x1 + ((x2 - x1) / (y2 - y1)) * (self.y_max - y1)
                y = self.y_max
            # низ
            elif code_out & self.BOTTOM:

                x = x1 + ((x2 - x1) / (y2 - y1)) * (self.y_min - y1)
                y = self.y_min

            # низ право
            elif code_out & self.RIGHT:

                y = y1 + ((y2 - y1) / (x2 - x1)) * (self.x_max - x1)
                x = self.x_max
            # лево
            elif code_out & self.LEFT:

                y = y1 + ((y2 - y1) / (x2 - x1)) * (self.x_min - x1)
                x = self.x_min
            # Заменяем коды на новые
            if code_out == code1:
                x1 = x
                y1 = y
                code1 = self.get_code(x1, y1)
            else:
                x2 = x
                y2 = y
                code2 = self.get_code(x2, y2)
        if accept:
            return [[x1, y1], [x2, y2]]
        return accept


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = ApplicationWindow()
    w.setFixedSize(680, 480)
    w.show()
    app.exec()