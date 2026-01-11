from PyQt6 import QtGui, QtCore, QtWidgets, QtPrintSupport
from PyQt6.QtCore import Qt

class View(QtWidgets.QMainWindow):
    """View class that handles all UI components"""
    def __init__(self, parent=None):
        super().__init__(parent)

        self.printer = None
        self.text = None
        self.toolbar = None
        self.formatbar = None
        self.status = None
        self.pageCountLabel = None
        self.scrollArea = None

        # Actions
        self.newAction = None
        self.openAction = None
        self.saveAction = None
        self.printAction = None
        self.previewAction = None
        self.findAction = None
        self.cutAction = None
        self.copyAction = None
        self.pasteAction = None
        self.undoAction = None
        self.redoAction = None

        self._init_ui()

    def _init_ui(self):
        """Initialize all UI components"""
        self._init_document()
        self._init_toolbar()
        self._init_formatbar()
        self._init_menubar()
        self._init_statusbar()

        self.setMinimumSize(995, 900)
        self.move(450, 25)
        self.setWindowTitle("Writer")
        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

    def _init_document(self):
        """Initialize document display components"""
        # Printer setup
        self.printer = QtPrintSupport.QPrinter()
        self.printer.setPageMargins(
            QtCore.QMarginsF(0, 0, 0, 0),
            QtGui.QPageLayout.Unit.Point
        )

        # Text editor
        self.text = QtWidgets.QTextEdit(self)
        self.text.setStyleSheet("background-color: #FFFFFF;")
        self.text.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.text.setFixedWidth(595)
        self.text.setTabStopDistance(33)
        self.text.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        # Document settings
        doc = self.text.document()
        doc.setPageSize(QtCore.QSizeF(595, 841))

        # Container and layout
        container = QtWidgets.QWidget(self)
        container.setStyleSheet("background-color: #A0A0A0;")

        layout = QtWidgets.QGridLayout(self)
        layout.addWidget(QtWidgets.QWidget(), 0, 0)
        layout.addWidget(self.text, 1, 0)
        container.setLayout(layout)

        # Scroll area
        self.scrollArea = QtWidgets.QScrollArea(self)
        self.scrollArea.setWidget(container)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.setCentralWidget(self.scrollArea)

    def _init_toolbar(self):
        """Initialize main toolbar with actions"""
        # File actions
        self.newAction = self._create_action(
            "icons/new.png", "New", "Ctrl+N",
            "Create a new document from scratch."
        )
        self.openAction = self._create_action(
            "icons/open.png", "Open file", "Ctrl+O",
            "Open existing document"
        )
        self.saveAction = self._create_action(
            "icons/save.png", "Save", "Ctrl+S",
            "Save document"
        )
        self.printAction = self._create_action(
            "icons/print.png", "Print document", "Ctrl+P",
            "Print document"
        )
        self.previewAction = self._create_action(
            "icons/preview.png", "Page view", "Ctrl+Shift+P",
            "Preview page before printing"
        )

        # Edit actions
        self.findAction = self._create_action(
            "icons/find.png", "Find and replace", "Ctrl+F",
            "Find and replace words in your document"
        )
        self.cutAction = self._create_action(
            "icons/cut.png", "Cut to clipboard", "Ctrl+X",
            "Delete and copy text to clipboard"
        )
        self.copyAction = self._create_action(
            "icons/copy.png", "Copy to clipboard", "Ctrl+C",
            "Copy text to clipboard"
        )
        self.pasteAction = self._create_action(
            "icons/paste.png", "Paste from clipboard", "Ctrl+V",
            "Paste text from clipboard"
        )
        self.undoAction = self._create_action(
            "icons/undo.png", "Undo last action", "Ctrl+Z",
            "Undo last action"
        )
        self.redoAction = self._create_action(
            "icons/redo.png", "Redo last undone thing", "Ctrl+Y",
            "Redo last undone thing"
        )

        # Insert actions
        dateTimeAction = self._create_action(
            "icons/calender.png", "Insert current date/time", "Ctrl+D",
            "Insert current date/time"
        )
        wordCountAction = self._create_action(
            "icons/count.png", "See word/symbol count", "Ctrl+W",
            "See word/symbol count"
        )
        tableAction = self._create_action(
            "icons/table.png", "Insert table", "Ctrl+T",
            "Insert table"
        )
        imageAction = self._create_action(
            "icons/image.png", "Insert image", "Ctrl+Shift+I",
            "Insert image"
        )
        linkAction = self._create_action(
            "icons/link.png", "Insert hyperlink", "Ctrl+H",
            "Insert hyperlink"
        )

        # List actions
        bulletAction = self._create_action(
            "icons/bullet.png", "Insert bullet List", "Ctrl+Shift+B",
            "Insert bullet list"
        )
        numberedAction = self._create_action(
            "icons/number.png", "Insert numbered List", "Ctrl+Shift+L",
            "Insert numbered list"
        )

        # Create toolbar
        self.toolbar = self.addToolBar("Options")

        # Add actions to toolbar
        self.toolbar.addAction(self.newAction)
        self.toolbar.addAction(self.openAction)
        self.toolbar.addAction(self.saveAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.printAction)
        self.toolbar.addAction(self.previewAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.cutAction)
        self.toolbar.addAction(self.copyAction)
        self.toolbar.addAction(self.pasteAction)
        self.toolbar.addAction(self.undoAction)
        self.toolbar.addAction(self.redoAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(self.findAction)
        self.toolbar.addAction(dateTimeAction)
        self.toolbar.addAction(wordCountAction)
        self.toolbar.addAction(tableAction)
        self.toolbar.addAction(imageAction)
        self.toolbar.addAction(linkAction)
        self.toolbar.addSeparator()
        self.toolbar.addAction(bulletAction)
        self.toolbar.addAction(numberedAction)

        self.addToolBarBreak()

        # Store additional actions for controller access
        self.dateTimeAction = dateTimeAction
        self.wordCountAction = wordCountAction
        self.tableAction = tableAction
        self.imageAction = imageAction
        self.linkAction = linkAction
        self.bulletAction = bulletAction
        self.numberedAction = numberedAction

    def _init_formatbar(self):
        """Initialize formatting toolbar"""
        # Font selection
        fontBox = QtWidgets.QFontComboBox(self)
        self.fontBox = fontBox

        fontSize = QtWidgets.QSpinBox(self)
        fontSize.setSuffix(" pt")
        fontSize.setValue(14)
        self.fontSize = fontSize

        # Format actions
        fontColor = self._create_action(
            "icons/font-color.png", "Change font color", None,
            "Change font color"
        )
        boldAction = self._create_action(
            "icons/bold.png", "Bold", None, "Bold"
        )
        italicAction = self._create_action(
            "icons/italic.png", "Italic", None, "Italic"
        )
        underlAction = self._create_action(
            "icons/underline.png", "Underline", None, "Underline"
        )
        strikeAction = self._create_action(
            "icons/strike.png", "Strike-out", None, "Strike-out"
        )
        superAction = self._create_action(
            "icons/superscript.png", "Superscript", None, "Superscript"
        )
        subAction = self._create_action(
            "icons/subscript.png", "Subscript", None, "Subscript"
        )

        # Alignment actions
        alignLeft = self._create_action(
            "icons/align-left.png", "Align left", None, "Align left"
        )
        alignCenter = self._create_action(
            "icons/align-center.png", "Align center", None, "Align center"
        )
        alignRight = self._create_action(
            "icons/align-right.png", "Align right", None, "Align right"
        )
        alignJustify = self._create_action(
            "icons/align-justify.png", "Align justify", None, "Align justify"
        )

        # Indent actions
        indentAction = self._create_action(
            "icons/indent.png", "Indent Area", "Ctrl+Tab", "Indent Area"
        )
        dedentAction = self._create_action(
            "icons/dedent.png", "Dedent Area", "Shift+Tab", "Dedent Area"
        )

        # Background color
        backColor = self._create_action(
            "icons/highlight.png", "Change background color", None,
            "Change background color"
        )

        # Create formatbar
        self.formatbar = self.addToolBar("Format")

        self.formatbar.addWidget(fontBox)
        self.formatbar.addWidget(fontSize)
        self.formatbar.addSeparator()
        self.formatbar.addAction(fontColor)
        self.formatbar.addAction(backColor)
        self.formatbar.addSeparator()
        self.formatbar.addAction(boldAction)
        self.formatbar.addAction(italicAction)
        self.formatbar.addAction(underlAction)
        self.formatbar.addAction(strikeAction)
        self.formatbar.addAction(superAction)
        self.formatbar.addAction(subAction)
        self.formatbar.addSeparator()
        self.formatbar.addAction(alignLeft)
        self.formatbar.addAction(alignCenter)
        self.formatbar.addAction(alignRight)
        self.formatbar.addAction(alignJustify)
        self.formatbar.addSeparator()
        self.formatbar.addAction(indentAction)
        self.formatbar.addAction(dedentAction)

        # Store for controller access
        self.fontColorAction = fontColor
        self.boldAction = boldAction
        self.italicAction = italicAction
        self.underlAction = underlAction
        self.strikeAction = strikeAction
        self.superAction = superAction
        self.subAction = subAction
        self.alignLeftAction = alignLeft
        self.alignCenterAction = alignCenter
        self.alignRightAction = alignRight
        self.alignJustifyAction = alignJustify
        self.indentAction = indentAction
        self.dedentAction = dedentAction
        self.backColorAction = backColor

    def _init_menubar(self):
        """Initialize menu bar"""
        menubar = self.menuBar()

        file_menu = menubar.addMenu("File")
        edit_menu = menubar.addMenu("Edit")
        view_menu = menubar.addMenu("View")

        # File menu
        file_menu.addAction(self.newAction)
        file_menu.addAction(self.openAction)
        file_menu.addAction(self.saveAction)
        file_menu.addAction(self.printAction)
        file_menu.addAction(self.previewAction)

        # Edit menu
        edit_menu.addAction(self.undoAction)
        edit_menu.addAction(self.redoAction)
        edit_menu.addAction(self.cutAction)
        edit_menu.addAction(self.copyAction)
        edit_menu.addAction(self.pasteAction)
        edit_menu.addAction(self.findAction)

        # View menu - toggle actions
        toolbarAction = QtGui.QAction("Toggle Toolbar", self)
        formatbarAction = QtGui.QAction("Toggle Formatbar", self)
        statusbarAction = QtGui.QAction("Toggle Statusbar", self)

        view_menu.addAction(toolbarAction)
        view_menu.addAction(formatbarAction)
        view_menu.addAction(statusbarAction)

        # Store for controller access
        self.toolbarToggleAction = toolbarAction
        self.formatbarToggleAction = formatbarAction
        self.statusbarToggleAction = statusbarAction

    def _init_statusbar(self):
        """Initialize status bar"""
        self.status = self.statusBar()
        self.status.setStyleSheet("background-color: #A0A0A0;")

        self.pageCountLabel = QtWidgets.QLabel("", self)
        self.status.addPermanentWidget(self.pageCountLabel)
        self.status.resize(400, 50)

    def _create_action(self, icon, text, shortcut, tip):
        """Helper to create QAction"""
        action = QtGui.QAction(QtGui.QIcon(icon), text, self)
        if shortcut:
            action.setShortcut(shortcut)
        action.setStatusTip(tip)
        return action

    # Public methods for updating UI
    def update_status_bar(self, line, col):
        """Update status bar with cursor position"""
        self.status.showMessage(f"Line: {line} | Column: {col}")

    def update_page_label(self, current_page, total_pages):
        """Update page count label"""
        self.pageCountLabel.setText(f"Page {current_page} of {total_pages}")

    def set_document_margin(self, margin):
        """Set document margin"""
        doc = self.text.document()
        rootFrame = doc.rootFrame()
        fmt = rootFrame.frameFormat()
        fmt.setMargin(margin)
        rootFrame.setFrameFormat(fmt)

    def set_minimum_height(self, height):
        """Set minimum height for text editor"""
        self.text.setMinimumHeight(height)

    def toggle_toolbar(self):
        """Toggle toolbar visibility"""
        self.toolbar.setVisible(not self.toolbar.isVisible())

    def toggle_formatbar(self):
        """Toggle formatbar visibility"""
        self.formatbar.setVisible(not self.formatbar.isVisible())

    def toggle_statusbar(self):
        """Toggle statusbar visibility"""
        self.status.setVisible(not self.status.isVisible())

    def show_unsaved_changes_dialog(self):
        """Show dialog for unsaved changes"""
        popup = QtWidgets.QMessageBox(self)
        popup.setIcon(QtWidgets.QMessageBox.Icon.Warning)
        popup.setText("The document has been modified")
        popup.setInformativeText("Do you want to save your changes?")
        popup.setStandardButtons(
            QtWidgets.QMessageBox.StandardButton.Save |
            QtWidgets.QMessageBox.StandardButton.Cancel |
            QtWidgets.QMessageBox.StandardButton.Discard
        )
        popup.setDefaultButton(QtWidgets.QMessageBox.StandardButton.Save)
        return popup.exec()

    def show_error_dialog(self, title, message):
        """Show error dialog"""
        popup = QtWidgets.QMessageBox(
            QtWidgets.QMessageBox.Icon.Critical,
            title,
            message,
            QtWidgets.QMessageBox.StandardButton.Ok,
            self
        )
        popup.show()