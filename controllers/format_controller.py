from PyQt6 import QtGui, QtWidgets, QtCore
from PyQt6.QtCore import Qt

class FormatController:
    def __init__(self, view):
        self.view = view
        self._connect_signals()

    def _connect_signals(self):
        # Format operations
        self.view.fontBox.currentFontChanged.connect(
            lambda font: self.view.text.setCurrentFont(font)
        )
        self.view.fontSize.valueChanged.connect(
            lambda size: self.view.text.setFontPointSize(size)
        )
        self.view.fontColorAction.triggered.connect(self.change_font_color)
        self.view.backColorAction.triggered.connect(self.highlight_text)
        self.view.boldAction.triggered.connect(self.toggle_bold)
        self.view.italicAction.triggered.connect(self.toggle_italic)
        self.view.underlAction.triggered.connect(self.toggle_underline)
        self.view.strikeAction.triggered.connect(self.toggle_strike)
        self.view.superAction.triggered.connect(self.toggle_superscript)
        self.view.subAction.triggered.connect(self.toggle_subscript)

        # Alignment operations
        self.view.alignLeftAction.triggered.connect(self.align_left)
        self.view.alignCenterAction.triggered.connect(self.align_center)
        self.view.alignRightAction.triggered.connect(self.align_right)
        self.view.alignJustifyAction.triggered.connect(self.align_justify)

        # Indent operations
        self.view.indentAction.triggered.connect(self.indent_text)
        self.view.dedentAction.triggered.connect(self.dedent_text)

    def change_font_color(self):
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.view.text.setTextColor(color)

    def highlight_text(self):
        color = QtWidgets.QColorDialog.getColor(QtGui.QColor(), self.view)
        if color.isValid():
            self.view.text.setTextBackgroundColor(color)

    def toggle_bold(self):
        if self.view.text.fontWeight() == QtGui.QFont.Weight.Bold:
            self.view.text.setFontWeight(QtGui.QFont.Weight.Normal)
        else:
            self.view.text.setFontWeight(QtGui.QFont.Weight.Bold)

    def toggle_italic(self):
        state = self.view.text.fontItalic()
        self.view.text.setFontItalic(not state)

    def toggle_underline(self):
        state = self.view.text.fontUnderline()
        self.view.text.setFontUnderline(not state)

    def toggle_strike(self):
        fmt = self.view.text.currentCharFormat()
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())
        self.view.text.setCurrentCharFormat(fmt)

    def toggle_superscript(self):
        fmt = self.view.text.currentCharFormat()
        align = fmt.verticalAlignment()
        if align == QtGui.QTextCharFormat.VerticalAlignment.AlignNormal:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.VerticalAlignment.AlignSuperScript)
        else:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.VerticalAlignment.AlignNormal)
        self.view.text.setCurrentCharFormat(fmt)

    def toggle_subscript(self):
        fmt = self.view.text.currentCharFormat()
        align = fmt.verticalAlignment()
        if align == QtGui.QTextCharFormat.VerticalAlignment.AlignNormal:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.VerticalAlignment.AlignSubScript)
        else:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.VerticalAlignment.AlignNormal)
        self.view.text.setCurrentCharFormat(fmt)

    def align_left(self):
        self.view.text.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def align_center(self):
        self.view.text.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def align_right(self):
        self.view.text.setAlignment(Qt.AlignmentFlag.AlignRight)

    def align_justify(self):
        self.view.text.setAlignment(Qt.AlignmentFlag.AlignJustify)

    def indent_text(self):
        cursor = self.view.text.textCursor()
        if cursor.hasSelection():
            temp = cursor.blockNumber()
            cursor.setPosition(cursor.anchor())
            diff = cursor.blockNumber() - temp
            direction = (QtGui.QTextCursor.MoveOperation.Up if diff > 0 
                         else QtGui.QTextCursor.MoveOperation.Down)
            for n in range(abs(diff) + 1):
                cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfLine)
                cursor.insertText("\t")
                cursor.movePosition(direction)
        else:
            cursor.insertText("\t")

    def dedent_text(self):
        cursor = self.view.text.textCursor()
        if cursor.hasSelection():
            temp = cursor.blockNumber()
            cursor.setPosition(cursor.anchor())
            diff = cursor.blockNumber() - temp
            direction = (QtGui.QTextCursor.MoveOperation.Up if diff > 0 
                         else QtGui.QTextCursor.MoveOperation.Down)
            for n in range(abs(diff) + 1):
                self._handle_dedent(cursor)
                cursor.movePosition(direction)
        else:
            self._handle_dedent(cursor)

    def _handle_dedent(self, cursor):
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfLine)
        line = cursor.block().text()
        if line.startswith("\t"):
            cursor.deleteChar()
        else:
            for char in line[:8]:
                if char != " ":
                    break
                cursor.deleteChar()