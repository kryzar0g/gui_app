import sys
import math
import os
from random import randint
import re
from PyQt5 import QtWidgets, QtCore, QtGui
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel, QCheckBox, QPushButton, QComboBox, QLineEdit, QToolBar, QAction
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QIcon


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("My App")
        self.setGeometry(0, 0, 1500, 900)

        # text s podkladem porty ..
        """textik1 = QLabel("Port ???")
        textik1.setStyleSheet("background-color: red")
        font = textik1.font()
        font.setPointSize(30)
        textik1.setFont(font)
        textik1.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)"""

        vyberportu = QComboBox()
        vyberportu.setStyleSheet("background-color: red")
        vyberportu.addItem("COM1")
        vyberportu.addItem("COM2")
        vyberportu.addItem("COM3")
        vyberportu.addItem("COM4")
        vyberportu.addItem("COM5")

        vyberportu.currentIndexChanged.connect(self.index_changed)


        vyberportu.currentTextChanged.connect(self.text_changed)


        textik2 = QLabel("Baudrate ???")
        textik2.setStyleSheet("background-color: green")
        font = textik2.font()
        font.setPointSize(30)
        textik2.setFont(font)
        textik2.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)


        """textik3 = QLabel("Connect button??")
        textik3.setStyleSheet("background-color: blue")
        font = textik3.font()
        font.setPointSize(30)
        textik3.setFont(font)
        textik3.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)"""

        self.button_is_checked = True
        self.button = QPushButton("Connect")
        self.button.setFixedSize(250, 100)
        self.button.setCheckable(True)
        self.button.released.connect(self.the_button_was_released)
        self.button.setChecked(self.button_is_checked)


        self.graf = pg.PlotWidget()
        self.graf.setFixedSize(1300, 500)
        self.graf.setBackground('w')

        self.x = list(range(100))  # 100 time points
        self.y = [randint(0, 100) for _ in range(100)]  # 100 data points

        pen = pg.mkPen(color=(255, 0, 0))
        self.data_line = self.graf.plot(self.x, self.y, pen=pen)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()


        """textik4 = QLabel("graph???")
        textik4.setStyleSheet("background-color: purple")
        font = textik4.font()
        font.setPointSize(30)
        textik4.setFont(font)
        textik4.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)"""

        """textik5 = QLabel("input???")
        textik5.setStyleSheet("background-color: yellow")
        font = textik5.font()
        font.setPointSize(30)
        textik5.setFont(font)
        textik5.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)"""


        input=QLineEdit()
        input.setStyleSheet("background-color: white")
        font = input.font()
        font.setPointSize(10)
        input.setFont(font)
        input.setMaxLength(150)
        input.setPlaceholderText("Enter your text")
        input.setFixedSize(500, 400)
        #input.setInputMask('00.00.00.00.00.00.00.00.00.00.00.00;_')


        """input.returnPressed.connect(self.return_pressed)
        input.selectionChanged.connect(self.selection_changed)
        input.textChanged.connect(self.text_changed)
        input.textEdited.connect(self.text_edited)"""


        textik6 = QLabel("output")
        textik6.setStyleSheet("background-color: orange")
        font = textik6.font()
        font.setPointSize(30)
        textik6.setFont(font)
        textik6.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        # toolbar ..
        """toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)
        button_action = QAction("Your button", self)
        button_action.setStatusTip("This is your button")
        button_action.triggered.connect(self.onMyToolBarButtonClick)
        toolbar.addAction(button_action)"""


        # grid layout ..
        """ layout = QGridLayout()
        
        layout.addWidget(Color('red'), 0, 0)
        layout.addWidget(Color('green'), 1, 0)
        layout.addWidget(Color('blue'), 0, 1)
        layout.addWidget(Color('purple'), 1, 1)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)"""

        # normalni layout ..
        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()
        layout4 = QHBoxLayout()

        layout1.setContentsMargins(0, 0, 0, 0)
        layout1.setSpacing(0)

        layout2.addWidget(vyberportu)
        layout2.addWidget(textik2)
        layout2.addWidget(self.button)

        layout1.addLayout(layout2)
        layout1.addLayout(layout3)

        layout3.addWidget(self.graf)

        layout3.addLayout(layout4)
        layout4.addWidget(input)
        layout4.addWidget(textik6)

        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)



    def index_changed(self, a): # i je index vybraneho prvku portu
        print(a)

    def text_changed(self, b): # s je text vybraneho prvku portu
        print(b)

    """def return_pressed(self):
        print("Return pressed!")
        self.centralWidget().setText("BOOM!")"""

    """def selection_changed(self):
        print("Selection changed")
        print(self.centralWidget().selectedText())"""

    """def text_changed(self, c):
        print("Text changed...")
        print(c)"""

    """def text_edited(self, d):
        print("Text edited...")
        print(d)"""

    def onMyToolBarButtonClick(self, e):
        print("click", e)

    def the_button_was_released(self):
        self.button_is_checked = self.button.isChecked()

        print(self.button_is_checked)
        if self.button_is_checked:
            self.button.setText("Connected")
            self.setStyleSheet("background-color: green")
        else:
            self.button.setText("Disconected")
            self.setStyleSheet("background-color: red")

    def update_plot_data(self):
        self.x = self.x[1:]  # Remove the first y element.
        self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

        self.y = self.y[1:]  # Remove the first
        self.y.append(randint(0, 100))  # Add a new random value.

        self.data_line.setData(self.x, self.y)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()