import os
from pathlib import Path
import sys

from calculus import *
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import (QFile, QCoreApplication, QDate, QDateTime, QLocale, QMetaObject, QObject, QPoint, QRect,
                            QSize, QTime, QUrl, Qt, Signal)

from PySide6.QtGui import (QBrush, QPen, QPolygon, QColor, QConicalGradient, QCursor,
                           QFont, QFontDatabase, QGradient, QIcon,
                           QImage, QKeySequence, QLinearGradient, QPainter, QPalette, QPixmap, QRadialGradient,
                           QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QLineEdit, QSizePolicy, QTextEdit, QToolButton, QWidget,
                               QVBoxLayout, QHBoxLayout)


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

        self.Menu.DrawFigure.clicked.connect(self.drawing)
        self.retranslateUi()

    def drawing(self):
        draw_res = self.Drawframe.drawing()
        if draw_res:
            self.Menu.LogText.setPlainText(draw_res)
        else:
            self.Menu.LogText.setPlainText('')

    def retranslateUi(self):
        self.setWindowTitle(QCoreApplication.translate("Widget", u"Widget", None))
        self.Menu.DrawFigure.setText(QCoreApplication.translate("Widget", "Нарисовать\nкривую Безье", None))


class Menu(QVBoxLayout):
    def __init__(self, parent):
        super().__init__(parent)

        self.setObjectName(u"Menu")

        self.DrawFigure = QToolButton()
        self.DrawFigure.setObjectName(u"DrawFigure")
        self.DrawFigure.setGeometry(QRect(0, 200, 71, 211))
        self.addWidget(self.DrawFigure)

        self.log_widget = QWidget()
        self.log_widget.setObjectName(u"LogWiget")
        self.log_widget.setFixedHeight(200)

        self.LogText = QTextEdit(self.log_widget)
        self.LogText.setObjectName(u"LogText")
        self.addWidget(self.log_widget)


class DrawFrame(QFrame):
    def __init__(self, parent):
        super().__init__(parent)

        self._mode = 'NONE'

        self.figure = []
        self.bezier = []
        self.setObjectName(u"Drawframe")
        self.setGeometry(QRect(70, 0, 521, 401))
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)

    @property
    def bezier(self):
        return self._bezier

    @bezier.setter
    def bezier(self, new_bezier):
        self._bezier = new_bezier

    @property
    def mode(self):
        return self._mode

    @mode.setter
    def mode(self, new_mode):
        self._mode = new_mode

    @property
    def figure(self):
        return self._figure

    @figure.setter
    def figure(self, new_figure):
        self._figure = new_figure

    def drawing(self):
        if self.mode != 'DRAW':
            self.figure = []
            self.mode = 'DRAW'
        else:
            self.mode = 'NONE'
            if len(self.figure) < 3:
                self.update()
                return 'Должно быть\nминимум 3\nточки'
            self.bezier = get_bezier(self.figure)

        self.update()

    def mousePressEvent(self, QMouseEvent):
        if self.mode == 'DRAW':
            self.figure.append([QMouseEvent.position().x(), QMouseEvent.position().y()])

        self.update()

    def paintEvent(self, event):

        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.black, Qt.SolidPattern))
        painter.drawLine(self.width() / 2, 0, self.width() / 2, self.height())
        painter.drawLine(0, self.height() / 2, self.width(), self.height() / 2)

        if self.mode != 'DRAW':
                if len(self.figure) > 2:
                    points = [
                        QPoint(coord[0], coord[1]) for coord in self.figure]
                    painter.drawPolyline(points)


        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.red, Qt.SolidPattern))

        for point in self.figure:
            painter.drawEllipse(point[0], point[1], 5, 5)

        if len(self.figure) > 2 and self.mode == 'NONE':
            painter.setPen(QPen(Qt.green, 2, Qt.SolidLine))
            painter.setBrush(QBrush(Qt.green, Qt.SolidPattern))
            points = [QPoint(coord[0], coord[1]) for coord in self.bezier]
            painter.drawPolyline(points)

        painter.end()


if __name__ == "__main__":
    app = QApplication([])
    widget = MainWidget()
    widget.show()
    sys.exit(app.exec())
