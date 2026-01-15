from PyQt6 import QtGui, QtCore, QtWidgets
from PyQt6.QtCore import Qt

class FormattingFacade:
    """
    Facade para simplificar operações complexas de formatação de texto (Rich Text).
    Esconde a complexidade de QTextCursor, QTextBlock e CharFormat.
    """
    def __init__(self, text_edit: QtWidgets.QTextEdit):
        self.text_edit = text_edit

    def _cursor(self):
        return self.text_edit.textCursor()

    def _merge_format(self, fmt):
        cursor = self._cursor()
        cursor.mergeCharFormat(fmt)
        self.text_edit.setCurrentCharFormat(fmt)

    # --- Font & Style Operations ---
    
    def set_font_family(self, font: QtGui.QFont):
        self.text_edit.setCurrentFont(font)

    def set_font_size(self, size: int):
        self.text_edit.setFontPointSize(size)

    def set_text_color(self, color: QtGui.QColor):
        self.text_edit.setTextColor(color)

    def set_background_color(self, color: QtGui.QColor):
        self.text_edit.setTextBackgroundColor(color)

    def toggle_bold(self):
        fmt = self.text_edit.currentCharFormat()
        weight = QtGui.QFont.Weight.Normal if fmt.fontWeight() == QtGui.QFont.Weight.Bold else QtGui.QFont.Weight.Bold
        fmt.setFontWeight(weight)
        self._merge_format(fmt)

    def toggle_italic(self):
        fmt = self.text_edit.currentCharFormat()
        fmt.setFontItalic(not fmt.fontItalic())
        self._merge_format(fmt)

    def toggle_underline(self):
        fmt = self.text_edit.currentCharFormat()
        fmt.setFontUnderline(not fmt.fontUnderline())
        self._merge_format(fmt)

    def toggle_strike(self):
        fmt = self.text_edit.currentCharFormat()
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())
        self._merge_format(fmt)

    def toggle_superscript(self):
        fmt = self.text_edit.currentCharFormat()
        align = fmt.verticalAlignment()
        if align == QtGui.QTextCharFormat.VerticalAlignment.AlignNormal:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.VerticalAlignment.AlignSuperScript)
        else:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.VerticalAlignment.AlignNormal)
        self._merge_format(fmt)

    def toggle_subscript(self):
        fmt = self.text_edit.currentCharFormat()
        align = fmt.verticalAlignment()
        if align == QtGui.QTextCharFormat.VerticalAlignment.AlignNormal:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.VerticalAlignment.AlignSubScript)
        else:
            fmt.setVerticalAlignment(QtGui.QTextCharFormat.VerticalAlignment.AlignNormal)
        self._merge_format(fmt)

    # --- Alignment Operations ---
    
    def set_alignment(self, alignment: Qt.AlignmentFlag):
        self.text_edit.setAlignment(alignment)

    # --- Indentation Logic (Encapsulada) ---

    def indent(self):
        cursor = self._cursor()
        if cursor.hasSelection():
            self._modify_selected_blocks(cursor, indent=True)
        else:
            cursor.insertText("\t")

    def dedent(self):
        cursor = self._cursor()
        if cursor.hasSelection():
            self._modify_selected_blocks(cursor, indent=False)
        else:
            self._handle_single_dedent(cursor)

    def _modify_selected_blocks(self, cursor, indent=True):
        """Helper para iterar sobre blocos selecionados"""
        temp_cursor = self._cursor()
        temp_cursor.setPosition(cursor.selectionStart())
        end = cursor.selectionEnd()
        
        temp_cursor.beginEditBlock()
        while temp_cursor.position() <= end:
            temp_cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfLine)
            if indent:
                temp_cursor.insertText("\t")
            else:
                self._handle_single_dedent(temp_cursor)
            
            if not temp_cursor.movePosition(QtGui.QTextCursor.MoveOperation.Down):
                break
        temp_cursor.endEditBlock()

    def _handle_single_dedent(self, cursor):
        """Helper para remover indentação de uma linha"""
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfLine)
        line = cursor.block().text()
        if line.startswith("\t"):
            cursor.deleteChar()
        else:
            # Remove até 8 espaços se não houver TAB
            for char in line[:8]:
                if char != " ": break
                cursor.deleteChar()