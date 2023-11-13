import sys
import calculation
import numpy as np
from PySide6.QtCore import (QCoreApplication, QPoint, QRect, Qt)
from PySide6.QtGui import (QBrush, QPen, QPolygon, QPainter)
from PySide6.QtWidgets import (QApplication, QFrame, QLineEdit, QLabel, QToolButton, QWidget, QVBoxLayout, QHBoxLayout)


class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        if not self.objectName():
            self.setObjectName(u"Widget")
        self.resize(585, 390)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        menuWidget = QFrame(self)
        menuWidget.setFixedWidth(100)
        self.layout.addWidget(menuWidget)
        self.Menu = Menu(menuWidget)
        self.Drawframe = DrawFrame(self)
        self.layout.addWidget(self.Drawframe)
        self.Menu.TurnFigure.clicked.connect(self.rotate)
        # Привязать сигнал Menu к событию DrawFrame
        self.retranslateUi()

    def rotate(self):
        self.Drawframe.corner = [float(self.Menu.AngleY.text()),
        float(self.Menu.AngleX.text()),
        float(self.Menu.AngleZ.text())]
        # self.Drawframe.rotate()
        self.Drawframe.turn = True
        self.Drawframe.update()
    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate(
        "Widget", u"Widget", None))

        self.Menu.TurnFigure.setText(QCoreApplication.translate(
        "Widget", "Повернуть\nфигуру", None))
class Menu(QVBoxLayout):
    """Класс-контроллер содержит необходимые кнопки"""
    def __init__(self, parent):
        super().__init__(parent)
        self.setObjectName(u"Menu")
        self.AngleY = QLineEdit()
        self.AngleY.setObjectName(u"Angle")
        self.AngleY.setMaximumWidth(80)
        self.AngleY.setText("0")
        lab = QLabel("Y")
        lab.setBuddy(self.AngleY)
        self.addWidget(lab)
        self.addWidget(self.AngleY)
        self.AngleX = QLineEdit()
        self.AngleX.setObjectName(u"Angle")
        self.AngleX.setMaximumWidth(80)
        lab = QLabel("X")
        lab.setBuddy(self.AngleX)
        self.addWidget(lab)
        self.addWidget(self.AngleX)
        self.AngleX.setText("0")
        self.AngleZ = QLineEdit()
        self.AngleZ.setObjectName(u"Angle")
        self.AngleZ.setMaximumWidth(80)
        lab = QLabel("Z")
        lab.setBuddy(self.AngleZ)
        self.addWidget(lab)
        self.addWidget(self.AngleZ)
        self.AngleZ.setText("0")


        self.TurnFigure = QToolButton()
        self.TurnFigure.setObjectName(u"TurnFigure")
        self.addWidget(self.TurnFigure)


class DrawFrame(QFrame):
    """Класс модель-отображение
    Отвечает и за отрисовку и за расчеты
    """

    def __init__(self, parent):
        super().__init__(parent)
        self.turn = False
        # MONE DRAW PUT_DOT
        # self._mode = 'NONE'
        self.corner = [0,0,0]
        self.polygons = [
        [
        [0, 0, 0],
        [0, 0, 80],
        [0, 80, 80],
        [0, 80, 0],
        ],
        [
        [0, 0, 0],
        [0, 80, 0],
        [80, 80, 0],
        [80, 0, 0],
        ],
        [
        [80, 80, 80],
        [80, 80, 0],
        [80, 0, 0],
        [80, 0, 80],
        ],
        [
        [0, 0, 80],
        [0, 80, 80],
        [80, 80, 80],
        [80, 0, 80],
        ],
        [
        [0, 80, 80],
        [0, 80, 0],
        [80, 80, 0],
        [80, 80, 80],
        ],
        [
        [0, 0, 0],
        [0, 0, 80],
        [80, 0, 80],
        [80, 0, 0],
        ],
        ]
        self.setObjectName(u"Drawframe")
        self.setGeometry(QRect(70, 0, 521, 401))
        self.setStyleSheet(u"background-color: rgb(139, 184, 255);")
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.dot = [self.width()/2,
        self.height()/2]


    @property
    def corner(self):
        return self._corner


    @corner.setter
    def corner(self, new_corner):
        self._corner = new_corner
    def rotate(self):
        self.polygons = calculation.turnFigures(self.polygons,
        self.corner,
        self.width(),
        self.height())

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        painter.drawLine(self.width()/2, 0, self.width()/2, self.height()/2)
        painter.drawLine(self.width()/2, self.height()/2,
        self.width(), self.height()/2)
        painter.drawLine(0, self.height(), self.width()/2, self.height()/2)
        # Рисуем точки для фигуры
        painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        color = 0
        colors = [Qt.red, Qt.green, Qt.gray, Qt.black,
        Qt.magenta, Qt.cyan, Qt.darkYellow, Qt.white]
        if self.turn:
            self.rotate()
        self.turn = False
        to_sort = []
        for x in self.polygons:
            to_sort.append([
        float(np.mean(np.array(x)[:, 2])),
        float(np.mean(np.array(x)[:, 1])),
        float(np.mean((np.array(x)[:, 0])))
        ])
        to_sort.sort(key=lambda x: (x[0], x[1], x[2]))
        print(to_sort)
        self.polygons.sort(key=lambda x: (
        float(np.mean(np.array(x)[:, 2])),
        float(np.mean(np.array(x)[:, 1])),
        float(np.mean((np.array(x)[:, 0])))
        ))
        for polygon in self.polygons:
            painter.setPen(QPen(colors[color], 2, Qt.SolidLine))
            painter.setBrush(


            QBrush(colors[color], Qt.SolidPattern))
            pol_coord = calculation.calc_coord(polygon, self.width(),
            self.height())
            points = QPolygon([
            QPoint(coord[0], coord[1]) for coord in pol_coord])
            painter.drawPolygon(points)
            color += 1
        painter.setPen(QPen(Qt.green, 2, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
        print(1)
        painter.end()

if __name__ == "__main__":
    app = QApplication([])
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec())