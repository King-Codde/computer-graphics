import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QSlider, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import Qt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class BilinearSurfaceWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Bilinear Surface')
        self.setGeometry(100, 100, 800, 600)

        self.fig = plt.figure()
        self.canvas = FigureCanvas(self.fig)
        self.setCentralWidget(self.canvas)

        self.slider_x = QSlider(Qt.Horizontal, self)
        self.slider_x.setMinimum(0)
        self.slider_x.setMaximum(360)
        self.slider_x.setValue(45)
        self.slider_x.setGeometry(50, 50, 200, 30)
        self.slider_x.valueChanged.connect(self.rotate_surface)

        self.slider_y = QSlider(Qt.Horizontal, self)
        self.slider_y.setMinimum(0)
        self.slider_y.setMaximum(360)
        self.slider_y.setValue(45)
        self.slider_y.setGeometry(50, 100, 200, 30)
        self.slider_y.valueChanged.connect(self.rotate_surface)

        self.label_p1 = QLabel("Point 1:", self)
        self.label_p1.setGeometry(50, 150, 50, 30)
        self.line_edit_p1 = QLineEdit(self)
        self.line_edit_p1.setGeometry(100, 150, 100, 30)

        self.label_p2 = QLabel("Point 2:", self)
        self.label_p2.setGeometry(50, 200, 50, 30)
        self.line_edit_p2 = QLineEdit(self)
        self.line_edit_p2.setGeometry(100, 200, 100, 30)

        self.label_p3 = QLabel("Point 3:", self)
        self.label_p3.setGeometry(50, 250, 50, 30)
        self.line_edit_p3 = QLineEdit(self)
        self.line_edit_p3.setGeometry(100, 250, 100, 30)

        self.label_p4 = QLabel("Point 4:", self)
        self.label_p4.setGeometry(50, 300, 50, 30)
        self.line_edit_p4 = QLineEdit(self)
        self.line_edit_p4.setGeometry(100, 300, 100, 30)

        self.button_update = QPushButton("Update", self)
        self.button_update.setGeometry(50, 350, 100, 30)
        self.button_update.clicked.connect(self.update_points)

        # Default points
        self.points = {
            'p1': np.array([0, 0, 0]),
            'p2': np.array([1, 0, 0]),
            'p3': np.array([0, 1, 0]),
            'p4': np.array([1, 1, 0])
        }

        self.update_line_edit_values()
        self.rotate_surface()

    def update_points(self):
        self.points['p1'] = np.array([float(val) for val in self.line_edit_p1.text().split(',')])
        self.points['p2'] = np.array([float(val) for val in self.line_edit_p2.text().split(',')])
        self.points['p3'] = np.array([float(val) for val in self.line_edit_p3.text().split(',')])
        self.points['p4'] = np.array([float(val) for val in self.line_edit_p4.text().split(',')])
        self.rotate_surface()

    def update_line_edit_values(self):
        self.line_edit_p1.setText(','.join(str(val) for val in self.points['p1']))
        self.line_edit_p2.setText(','.join(str(val) for val in self.points['p2']))
        self.line_edit_p3.setText(','.join(str(val) for val in self.points['p3']))
        self.line_edit_p4.setText(','.join(str(val) for val in self.points['p4']))

    def rotate_surface(self):
        angle_x = (self.slider_x.value())
        angle_y = (self.slider_y.value())

        print(angle_x, angle_y)

        u, v = np.meshgrid(np.linspace(0, 1, 20), np.linspace(0, 1, 20))
        p1 = self.points['p1']
        p2 = self.points['p2']
        p3 = self.points['p3']
        p4 = self.points['p4']

        x = (1 - u) * (1 - v) * p1[0] + u * (1 - v) * p2[0] + (1 - u) * v * p3[0] + u * v * p4[0]
        y = (1 - u) * (1 - v) * p1[1] + u * (1 - v) * p2[1] + (1 - u) * v * p3[1] + u * v * p4[1]
        z = (1 - u) * (1 - v) * p1[2] + u * (1 - v) * p2[2] + (1 - u) * v * p3[2] + u * v * p4[2]

        ax = self.fig.add_subplot(111, projection='3d')
        ax.clear()
        ax.plot_surface(x, y, z, cmap='viridis')

        ax.elev = angle_x
        ax.azim = angle_y

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')

        self.canvas.draw()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = BilinearSurfaceWindow()
    window.show()
    sys.exit(app.exec_())