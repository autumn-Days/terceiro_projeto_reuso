from PyQt6 import QtGui, QtWidgets

class ActionManager:
    """
    Responsible for creating Actions, Toolbars, and Menus.
    Attaches them to the main window instance.
    """
    def __init__(self, main_window):
        self.window = main_window
        self._create_actions()
        self._init_toolbar()
        self._init_formatbar()
        self._init_menubar()

    def _create_action(self, icon, text, shortcut, tip):
        action = QtGui.QAction(QtGui.QIcon(icon), text, self.window)
        if shortcut:
            action.setShortcut(shortcut)
        action.setStatusTip(tip)
        return action

    def _create_actions(self):
        # File actions
        self.window.newAction = self._create_action("icons/new.png", "New", "Ctrl+N", "Create a new document.")
        self.window.openAction = self._create_action("icons/open.png", "Open file", "Ctrl+O", "Open existing document")
        self.window.saveAction = self._create_action("icons/save.png", "Save", "Ctrl+S", "Save document")
        self.window.printAction = self._create_action("icons/print.png", "Print document", "Ctrl+P", "Print document")
        self.window.previewAction = self._create_action("icons/preview.png", "Page view", "Ctrl+Shift+P", "Preview page")

        # Edit actions
        self.window.findAction = self._create_action("icons/find.png", "Find and replace", "Ctrl+F", "Find and replace")
        self.window.cutAction = self._create_action("icons/cut.png", "Cut", "Ctrl+X", "Cut to clipboard")
        self.window.copyAction = self._create_action("icons/copy.png", "Copy", "Ctrl+C", "Copy to clipboard")
        self.window.pasteAction = self._create_action("icons/paste.png", "Paste", "Ctrl+V", "Paste from clipboard")
        self.window.undoAction = self._create_action("icons/undo.png", "Undo", "Ctrl+Z", "Undo last action")
        self.window.redoAction = self._create_action("icons/redo.png", "Redo", "Ctrl+Y", "Redo last undone thing")

        # Insert actions
        self.window.dateTimeAction = self._create_action("icons/calender.png", "Date/Time", "Ctrl+D", "Insert date/time")
        self.window.wordCountAction = self._create_action("icons/count.png", "Word count", "Ctrl+W", "See word count")
        self.window.tableAction = self._create_action("icons/table.png", "Table", "Ctrl+T", "Insert table")
        self.window.imageAction = self._create_action("icons/image.png", "Image", "Ctrl+Shift+I", "Insert image")
        self.window.linkAction = self._create_action("icons/link.png", "Hyperlink", "Ctrl+H", "Insert hyperlink")
        
        # Lists
        self.window.bulletAction = self._create_action("icons/bullet.png", "Bullet List", "Ctrl+Shift+B", "Insert bullet list")
        self.window.numberedAction = self._create_action("icons/number.png", "Numbered List", "Ctrl+Shift+L", "Insert numbered list")

        # Format Actions
        self.window.fontColorAction = self._create_action("icons/font-color.png", "Font color", None, "Change font color")
        self.window.backColorAction = self._create_action("icons/highlight.png", "Background color", None, "Change background")
        self.window.boldAction = self._create_action("icons/bold.png", "Bold", None, "Bold")
        self.window.italicAction = self._create_action("icons/italic.png", "Italic", None, "Italic")
        self.window.underlAction = self._create_action("icons/underline.png", "Underline", None, "Underline")
        self.window.strikeAction = self._create_action("icons/strike.png", "Strike-out", None, "Strike-out")
        self.window.superAction = self._create_action("icons/superscript.png", "Superscript", None, "Superscript")
        self.window.subAction = self._create_action("icons/subscript.png", "Subscript", None, "Subscript")

        # Alignment
        self.window.alignLeftAction = self._create_action("icons/align-left.png", "Align left", None, "Align left")
        self.window.alignCenterAction = self._create_action("icons/align-center.png", "Align center", None, "Align center")
        self.window.alignRightAction = self._create_action("icons/align-right.png", "Align right", None, "Align right")
        self.window.alignJustifyAction = self._create_action("icons/align-justify.png", "Align justify", None, "Align justify")

        # Indent
        self.window.indentAction = self._create_action("icons/indent.png", "Indent", "Ctrl+Tab", "Indent Area")
        self.window.dedentAction = self._create_action("icons/dedent.png", "Dedent", "Shift+Tab", "Dedent Area")

    def _init_toolbar(self):
        self.window.toolbar = self.window.addToolBar("Options")
        
        # Add actions
        actions = [
            self.window.newAction, self.window.openAction, self.window.saveAction, None,
            self.window.printAction, self.window.previewAction, None,
            self.window.cutAction, self.window.copyAction, self.window.pasteAction, 
            self.window.undoAction, self.window.redoAction, None,
            self.window.findAction, self.window.dateTimeAction, self.window.wordCountAction, 
            self.window.tableAction, self.window.imageAction, self.window.linkAction, None,
            self.window.bulletAction, self.window.numberedAction
        ]

        for action in actions:
            if action is None:
                self.window.toolbar.addSeparator()
            else:
                self.window.toolbar.addAction(action)
        
        self.window.addToolBarBreak()

    def _init_formatbar(self):
        self.window.formatbar = self.window.addToolBar("Format")
        
        # Font Widgets
        self.window.fontBox = QtWidgets.QFontComboBox(self.window)
        self.window.fontSize = QtWidgets.QSpinBox(self.window)
        self.window.fontSize.setSuffix(" pt")
        self.window.fontSize.setValue(14)

        self.window.formatbar.addWidget(self.window.fontBox)
        self.window.formatbar.addWidget(self.window.fontSize)
        self.window.formatbar.addSeparator()

        actions = [
            self.window.fontColorAction, self.window.backColorAction, None,
            self.window.boldAction, self.window.italicAction, self.window.underlAction,
            self.window.strikeAction, self.window.superAction, self.window.subAction, None,
            self.window.alignLeftAction, self.window.alignCenterAction, self.window.alignRightAction,
            self.window.alignJustifyAction, None,
            self.window.indentAction, self.window.dedentAction
        ]

        for action in actions:
            if action is None:
                self.window.formatbar.addSeparator()
            else:
                self.window.formatbar.addAction(action)

    def _init_menubar(self):
        menubar = self.window.menuBar()
        file_menu = menubar.addMenu("File")
        edit_menu = menubar.addMenu("Edit")
        view_menu = menubar.addMenu("View")

        # File
        file_menu.addAction(self.window.newAction)
        file_menu.addAction(self.window.openAction)
        file_menu.addAction(self.window.saveAction)
        file_menu.addAction(self.window.printAction)
        file_menu.addAction(self.window.previewAction)

        # Edit
        edit_menu.addAction(self.window.undoAction)
        edit_menu.addAction(self.window.redoAction)
        edit_menu.addAction(self.window.cutAction)
        edit_menu.addAction(self.window.copyAction)
        edit_menu.addAction(self.window.pasteAction)
        edit_menu.addAction(self.window.findAction)

        # View Toggles
        self.window.toolbarToggleAction = QtGui.QAction("Toggle Toolbar", self.window)
        self.window.formatbarToggleAction = QtGui.QAction("Toggle Formatbar", self.window)
        self.window.statusbarToggleAction = QtGui.QAction("Toggle Statusbar", self.window)

        view_menu.addAction(self.window.toolbarToggleAction)
        view_menu.addAction(self.window.formatbarToggleAction)
        view_menu.addAction(self.window.statusbarToggleAction)