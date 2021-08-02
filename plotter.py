from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QMessageBox, QLabel, QMainWindow, QStyle, QDesktopWidget, QDialog, QHBoxLayout, QVBoxLayout, QGroupBox, QTextEdit
from PySide2.QtGui import QIcon, QPixmap, QGuiApplication, QFont
from PySide2.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
import numpy as np
import sys
import re
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)


class Window(QWidget):
    def __init__(self):
        super().__init__()

        # set the valid operators and inputs
        self.replacements = {
            '^': '**'
        }
        self.allowedWords = [
            'x'
        ]

        # set the window title
        self.setWindowTitle("Function Plotter")
        # set the size of the window
        self.setGeometry(600, 600, 600, 600)
        # center the main window
        self.centerMainWindow()
        # set the icon of the program
        self.setIcon()

        # initialize the group box that will contain the layout of the program
        self.createLayout()
        # set the layout of the group box to a vbox layout
        vbox = QVBoxLayout()
        self.groupBox.setLayout(vbox)
        # set the layout of the vbox that contains the group box to hbox
        hbox = QHBoxLayout()
        hbox.addWidget(self.groupBox)
        self.setLayout(hbox)

        # set the text boxes of the equation & minX & maxX
        self.setTextBoxes(vbox)
        # initialize a canvas and set it to a figure
        self.setCanvas(vbox)
        # initialize the plot button  and connect it to the plot function
        self.setButton(vbox)

    # center the main window
    def centerMainWindow(self):
        qRect = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qRect.moveCenter(centerPoint)
        self.move(qRect.topLeft())

    # set the icon of the program
    def setIcon(self):
        appIcon = QIcon("icon.png")
        self.setWindowIcon(appIcon)

    # set the text boxes of the equation & minX & maxX
    def setTextBoxes(self, vbox):
        self.equation = QTextEdit(self)
        self.equation.setFont(QFont('Sanserif', 13))
        self.equation.setPlaceholderText("EQUATION")
        vbox.addWidget(self.equation)

        hbox = QHBoxLayout()

        self.minInput = QTextEdit(self)
        self.minInput.setFont(QFont('Sanserif', 13))
        self.minInput.setPlaceholderText("MINIMUM X")
        hbox.addWidget(self.minInput)

        self.maxInput = QTextEdit(self)
        self.maxInput.setFont(QFont('Sanserif', 13))
        self.maxInput.setPlaceholderText("MAXIMUM X")
        hbox.addWidget(self.maxInput)

        vbox.addLayout(hbox)

    # initialize the group box that will contain the layout of the program
    def createLayout(self):
        self.groupBox = QGroupBox()
        self.groupBox.setFont(QFont("Sanserif", 13))

    # initialize a canvas and set it to a figure
    def setCanvas(self, vbox):
        fig = plt.figure(figsize=(10, 5))
        self.canvas = FigureCanvas(fig)
        vbox.addWidget(self.canvas)
    # plot the input equation of the user using matplotlib after checking if the input is valid and secure

    def plot(self):
        if re.match("(([0-9]{1,}[*|^|\/|+|-][xX])|[xX]|[0-9]{1,}|[*|^|\/|+|-]|\s)+$", self.equation.toPlainText(), flags=0):
            pass
        else:
            QMessageBox.critical(
                self, "Error", "The equation you entered doesn't have the required format! eg: 5*x^2+6*x", QMessageBox.Ok)
            return
        if re.match("^-?[0-9]+$", self.maxInput.toPlainText(), flags=0):
            pass
        else:
            QMessageBox.critical(
                self, "Error", "The Maximum value of x has to be a number!", QMessageBox.Ok)
            return
        if re.match("^-?[0-9]+$", self.minInput.toPlainText(), flags=0):
            pass
        else:
            QMessageBox.critical(
                self, "Error", "The Minimum value of x has to be a number!", QMessageBox.Ok)
            return
        if int(self.minInput.toPlainText()) > int(self.maxInput.toPlainText()):
            QMessageBox.critical(
                self, "Error", "The Minimum value of x can't be greater than the maximum value of x !", QMessageBox.Ok)
            return
        # matplotlib CODE
        plt.clf()
        self.ax = self.canvas.figure.subplots()
        self.x = np.linspace(int(self.minInput.toPlainText()),
                             int(self.maxInput.toPlainText()), 100)
        self.y = self.strToEq(self.equation.toPlainText())(self.x)

        self.ax.plot(self.x, self.y)

        self.ax.set(
            title="f(x)="+self.equation.toPlainText())
        self.ax.grid()
        self.canvas.draw()
        return

    # initialize the plot button  and connect it to the plot function
    def setButton(self, vbox):
        self.plotButton = QPushButton("Plot", self)
        vbox.addWidget(self.plotButton)
        self.plotButton.clicked.connect(self.plot)

    # convert the input equation to an understandable code
    def strToEq(self, string):
        # find all words and check if all are allowed:
        for word in re.findall('[a-zA-Z_]+', string):
            if word not in self.allowedWords:
                raise ValueError(
                    '"{}" is forbidden to use in math expression'.format(word)
                )

        for old, new in self.replacements.items():
            string = string.replace(old, new)

        def func(x):
            return eval(string)

        return func


if __name__ == '__main__':
    myapp = QApplication(sys.argv)
    window = Window()
    window.show()

    myapp.exec_()
    sys.exit()
