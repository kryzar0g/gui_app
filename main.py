import sys
from PyQt5 import QtWidgets
import pyqtgraph as pg
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QPushButton, QLineEdit
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import QIODevice,QTimer
import time
from PyQt5.QtWidgets import QFileDialog

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



        self.setWindowTitle("co2 monitoring")
        self.setGeometry(0, 0, 1500, 900)

        self.port = QSerialPort()

        # porty
        self.portNames = QtWidgets.QComboBox(self)
        self.portNames.addItems([port.portName() for port in QSerialPortInfo().availablePorts()])
        self.portNames.setMinimumHeight(30)

        self.portNames.currentIndexChanged.connect(self.index_changed)
        self.portNames.currentTextChanged.connect(self.index_changed)


        # baudrate
        self.baudRates = QtWidgets.QComboBox(self)
        self.baudRates.addItems([
            '110', '300', '600', '1200', '2400', '4800', '9600', '14400', '19200', '28800',
            '31250', '38400', '51200', '56000', '57600', '76800', '115200'])
        self.baudRates.setCurrentText('115200')
        self.baudRates.setMinimumHeight(30)
        self.baudRates.currentIndexChanged.connect(self.index_changed)
        self.baudRates.currentTextChanged.connect(self.index_changed)

        self.typ_sensoru = QtWidgets.QComboBox(self)
        self.typ_sensoru.addItems(['MH-Z19B', 'Sensirion SCD40'])
        self.typ_sensoru.currentIndexChanged.connect(self.index_changed)
        self.typ_sensoru.currentTextChanged.connect(self.index_changed)


        self.button_is_checked = False
        self.button = QPushButton("Connect")
        self.button.setFixedSize(250, 100)
        self.button.setCheckable(True)
        self.button.released.connect(self.the_button_was_released)
        self.button.setChecked(self.button_is_checked)

        self.graf = pg.PlotWidget()
        self.graf.setFixedSize(1300, 500)
        self.graf.setBackground('w')

        self.x = list(range(100))  # 100 time points
        self.y_ppm = [0] * 100  # Initialize data points for ppm

        pen_ppm = pg.mkPen(color=(255, 0, 0))

        self.data_line_ppm = self.graf.plot(self.x, self.y_ppm, pen=pen_ppm)

        self.timer = QTimer()
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()


        input = QLineEdit()
        input.setStyleSheet("background-color: white")
        font = input.font()
        font.setPointSize(10)
        input.setFont(font)
        input.setMaxLength(150)
        input.setPlaceholderText("Enter your text")
        input.setFixedSize(400, 400)
        # input.setInputMask('00.00.00.00.00.00.00.00.00.00.00.00;_')
        input.returnPressed.connect(self.return_pressed)
        input.selectionChanged.connect(self.selection_changed)
        input.textChanged.connect(self.index_changed)
        input.textEdited.connect(self.text_edited)


        self.serialData = QtWidgets.QTextEdit(self)
        self.serialData.setReadOnly(True)
        self.serialData.setFontFamily('Comic Sans MS')
        self.serialData.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.serialDataHex = QtWidgets.QTextEdit(self)
        self.serialDataHex.setReadOnly(True)
        self.serialDataHex.setFontFamily('Comic Sans MS')
        self.serialDataHex.setFixedWidth(400)
        self.serialDataHex.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.fileNameInput = QLineEdit()
        self.fileNameInput.setStyleSheet("background-color: white")
        self.fileNameInput.setPlaceholderText("soubor pro ulozeni bez pripony")
        self.fileNameInput.returnPressed.connect(self.save_file)

        # normalni layout ..
        layout1 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()
        layout4 = QHBoxLayout()

        layout1.setContentsMargins(0, 0, 0, 0)
        layout1.setSpacing(0)

        layout2.addWidget(self.portNames)
        layout2.addWidget(self.baudRates)
        layout2.addWidget(self.typ_sensoru)
        layout2.addWidget(self.fileNameInput)
        layout2.addWidget(self.button)

        layout1.addLayout(layout2)
        layout1.addLayout(layout3)

        layout3.addWidget(self.graf)

        layout3.addLayout(layout4)
        layout4.addWidget(input)
        layout4.addWidget(self.serialData)
        layout4.addWidget(self.serialDataHex)

        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)


    def index_changed(self, a):  # i je index vybraneho prvku portu
        print(a)
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        print(current_time)

    def text_changed(self, b):  # s je text vybraneho prvku portu
        print(b)

    def baudRate(self, g):
        print(g)

    def baudrateindex(self, h):
        print(h)

    def the_button_was_released(self):
        self.button_is_checked = self.button.isChecked()

        if self.button_is_checked:
            self.button.setText("Connected")
            #self.setStyleSheet("background-color: green")
            self.port.setBaudRate(self.baudRate())
            self.port.setPortName(self.portName())
            r = self.port.open(QIODevice.ReadWrite)
            if not r:
                print("Cannot open port, error")
                self.button.setChecked(False)
            else:
                print("Port is open")
                self.port.readyRead.connect(self.readFromPort)
                self.button.setText("Connected")
                self.button.setChecked(True)
                self.port.setDataTerminalReady(True)
        else:
            self.button.setText("Disconnected")
            #self.setStyleSheet("background-color: red")
            self.button.setChecked(False)
            self.port.close()
            print("Port is closed")

    def readFromPort(self):
        data = self.port.readAll().data().decode('utf-8')
        self.serialData.append(data)
        print(data)
        self.serialDataHex.append(data.encode('utf-8').hex())


    def update_plot_data(self):
        data = self.port.readLine()
        if data:
            data_str = data.data().decode().strip()
            values = data_str.split(",")

            if len(values) == 3:
                try:
                    ppm = float(values[0])

                    self.x = self.x[1:]  # Remove the first x element.
                    self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last.

                    self.y_ppm = self.y_ppm[1:]  # Remove the first ppm value.
                    self.y_ppm.append(ppm)  # Add the new ppm value

                    self.data_line_ppm.setData(self.x, self.y_ppm)

                except ValueError:
                    print("Invalid data format")
            else:
                print("Invalid data format")


    def baudRate(self):
        return int(self.baudRates.currentText())
        print(self.baudRates.currentText())

    def portName(self):
        return self.portNames.currentText()

    def return_pressed(self, i):
        print(i)

    def selection_changed(self, j):
        print(j)

    def text_changed(self, k):
        print(k)

    def text_edited(self, l):
        print(l)

    def save_file(self):
        file_name = self.fileNameInput.text()
        if file_name:
            directory = QFileDialog.getExistingDirectory(self, "Select Location")
            if directory:
                file_path = directory + "/" + file_name + ".csv"  # Modify the file path generation as needed
                try:
                    with open(file_path, "w") as file:
                        file.write(self.serialData.toPlainText())
                    print("File saved:", file_path)
                except IOError as e:
                    print("Error saving file:", str(e))


app = QApplication(sys.argv)

window = MainWindow()
window.show()

sys.exit(app.exec())
