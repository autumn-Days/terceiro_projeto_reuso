from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtCore import Qt

class WordCount(QtWidgets.QDialog):
    def __init__(self, parent=None):
        # Uso moderno do super() para herança
        super().__init__(parent)

        self.parent = parent
        self.initUI()
 
    def initUI(self):
        # CORREÇÃO PRINCIPAL: QtGui.QLabel -> QtWidgets.QLabel
        
        # Word count in selection
        currentLabel = QtWidgets.QLabel("Current selection", self)
        currentLabel.setStyleSheet("font-weight:bold; font-size: 15px;")

        currentWordsLabel = QtWidgets.QLabel("Words: ", self)
        currentSymbolsLabel = QtWidgets.QLabel("Symbols: ", self)
        
        self.currentWords = QtWidgets.QLabel(self)
        self.currentSymbols = QtWidgets.QLabel(self)

        # Total word/symbol count
        totalLabel = QtWidgets.QLabel("Total", self)
        totalLabel.setStyleSheet("font-weight:bold; font-size: 15px;")

        totalWordsLabel = QtWidgets.QLabel("Words: ", self)
        totalSymbolsLabel = QtWidgets.QLabel("Symbols: ", self)

        self.totalWords = QtWidgets.QLabel(self)
        self.totalSymbols = QtWidgets.QLabel(self)

        # Layout
        # CORREÇÃO: QtGui.QGridLayout -> QtWidgets.QGridLayout
        layout = QtWidgets.QGridLayout(self)

        layout.addWidget(currentLabel, 0, 0)
        
        layout.addWidget(currentWordsLabel, 1, 0)
        layout.addWidget(self.currentWords, 1, 1)

        layout.addWidget(currentSymbolsLabel, 2, 0)
        layout.addWidget(self.currentSymbols, 2, 1)

        # CORREÇÃO: QtGui.QWidget -> QtWidgets.QWidget
        spacer = QtWidgets.QWidget()
        spacer.setFixedSize(0, 5)

        layout.addWidget(spacer, 3, 0)

        layout.addWidget(totalLabel, 4, 0)

        layout.addWidget(totalWordsLabel, 5, 0)
        layout.addWidget(self.totalWords, 5, 1)

        layout.addWidget(totalSymbolsLabel, 6, 0)
        layout.addWidget(self.totalSymbols, 6, 1)

        self.setWindowTitle("Word count")
        self.setGeometry(300, 300, 200, 200)
        self.setLayout(layout)

    def getText(self):
        # O método getText permanece praticamente igual, pois manipula strings
        # e objetos do QTextEdit (que já deve estar correto no parent)

        # Pega o texto da seleção atual
        # Nota: textCursor() retorna uma cópia, então é seguro chamar selectedText()
        text = self.parent.text.textCursor().selectedText()

        # Split remove espaços em branco e conta os itens da lista
        words = str(len(text.split()))

        # Conta caracteres (incluindo espaços)
        symbols = str(len(text))

        self.currentWords.setText(words)
        self.currentSymbols.setText(symbols)

        # Pega o texto total do editor
        text = self.parent.text.toPlainText()

        words = str(len(text.split()))
        symbols = str(len(text))

        self.totalWords.setText(words)
        self.totalSymbols.setText(symbols)