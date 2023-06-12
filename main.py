import sys
from PyQt5 import QtWidgets
import pyqtgraph as pg
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,QPushButton, QLineEdit
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import QIODevice
import time
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtCore
from PyQt5.QtCore import Qt


class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)

        palette = self.palette()
        palette.setColor(QPalette.Window, QColor(color))
        self.setPalette(palette)



class MainWindow(QMainWindow):

    def update_plot_data(self):
        if self.typ_grafu.currentText() == "ppm":
            self.x = self.x[1:]  # Remove the first element
            self.x.append(self.x[-1] + 1)  # Add a new value 1 higher than the last
            self.y = self.y[1:]  # Remove the first element
            self.y.append(self.ppm)  # Add a new data point
            self.data_line.setData(self.x, self.y)

        if self.typ_grafu.currentText() == "temperature":
            self.x = self.x[1:]
            self.x.append(self.x[-1] + 1)
            self.y = self.y[1:]
            self.y.append(self.temp)
            self.data_line.setData(self.x, self.y)

        if self.typ_grafu.currentText() == "humidity":
            self.x = self.x[1:]
            self.x.append(self.x[-1] + 1)
            self.y = self.y[1:]
            self.y.append(self.hum)
            self.data_line.setData(self.x, self.y)



    def cteni_dat(self):
        data = self.port.readAll().data().decode('utf-8').strip()
        self.serialData.append(data)
        self.serialDataHex.append(data.encode('utf-8').hex())
        print(data)

        hodnoty = []  # Initialize hodnoty as an empty list

        if data:
            hodnoty = data.split(";")

        if len(hodnoty) == 3:
            ppm = float(hodnoty[0])
            temp = float(hodnoty[1])
            hum = float(hodnoty[2].split("\r\n")[0])  # Extract numeric part and convert to float
            print("ppm: ", ppm)
            print("temp: ", temp)
            print("hum: ", hum)

            self.ppm = ppm
            self.temp = temp
            self.hum = hum
            # Update ppm value

            self.update_plot_data()  # Call update_plot_data to update the plot

    def __init__(self):
        super(MainWindow, self).__init__()

        #app.setStyle('Fusion')
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, Qt.white)
        dark_palette.setColor(QPalette.Base, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, Qt.white)
        dark_palette.setColor(QPalette.ToolTipText, Qt.white)
        dark_palette.setColor(QPalette.Text, Qt.white)
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, Qt.white)
        dark_palette.setColor(QPalette.BrightText, Qt.red)
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(dark_palette)





        self.setWindowTitle("CO2 monitor_Project 2 - Zaruba Krystof")


        self.port = QSerialPort()

        # porty
        self.portNames = QtWidgets.QComboBox(self)
        self.portNames.addItems([port.portName() for port in QSerialPortInfo().availablePorts()])
        #self.portNames.setMinimumHeight(30)
        self.portNames.setStyleSheet("background-color: black")

        self.portNames.currentIndexChanged.connect(self.index_changed)
        self.portNames.currentTextChanged.connect(self.index_changed)

        self.ppm=0
        self.temp=0
        self.hum=0

        # baudrate
        self.baudRates = QtWidgets.QComboBox(self)
        self.baudRates.addItems([
            '110', '300', '600', '1200', '2400', '4800', '9600', '14400', '19200', '28800',
            '31250', '38400', '51200', '56000', '57600', '76800', '115200'])
        self.baudRates.setCurrentText('115200')
        #self.baudRates.setMinimumHeight(30)
        self.baudRates.setStyleSheet("background-color: black")
        self.baudRates.currentIndexChanged.connect(self.index_changed)
        self.baudRates.currentTextChanged.connect(self.index_changed)

        self.button_is_checked = False
        self.button = QPushButton("Connect")
        #self.button.setFixedSize(250, 100)
        self.button.setCheckable(True)
        self.button.setStyleSheet("background-color: black")
        self.button.released.connect(self.the_button_was_released)
        self.button.setChecked(self.button_is_checked)

        self.typ_grafu = QtWidgets.QComboBox(self)
        self.typ_grafu.addItems(['ppm', 'temperature', 'humidity'])
        self.typ_grafu.setStyleSheet("background-color: black")
        self.typ_grafu.currentTextChanged.connect(self.index_changed)
        self.typ_grafu.currentIndexChanged.connect(self.index_changed)



        self.graf = pg.PlotWidget()
        self.setCentralWidget(self.graf)
        self.graf.showGrid(x=True, y=True)
        self.x = list(range(1000))  # 100 time points
        self.y = [0] * 1000  # 100 data points

        self.graf.setBackground('k')

        pen = pg.mkPen(color=(215, 51, 112))
        self.data_line = self.graf.plot(self.x, self.y, pen=pen)

        self.timer = QtCore.QTimer()
        self.timer.setInterval(10)
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        self.serialData = QtWidgets.QTextEdit(self)
        self.serialData.setReadOnly(True)
        self.serialData.setFontFamily('Calibri')
        self.serialData.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.serialDataHex = QtWidgets.QTextEdit(self)
        self.serialDataHex.setReadOnly(True)
        self.serialDataHex.setFontFamily('Calibri')
        self.serialDataHex.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        self.fileNameInput = QLineEdit()
        self.fileNameInput.setStyleSheet("background-color: black")
        self.fileNameInput.setPlaceholderText("nazev souboru k ulozeni ve formatu .csv")
        self.fileNameInput.returnPressed.connect(self.save_file)

        # normalni layout ..
        layout1 = QVBoxLayout()
        layout2 = QHBoxLayout()
        layout3 = QVBoxLayout()
        layout4 = QHBoxLayout()

        layout1.setContentsMargins(0, 0, 0, 0)
        layout1.setSpacing(0)

        layout2.addWidget(self.portNames)
        layout2.addWidget(self.baudRates)
        layout2.addWidget(self.typ_grafu)
        layout2.addWidget(self.fileNameInput)
        layout2.addWidget(self.button)

        layout1.addLayout(layout2)
        layout1.addLayout(layout3)

        layout3.addWidget(self.graf)

        layout3.addLayout(layout4)
        layout4.addWidget(self.serialData)
        layout4.addWidget(self.serialDataHex)

        widget = QWidget()
        widget.setLayout(layout1)
        self.setCentralWidget(widget)


    def index_changed(self, a):  # i je index vybraneho prvku portu
        print(a)
        t = time.localtime()
        current_time = time.strftime("%H:%M:%S", t)
        #print(current_time)

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
            self.port.setBaudRate(self.baudRate())
            self.port.setPortName(self.portName())
            r = self.port.open(QIODevice.ReadWrite)
            if not r:
                print("Cannot open port, error")
                self.button.setChecked(False)
                self.button.setText("Cannot open port, error")
            else:
                print("Port is open")
                self.port.readyRead.connect(self.cteni_dat)
                self.button.setText("Connected")
                self.button.setChecked(True)
                self.port.setDataTerminalReady(True)
        else:
            self.button.setText("Disconnected")
            self.button.setChecked(False)
            self.port.close()
            print("Port is closed")

    def baudRate(self):
        return int(self.baudRates.currentText())
        print(self.baudRates.currentText())

    def portName(self):
        return self.portNames.currentText()


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
