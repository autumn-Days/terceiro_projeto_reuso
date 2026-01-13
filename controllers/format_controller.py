from PyQt6 import QtWidgets, QtGui
from PyQt6.QtCore import Qt
from utils.formatting_facade import FormattingFacade

class FormatController:
    #Esse elemento vai ser o responsável por mandar os dados para o Facade
    def __init__(self, view):
        self.view = view
        # Instancia a Fachada injetando o componente de texto da View
        self.formatter = FormattingFacade(self.view.text)
        self._connect_signals()

    def _connect_signals(self):
        # parte da fonte
        self.view.fontBox.currentFontChanged.connect(self.formatter.set_font_family)
        self.view.fontSize.valueChanged.connect(self.formatter.set_font_size)
        
        # parte da cor (Dialogs ficam no Controller, aplicação na Facade)
        self.view.fontColorAction.triggered.connect(self.select_font_color)
        self.view.backColorAction.triggered.connect(self.select_highlight_color)

        # alterações do estilo da fonte
        self.view.boldAction.triggered.connect(self.formatter.toggle_bold)
        self.view.italicAction.triggered.connect(self.formatter.toggle_italic)
        self.view.underlAction.triggered.connect(self.formatter.toggle_underline)
        self.view.strikeAction.triggered.connect(self.formatter.toggle_strike)
        self.view.superAction.triggered.connect(self.formatter.toggle_superscript)
        self.view.subAction.triggered.connect(self.formatter.toggle_subscript)

        # Parte do alinhamento
        self.view.alignLeftAction.triggered.connect(lambda: self.formatter.set_alignment(Qt.AlignmentFlag.AlignLeft))
        self.view.alignCenterAction.triggered.connect(lambda: self.formatter.set_alignment(Qt.AlignmentFlag.AlignCenter))
        self.view.alignRightAction.triggered.connect(lambda: self.formatter.set_alignment(Qt.AlignmentFlag.AlignRight))
        self.view.alignJustifyAction.triggered.connect(lambda: self.formatter.set_alignment(Qt.AlignmentFlag.AlignJustify))

        # Parte da identação
        self.view.indentAction.triggered.connect(self.formatter.indent)
        self.view.dedentAction.triggered.connect(self.formatter.dedent)

    #aqui o Controller vai abrir a janela, pegar o dado e passar para o Facade lidar

    def select_font_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.formatter.set_text_color(color)

    def select_highlight_color(self):
        color = QtWidgets.QColorDialog.getColor(QtGui.QColor(), self.view)
        if color.isValid():
            self.formatter.set_background_color(color)