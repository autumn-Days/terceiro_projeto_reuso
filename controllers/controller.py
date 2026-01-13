from PyQt6 import QtGui, QtCore, QtWidgets, QtPrintSupport
from PyQt6.QtCore import Qt

from ext import find, datetime, wordcount, table, link

class Controller:
    def __init__(self, model, view, app):
        self.model = model
        self.view = view
        self.app = app

        self._connect_signals()
        self._setup_initial_state()

    def _connect_signals(self):
        """Connect view actions to controller methods"""
        # File operations
        self.view.newAction.triggered.connect(self.new_document)
        self.view.openAction.triggered.connect(self.open_document)
        self.view.saveAction.triggered.connect(self.save_document)
        self.view.printAction.triggered.connect(self.print_document)
        self.view.previewAction.triggered.connect(self.preview_document)

        # Edit operations
        self.view.findAction.triggered.connect(self.show_find_dialog)
        self.view.cutAction.triggered.connect(self.view.text.cut)
        self.view.copyAction.triggered.connect(self.view.text.copy)
        self.view.pasteAction.triggered.connect(self.view.text.paste)
        self.view.undoAction.triggered.connect(self.view.text.undo)
        self.view.redoAction.triggered.connect(self.view.text.redo)

        # Insert operations
        self.view.dateTimeAction.triggered.connect(self.show_datetime_dialog)
        self.view.wordCountAction.triggered.connect(self.show_word_count)
        self.view.tableAction.triggered.connect(self.show_table_dialog)
        self.view.imageAction.triggered.connect(self.insert_image)
        self.view.linkAction.triggered.connect(self.show_link_dialog)

        # List operations
        self.view.bulletAction.triggered.connect(self.insert_bullet_list)
        self.view.numberedAction.triggered.connect(self.insert_numbered_list)

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

        # View toggles
        self.view.toolbarToggleAction.triggered.connect(self.view.toggle_toolbar)
        self.view.formatbarToggleAction.triggered.connect(self.view.toggle_formatbar)
        self.view.statusbarToggleAction.triggered.connect(self.view.toggle_statusbar)

        # Document signals
        self.view.text.document().documentLayout().documentSizeChanged.connect(
            self.handle_document_size_changed
        )
        self.view.text.cursorPositionChanged.connect(self.update_cursor_position)
        self.view.text.textChanged.connect(self.on_text_changed)

        # Context menu
        self.view.text.setContextMenuPolicy(
            QtCore.Qt.ContextMenuPolicy.CustomContextMenu
        )
        self.view.text.customContextMenuRequested.connect(self.show_context_menu)

        # Model signals
        self.model.cursor_position_changed.connect(self.view.update_status_bar)
        self.model.page_changed.connect(self.view.update_page_label)

    def _setup_initial_state(self):
        """Setup initial document state"""
        self.view.set_document_margin(self.model.document_margin)
        self.view.set_minimum_height(self.model.page_height)
        self.update_cursor_position()

    # File operations
    def new_document(self):
        """Create a new document window"""
        from main_view import MainView
        from document_model import DocumentModel

        new_model = DocumentModel()
        new_view = MainView()
        new_controller = MainController(new_model, new_view, self.app)
        new_view.show()

    def open_document(self):
        """Open an existing document"""
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.view,
            'Open File',
            '.',
            'Writer Files (*.writer)'
        )

        if filename:
            try:
                content = self.model.load_from_file(filename)
                self.view.text.setText(content)
            except IOError as e:
                self.view.show_error_dialog("Open Error", str(e))

    def save_document(self):
        """Save the current document"""
        if not self.model.filename:
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(
                self.view,
                'Save File',
                '.',
                'Writer Files (*.writer)'
            )
            if not filename:
                return
            self.model.filename = filename

        try:
            content = self.view.text.toHtml()
            self.model.save_to_file(content)
        except (IOError, ValueError) as e:
            self.view.show_error_dialog("Save Error", str(e))

    def print_document(self):
        """Print the document"""
        dialog = QtPrintSupport.QPrintDialog(self.view.printer, self.view)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.view.text.document().print(self.view.printer)

    def preview_document(self):
        """Preview document before printing"""
        preview = QtPrintSupport.QPrintPreviewDialog(self.view.printer)
        preview.paintRequested.connect(lambda p: self.view.text.print(p))
        preview.exec()

    # Edit operations
    def show_find_dialog(self):
        """Show find and replace dialog"""
        find.Find(self.view).show()

    def show_datetime_dialog(self):
        """Show date/time insertion dialog"""
        datetime.DateTime(self.view).show()

    def show_word_count(self):
        """Show word count dialog"""
        wc = wordcount.WordCount(self.view)
        wc.getText()
        wc.show()

    def show_table_dialog(self):
        """Show table insertion dialog"""
        table.Table(self.view).show()

    def show_link_dialog(self):
        """Show hyperlink insertion dialog"""
        link.Link(self.view).show()

    def insert_image(self):
        """Insert an image into the document"""
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.view,
            'Insert image',
            '.',
            'Images (*.png *.xpm *.jpg *.bmp *.gif)'
        )

        if filename:
            image = QtGui.QImage(filename)

            if image.isNull():
                self.view.show_error_dialog(
                    "Image load error",
                    "Could not load image file!"
                )
            else:
                cursor = self.view.text.textCursor()
                cursor.insertImage(image, filename)

    def insert_bullet_list(self):
        """Insert a bullet list"""
        cursor = self.view.text.textCursor()
        list_format = QtGui.QTextListFormat()
        list_format.setStyle(QtGui.QTextListFormat.Style.ListDisc)
        cursor.insertList(list_format)

    def insert_numbered_list(self):
        """Insert a numbered list"""
        cursor = self.view.text.textCursor()
        cursor.insertList(QtGui.QTextListFormat.Style.ListDecimal)

    # Format operations
    def change_font_color(self):
        """Change text font color"""
        color = QtWidgets.QColorDialog.getColor()
        if color.isValid():
            self.view.text.setTextColor(color)

    def highlight_text(self):
        """Highlight text with background color"""
        color = QtWidgets.QColorDialog.getColor(QtGui.QColor(), self.view)
        if color.isValid():
            self.view.text.setTextBackgroundColor(color)

    def toggle_bold(self):
        """Toggle bold formatting"""
        if self.view.text.fontWeight() == QtGui.QFont.Weight.Bold:
            self.view.text.setFontWeight(QtGui.QFont.Weight.Normal)
        else:
            self.view.text.setFontWeight(QtGui.QFont.Weight.Bold)

    def toggle_italic(self):
        """Toggle italic formatting"""
        state = self.view.text.fontItalic()
        self.view.text.setFontItalic(not state)

    def toggle_underline(self):
        """Toggle underline formatting"""
        state = self.view.text.fontUnderline()
        self.view.text.setFontUnderline(not state)

    def toggle_strike(self):
        """Toggle strikethrough formatting"""
        fmt = self.view.text.currentCharFormat()
        fmt.setFontStrikeOut(not fmt.fontStrikeOut())
        self.view.text.setCurrentCharFormat(fmt)

    def toggle_superscript(self):
        """Toggle superscript formatting"""
        fmt = self.view.text.currentCharFormat()
        align = fmt.verticalAlignment()

        if align == QtGui.QTextCharFormat.VerticalAlignment.AlignNormal:
            fmt.setVerticalAlignment(
                QtGui.QTextCharFormat.VerticalAlignment.AlignSuperScript
            )
        else:
            fmt.setVerticalAlignment(
                QtGui.QTextCharFormat.VerticalAlignment.AlignNormal
            )

        self.view.text.setCurrentCharFormat(fmt)

    def toggle_subscript(self):
        """Toggle subscript formatting"""
        fmt = self.view.text.currentCharFormat()
        align = fmt.verticalAlignment()

        if align == QtGui.QTextCharFormat.VerticalAlignment.AlignNormal:
            fmt.setVerticalAlignment(
                QtGui.QTextCharFormat.VerticalAlignment.AlignSubScript
            )
        else:
            fmt.setVerticalAlignment(
                QtGui.QTextCharFormat.VerticalAlignment.AlignNormal
            )

        self.view.text.setCurrentCharFormat(fmt)

    # Alignment operations
    def align_left(self):
        """Align text to the left"""
        self.view.text.setAlignment(Qt.AlignmentFlag.AlignLeft)

    def align_center(self):
        """Center align text"""
        self.view.text.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def align_right(self):
        """Align text to the right"""
        self.view.text.setAlignment(Qt.AlignmentFlag.AlignRight)

    def align_justify(self):
        """Justify text"""
        self.view.text.setAlignment(Qt.AlignmentFlag.AlignJustify)

    # Indent operations
    def indent_text(self):
        """Indent selected text or insert tab"""
        cursor = self.view.text.textCursor()

        if cursor.hasSelection():
            temp = cursor.blockNumber()
            cursor.setPosition(cursor.anchor())
            diff = cursor.blockNumber() - temp

            direction = (
                QtGui.QTextCursor.MoveOperation.Up if diff > 0
                else QtGui.QTextCursor.MoveOperation.Down
            )

            for n in range(abs(diff) + 1):
                cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfLine)
                cursor.insertText("\t")
                cursor.movePosition(direction)
        else:
            cursor.insertText("\t")

    def dedent_text(self):
        """Dedent selected text"""
        cursor = self.view.text.textCursor()

        if cursor.hasSelection():
            temp = cursor.blockNumber()
            cursor.setPosition(cursor.anchor())
            diff = cursor.blockNumber() - temp

            direction = (
                QtGui.QTextCursor.MoveOperation.Up if diff > 0
                else QtGui.QTextCursor.MoveOperation.Down
            )

            for n in range(abs(diff) + 1):
                self._handle_dedent(cursor)
                cursor.movePosition(direction)
        else:
            self._handle_dedent(cursor)

    def _handle_dedent(self, cursor):
        """Handle dedenting a single line"""
        cursor.movePosition(QtGui.QTextCursor.MoveOperation.StartOfLine)
        line = cursor.block().text()

        if line.startswith("\t"):
            cursor.deleteChar()
        else:
            for char in line[:8]:
                if char != " ":
                    break
                cursor.deleteChar()

    # Document event handlers
    def handle_document_size_changed(self, size):
        """Handle document size changes for pagination"""
        height = int(size.height())
        page_height = self.model.page_height

        if height > page_height:
            self.view.text.setFixedHeight(height)
            self.view.scrollArea.verticalScrollBar().setValue(height)

            if (height > self.model.last_document_height and
                    height > (self.model.page_count + 1) * page_height):
                self.model.page_count += 1

            elif (height < self.model.last_document_height and
                  height < self.model.page_count * page_height):
                self.model.page_count -= 1

        self.model.last_document_height = height

    def update_cursor_position(self):
        """Update cursor position in status bar"""
        cursor = self.view.text.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1

        self.model.update_cursor_position(line, col)

        # Calculate current page
        cursor_y = self.view.text.cursorRect().center().y()
        page_current = int(
            (cursor_y + self.model.document_margin + 10) / self.model.page_height
        )

        self.model.update_page_info(page_current, self.model.page_count)

    def on_text_changed(self):
        """Handle text changes"""
        self.model.changes_saved = False

    # Context menu
    def show_context_menu(self, pos):
        """Show custom context menu for tables and links"""
        cursor = self.view.text.textCursor()
        table_obj = cursor.currentTable()
        hyperlink = link.currentHyperlink(cursor)

        if table_obj or hyperlink:
            pos = self.view.text.mapToGlobal(pos)
            menu = QtWidgets.QMenu(self.view.text)

            # Add hyperlink actions
            if hyperlink:
                self._add_hyperlink_menu_items(menu, hyperlink, cursor)

            # Add table actions
            if table_obj:
                self._add_table_menu_items(menu, table_obj, cursor)

            menu.exec(pos)
        else:
            # Show default context menu
            event = QtGui.QContextMenuEvent(
                QtGui.QContextMenuEvent.Reason.Mouse,
                QtCore.QPoint(),
                self.view.text.mapToGlobal(QtCore.QPoint())
            )
            self.view.text.contextMenuEvent(event)

    def _add_hyperlink_menu_items(self, menu, hyperlink, cursor):
        """Add hyperlink menu items"""
        openAction = QtGui.QAction("Open hyperlink", self.view)
        openAction.triggered.connect(lambda: link.openHyperlink(hyperlink))

        copyAction = QtGui.QAction("Copy hyperlink", self.view)
        copyAction.triggered.connect(
            lambda: self.app.clipboard().setText(hyperlink)
        )

        removeAction = QtGui.QAction("Remove hyperlink", self.view)
        removeAction.triggered.connect(lambda: link.removeHyperlink(cursor))

        editAction = QtGui.QAction("Edit hyperlink", self.view)
        editAction.triggered.connect(lambda: link.Link(self.view, True).show())

        menu.addAction(openAction)
        menu.addAction(copyAction)
        menu.addAction(removeAction)
        menu.addAction(editAction)
        menu.addSeparator()

    def _add_table_menu_items(self, menu, table_obj, cursor):
        """Add table menu items"""
        appendRowAction = QtGui.QAction("Append row", self.view)
        appendRowAction.triggered.connect(lambda: table_obj.appendRows(1))

        appendColAction = QtGui.QAction("Append column", self.view)
        appendColAction.triggered.connect(lambda: table_obj.appendColumns(1))

        removeRowAction = QtGui.QAction("Remove row", self.view)
        removeRowAction.triggered.connect(lambda: self._remove_row(table_obj, cursor))

        removeColAction = QtGui.QAction("Remove column", self.view)
        removeColAction.triggered.connect(lambda: self._remove_col(table_obj, cursor))

        insertRowAction = QtGui.QAction("Insert row", self.view)
        insertRowAction.triggered.connect(lambda: self._insert_row(table_obj, cursor))

        insertColAction = QtGui.QAction("Insert column", self.view)
        insertColAction.triggered.connect(lambda: self._insert_col(table_obj, cursor))

        mergeAction = QtGui.QAction("Merge cells", self.view)
        mergeAction.triggered.connect(lambda: table_obj.mergeCells(cursor))

        if not cursor.hasSelection():
            mergeAction.setEnabled(False)

        splitAction = QtGui.QAction("Split cells", self.view)
        cell = table_obj.cellAt(cursor)

        if cell.rowSpan() > 1 or cell.columnSpan() > 1:
            splitAction.triggered.connect(
                lambda: table_obj.splitCell(cell.row(), cell.column(), 1, 1)
            )
        else:
            splitAction.setEnabled(False)

        menu.addAction(appendRowAction)
        menu.addAction(appendColAction)
        menu.addSeparator()
        menu.addAction(removeRowAction)
        menu.addAction(removeColAction)
        menu.addSeparator()
        menu.addAction(insertRowAction)
        menu.addAction(insertColAction)
        menu.addSeparator()
        menu.addAction(mergeAction)
        menu.addAction(splitAction)

    def _remove_row(self, table_obj, cursor):
        """Remove current row from table"""
        cell = table_obj.cellAt(cursor)
        table_obj.removeRows(cell.row(), 1)

    def _remove_col(self, table_obj, cursor):
        """Remove current column from table"""
        cell = table_obj.cellAt(cursor)
        table_obj.removeColumns(cell.column(), 1)

    def _insert_row(self, table_obj, cursor):
        """Insert row at current position"""
        cell = table_obj.cellAt(cursor)
        table_obj.insertRows(cell.row(), 1)

    def _insert_col(self, table_obj, cursor):
        """Insert column at current position"""
        cell = table_obj.cellAt(cursor)
        table_obj.insertColumns(cell.column(), 1)

    # Window close event
    def handle_close_event(self, event):
        """Handle window close event"""
        if self.model.changes_saved:
            event.accept()
            return

        answer = self.view.show_unsaved_changes_dialog()

        if answer == QtWidgets.QMessageBox.StandardButton.Save:
            self.save_document()
            event.accept()
        elif answer == QtWidgets.QMessageBox.StandardButton.Discard:
            event.accept()
        else:
            event.ignore()