import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QDockWidget, QLineEdit, \
    QHBoxLayout, QLabel
from PyQt5.QtGui import QPainter, QPen, QColor, QDoubleValidator
from PyQt5.QtCore import Qt, QPoint
from PyQt5.uic.properties import QtGui
import math


class CoordinatePlaneWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.points = []
        self.ref_points = []
        self.flag_paint = 0
        self.flag_ref = 0
        self.corner = 0

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor(0, 0, 0))
        painter.setPen(pen)

        # Рисование оси X
        painter.drawLine(0, self.height() // 2, self.width(), self.height() // 2)
        painter.drawText(self.width() - 20, self.height() // 2 - 10, "X")

        # Рисование оси Y
        painter.drawLine(self.width() // 2, 0, self.width() // 2, self.height())
        painter.drawText(self.width() // 2 + 10, 20, "Y")

        # Настройка пера для рисования точек
        pen.setWidth(2)
        pen.setColor(QColor(255, 0, 0))
        painter.setPen(pen)

        if self.flag_paint == 1:
            pen.setWidth(2)
            pen.setColor(QColor(255, 0, 0))
            painter.setPen(pen)

            if len(self.points) > 0:
                p = self.points[len(self.points)-1]

            # Рисование точек
                for point in self.points:
                    painter.drawPoint(point)
                    painter.drawLine(p, point)
                    p = point

        if self.flag_ref == 1:
            pen.setWidth(2)
            pen.setColor(QColor(100, 0, 0))
            painter.setPen(pen)

            painter.drawPoint(self.ref_points[0])
            self.ref_points[0] = self.ref_points[1]

            if len(self.ref_points) > 0:
                p = self.ref_points[len(self.ref_points)-1]

                for point in self.ref_points:
                    painter.drawPoint(point)
                    painter.drawLine(p, point)
                    p = point
            self.ref_points.clear()

    def add_point(self, x, y):
        self.flag_paint = 1
        widget_width = self.width()
        widget_height = self.height()
        center_x = widget_width // 2
        center_y = widget_height // 2
        point_x = center_x + 10*x
        point_y = center_y - 10*y
        point = QPoint(point_x, point_y)
        self.points.append(point)
        self.update()

    def ref_point(self, x, y):
        self.flag_ref = 1
        widget_width = self.width()
        widget_height = self.height()
        center_x = widget_width // 2
        center_y = widget_height // 2
        point_x = center_x + 10 * x
        point_y = center_y - 10 * y
        point = QPoint(point_x, point_y)
        self.ref_points.append(point)
        self.update()

    def clear_paint(self):
        self.flag_paint = 0
        self.flag_ref = 0
        print(1)
        self.update()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Создание виджета координатной плоскости
        self.plane_widget = CoordinatePlaneWidget()
        self.setCentralWidget(self.plane_widget)

        x_label = QLabel("X-координата:")
        y_label = QLabel("Y-координата:")
        func_label = QLabel("Координата точки поворота:")
        corner_label = QLabel("Угол поворота вокруг точки:")

        self.coordinates_x = QLineEdit("0", self)
        self.coordinates_y = QLineEdit("0", self)
        self.corner = QLineEdit("0", self)
        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.StandardNotation)
        self.coordinates_x.setValidator(validator)
        self.coordinates_y.setValidator(validator)
        self.corner.setValidator(validator)

        # Создание кнопок для изменения размера окна
        increase_button = QPushButton("Нарисовать объект", self)
        increase_button.clicked.connect(self.increase_size)

        clear_button = QPushButton("Очистить поле", self)
        clear_button.clicked.connect(self.clear)

        ref_button = QPushButton("Повернуть объект", self)
        ref_button.clicked.connect(self.ref_object)

        main_layout = QVBoxLayout()
        first_layout = QHBoxLayout()
        twelve_layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        left_layout.addWidget(x_label)
        left_layout.addWidget(y_label)
        right_layout.addWidget(self.coordinates_x)
        right_layout.addWidget(self.coordinates_y)

        first_layout.addLayout(left_layout)
        first_layout.addLayout(right_layout)

        main_layout.addWidget(func_label)
        main_layout.addLayout(first_layout)

        main_layout.addWidget(corner_label)
        main_layout.addWidget(self.corner)
        main_layout.addLayout(twelve_layout)
        main_layout.addWidget(increase_button)
        main_layout.addWidget(clear_button)
        main_layout.addWidget(ref_button)

        # Создание виджета для размещения кнопок
        button_widget = QWidget()
        button_widget.setLayout(main_layout)

        # Создание бокового виджета и установка виджета с кнопками в него
        dock_widget = QDockWidget("Buttons", self)
        dock_widget.setWidget(button_widget)

        # Добавление бокового виджета в правую боковую панель
        self.addDockWidget(Qt.LeftDockWidgetArea, dock_widget)

        self.setWindowTitle("Координатная плоскость")
        self.setGeometry(0, 0, 3*400, 3*300)

        self.show()

    def increase_size(self):
        p = [[4, 2], [-1, 5], [-4, 2], [-3, -4], [2, -6], [5, -2]]
        for i in p:
            self.plane_widget.add_point(i[0], i[1])

    def ref_object(self):
        p = [[4, 2], [-1, 5], [-4, 2], [-3, -4], [2, -6], [5, -2]]
        x0 = int(self.coordinates_x.text())
        y0 = int(self.coordinates_y.text())
        a = (int(self.corner.text()) * math.pi)/180

        self.plane_widget.ref_point(x0, y0)

        for i in p:
            x_ = round(i[0]*math.cos(a)-i[1]*math.sin(a)-x0*(math.cos(a) - 1) + y0*math.sin(a))
            y_ = round(i[0]*math.sin(a)+i[1]*math.cos(a)-x0*(math.cos(a) - 1)-y0*math.sin(a))
            self.plane_widget.ref_point(x_, y_)

    def clear(self):
        self.plane_widget.clear_paint()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())