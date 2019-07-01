import sys
import os
from PyQt5 import QtGui, QtCore, QtWidgets, Qt
import numpy as np


class pixelGrid(QtWidgets.QTableView):
    def __init__(self):
        super().__init__()
        self.activated.connect(self.onClick)

    def onClick(self):
        pass
        # currCell = self.


class FontCodeGenerator:

    def __init__(self):
        super(FontCodeGenerator, self).__init__()

        self.charDict = {}

        # --- Main Menu Window  --- #
        self.mainWindow = QtWidgets.QWidget()
        self.titleLabel = QtWidgets.QLabel("Font Code Generator for C")
        self.mainWinLayout = QtWidgets.QVBoxLayout()
        self.newButton = QtWidgets.QPushButton(text="New")
        self.loadButton = QtWidgets.QPushButton(text="Load")
        self.widthTextLayout = QtWidgets.QVBoxLayout()
        self.heightTextLayout = QtWidgets.QVBoxLayout()
        self.widthTextInput = QtWidgets.QLineEdit(text="7")
        self.heightTextInput = QtWidgets.QLineEdit(text="10")
        self.textInputLayout = QtWidgets.QHBoxLayout()

        # Set Widget Actions/Behavior
        self.newButton.clicked.connect(self.startNew)
        self.loadButton.clicked.connect(self.startLoad)

        # Build Main Window UI
        self.widthTextLayout.addWidget(QtWidgets.QLabel("Width:"))
        self.heightTextLayout.addWidget(QtWidgets.QLabel("Height:"))
        self.widthTextLayout.addWidget(self.widthTextInput)
        self.heightTextLayout.addWidget(self.heightTextInput)
        self.textInputLayout.addLayout(self.widthTextLayout)
        self.textInputLayout.addLayout(self.heightTextLayout)
        self.mainWinLayout.addWidget(self.titleLabel)
        self.mainWinLayout.addLayout(self.textInputLayout)
        self.mainWinLayout.addWidget(self.newButton)
        self.mainWinLayout.addWidget(self.loadButton)
        self.mainWindow.setLayout(self.mainWinLayout)

        # --- Drawing UI --- #
        self.drawWindow = QtWidgets.QWidget()
        self.drawWindow.resize(550, 400)
        self.hLayout = QtWidgets.QHBoxLayout()
        self.vLayout = QtWidgets.QVBoxLayout()
        self.drawLayout = QtWidgets.QVBoxLayout()
        self.pixelGrid = QtWidgets.QTableWidget()
        self.pixelGrid.horizontalHeader().setDefaultSectionSize(30)
        self.pixelGrid.verticalHeader().setDefaultSectionSize(30)
        self.pixelGrid.horizontalHeader().hide()
        self.pixelGrid.verticalHeader().hide()
        self.charList = QtWidgets.QListWidget()
        self.charList.addItems(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'])
        self.saveCharButton = QtWidgets.QPushButton(text="Save")
        self.drawButton = QtWidgets.QPushButton(text="Draw")
        self.eraseButton = QtWidgets.QPushButton(text="Erase")
        self.drawBtnLayout = QtWidgets.QHBoxLayout()

        # Set Widget Actions Behavior
        # Button Behavior
        self.saveCharButton.clicked.connect(self.startSave)
        self.drawButton.clicked.connect(self.selectDraw)
        self.eraseButton.clicked.connect(self.selectErase)
        # Pixel Grid Behavior
        self.pixelGrid.itemSelectionChanged.connect(self.onCellSelection)
        self.pixelPalette = self.pixelGrid.palette()
        self.selectDraw()
        self.pixelGridArray = np.zeros(1)
        # Char List Behavior
        self.charList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)  # Allow only selection of 1 item
        self.charList.itemClicked.connect(self.listSelect)  # Connect to listSelect function
        self.charList.setCurrentRow(0)
        self.currChar = self.charList.currentItem().text()

        # Build Drawing Window UI
        self.vLayout.addWidget(self.charList)
        self.vLayout.addWidget(self.saveCharButton)
        self.hLayout.addLayout(self.vLayout)
        self.drawLayout.addWidget(self.pixelGrid)
        self.drawBtnLayout.addWidget(self.drawButton)
        self.drawBtnLayout.addWidget(self.eraseButton)
        self.drawLayout.addLayout(self.drawBtnLayout)
        self.hLayout.addLayout(self.drawLayout)
        self.hLayout.setStretch(0, 1)
        self.hLayout.setStretch(1, 2)
        self.drawWindow.setLayout(self.hLayout)

        self.mainWindow.show()

    def startNew(self):
        print("Making new font")
        self.mainWindow.close()
        rows = int(self.heightTextInput.text())
        cols = int(self.widthTextInput.text())
        self.pixelGrid.setRowCount(rows)
        self.pixelGrid.setColumnCount(cols)
        self.pixelGridArray = np.zeros((rows, cols))
        # Allows drawing on the pixel grid
        for x in range(rows):
            for y in range(cols):
                self.pixelGrid.setItem(x, y, QtWidgets.QTableWidgetItem())
        # Initialize dictionary of font data
        for i in range(self.charList.count()):
            self.charDict.update({self.charList.item(i).text(): np.zeros((rows, cols))})
        print(self.pixelGridArray)
        self.drawWindow.show()

    def startLoad(self):
        print("Loading font")
        self.mainWindow.close()
        self.drawWindow.show()

    def startSave(self):
        print(self.pixelGridArray)

    def selectDraw(self):
        self.drawButton.setStyleSheet("background-color: #70a5fa")
        self.eraseButton.setStyleSheet("background-color: grey")
        self.pixelGrid.clearSelection()
        self.pixelPalette.setBrush(QtGui.QPalette.Highlight, QtGui.QBrush(QtGui.QColor(0, 0, 0)))
        self.pixelPalette.setBrush(QtGui.QPalette.HighlightedText, QtGui.QBrush(QtGui.QColor(0, 0, 0)))
        self.pixelGrid.setPalette(self.pixelPalette)
        self.drawMode = True

    def selectErase(self):
        self.drawButton.setStyleSheet("background-color: grey")
        self.eraseButton.setStyleSheet("background-color: #70a5fa")
        self.pixelGrid.clearSelection()
        self.pixelPalette.setBrush(QtGui.QPalette.Highlight, QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        self.pixelPalette.setBrush(QtGui.QPalette.HighlightedText, QtGui.QBrush(QtGui.QColor(255, 255, 255)))
        self.pixelGrid.setPalette(self.pixelPalette)
        self.drawMode = False

    def onCellSelection(self):
        for x in self.pixelGrid.selectedIndexes():
            if self.drawMode:
                self.pixelGridArray[x.row(), x.column()] = 1
                self.pixelGrid.item(x.row(), x.column()).setBackground(QtGui.QColor(0, 0, 0))
            else:
                self.pixelGridArray[x.row(), x.column()] = 0
                self.pixelGrid.item(x.row(), x.column()).setBackground(QtGui.QColor(255, 255, 255))

    def listSelect(self):
        # Save the current pixel grid in the dictionary
        self.charDict[self.currChar] = np.copy(self.pixelGridArray)
        self.currChar = self.charList.currentItem().text()
        print(self.charList.currentItem().text())
        self.drawFromArray(self.currChar)

    def drawFromArray(self, char):
        array = self.charDict[char]
        print(array)
        print("h")
        self.pixelGridArray = np.copy(array)
        self.pixelGrid.clearSelection()
        for x in range(array.shape[0]):
            for y in range(array.shape[1]):
                if array[x, y] == 1:
                    self.pixelGrid.item(x, y).setBackground(Qt.QColor(0, 0, 0))
                else:
                    self.pixelGrid.item(x, y).setBackground(Qt.QColor(255, 255, 255))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    program = FontCodeGenerator()
    sys.exit(app.exec_())
