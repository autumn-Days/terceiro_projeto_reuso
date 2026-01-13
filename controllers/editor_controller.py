from PyQt6 import QtGui, QtCore, QtWidgets
from ext import find, datetime, wordcount, table, link

class EditorController:
    def __init__(self, model, view, app):
        self.model = model
        self.view = view
        self.app = app
        self._connect_signals()

    def _connect_signals(self):
        # Insert operations
        self.view.findAction.triggered.connect(self.show_find_dialog)
        self.view.dateTimeAction.triggered.connect(self.show_datetime_dialog)
        self.view.wordCountAction.triggered.connect(self.show_word_count)
        self.view.tableAction.triggered.connect(self.show_table_dialog)
        self.view.imageAction.triggered.connect(self.insert_image)
        self.view.linkAction.triggered.connect(self.show_link_dialog)

        # List operations
        self.view.bulletAction.triggered.connect(self.insert_bullet_list)
        self.view.numberedAction.triggered.connect(self.insert_numbered_list)

        # Document signals
        self.view.text.document().documentLayout().documentSizeChanged.connect(
            self.handle_document_size_changed
        )
        self.view.text.cursorPositionChanged.connect(self.update_cursor_position)
        self.view.text.textChanged.connect(self.on_text_changed)

        # Context menu
        self.view.text.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.CustomContextMenu)
        self.view.text.customContextMenuRequested.connect(self.show_context_menu)

    # Dialog helpers
    def show_find_dialog(self):
        find.Find(self.view).show()

    def show_datetime_dialog(self):
        datetime.DateTime(self.view).show()

    def show_word_count(self):
        wc = wordcount.WordCount(self.view)
        wc.getText()
        wc.show()

    def show_table_dialog(self):
        table.Table(self.view).show()

    def show_link_dialog(self):
        link.Link(self.view).show()

    def insert_image(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.view, 'Insert image', '.', 'Images (*.png *.xpm *.jpg *.bmp *.gif)'
        )
        if filename:
            image = QtGui.QImage(filename)
            if image.isNull():
                self.view.show_error_dialog("Image load error", "Could not load image file!")
            else:
                cursor = self.view.text.textCursor()
                cursor.insertImage(image, filename)

    def insert_bullet_list(self):
        cursor = self.view.text.textCursor()
        list_format = QtGui.QTextListFormat()
        list_format.setStyle(QtGui.QTextListFormat.Style.ListDisc)
        cursor.insertList(list_format)

    def insert_numbered_list(self):
        cursor = self.view.text.textCursor()
        cursor.insertList(QtGui.QTextListFormat.Style.ListDecimal)

    def handle_document_size_changed(self, size):
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
        cursor = self.view.text.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber() + 1
        
        # Atualiza status bar (assumindo que view tem esse método)
        if hasattr(self.view, 'update_status_bar'):
            self.view.update_status_bar(line, col)

        # Calculate current page
        cursor_y = self.view.text.cursorRect().center().y()
        page_current = int(
            (cursor_y + self.model.document_margin + 10) / self.model.page_height
        )
        
        # Atualiza label da página
        if hasattr(self.view, 'update_page_label'):
            self.view.update_page_label(page_current, self.model.page_count)

    def on_text_changed(self):
        self.model.changes_saved = False

    # --- Lógica do Menu de Contexto (Table/Link) ---
    def show_context_menu(self, pos):
        cursor = self.view.text.textCursor()
        table_obj = cursor.currentTable()
        hyperlink = link.currentHyperlink(cursor)

        if table_obj or hyperlink:
            pos = self.view.text.mapToGlobal(pos)
            menu = QtWidgets.QMenu(self.view.text)

            if hyperlink:
                self._add_hyperlink_menu_items(menu, hyperlink, cursor)
            if table_obj:
                self._add_table_menu_items(menu, table_obj, cursor)

            menu.exec(pos)
        else:
            event = QtGui.QContextMenuEvent(
                QtGui.QContextMenuEvent.Reason.Mouse,
                QtCore.QPoint(),
                self.view.text.mapToGlobal(QtCore.QPoint())
            )
            self.view.text.contextMenuEvent(event)

    def _add_hyperlink_menu_items(self, menu, hyperlink, cursor):
        openAction = QtGui.QAction("Open hyperlink", self.view)
        openAction.triggered.connect(lambda: link.openHyperlink(hyperlink))

        copyAction = QtGui.QAction("Copy hyperlink", self.view.text) # Ajustado parent
        copyAction.triggered.connect(lambda: self.app.clipboard().setText(hyperlink))

        removeAction = QtGui.QAction("Remove hyperlink", self.view.text)
        removeAction.triggered.connect(lambda: link.removeHyperlink(cursor))

        editAction = QtGui.QAction("Edit hyperlink", self.view.text)
        editAction.triggered.connect(lambda: link.Link(self.view, True).show())

        menu.addAction(openAction)
        menu.addAction(copyAction)
        menu.addAction(removeAction)
        menu.addAction(editAction)
        menu.addSeparator()

    def _add_table_menu_items(self, menu, table_obj, cursor):
        appendRowAction = QtGui.QAction("Append row", self.view.text)
        appendRowAction.triggered.connect(lambda: table_obj.appendRows(1))

        appendColAction = QtGui.QAction("Append column", self.view.text)
        appendColAction.triggered.connect(lambda: table_obj.appendColumns(1))

        removeRowAction = QtGui.QAction("Remove row", self.view.text)
        removeRowAction.triggered.connect(lambda: self._remove_row(table_obj, cursor))

        removeColAction = QtGui.QAction("Remove column", self.view.text)
        removeColAction.triggered.connect(lambda: self._remove_col(table_obj, cursor))

        insertRowAction = QtGui.QAction("Insert row", self.view.text)
        insertRowAction.triggered.connect(lambda: self._insert_row(table_obj, cursor))

        insertColAction = QtGui.QAction("Insert column", self.view.text)
        insertColAction.triggered.connect(lambda: self._insert_col(table_obj, cursor))

        mergeAction = QtGui.QAction("Merge cells", self.view.text)
        mergeAction.triggered.connect(lambda: table_obj.mergeCells(cursor))

        if not cursor.hasSelection():
            mergeAction.setEnabled(False)

        splitAction = QtGui.QAction("Split cells", self.view.text)
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
        cell = table_obj.cellAt(cursor)
        table_obj.removeRows(cell.row(), 1)

    def _remove_col(self, table_obj, cursor):
        cell = table_obj.cellAt(cursor)
        table_obj.removeColumns(cell.column(), 1)

    def _insert_row(self, table_obj, cursor):
        cell = table_obj.cellAt(cursor)
        table_obj.insertRows(cell.row(), 1)

    def _insert_col(self, table_obj, cursor):
        cell = table_obj.cellAt(cursor)
        table_obj.insertColumns(cell.column(), 1)