from PyQt6 import QtGui, QtWidgets
from views.editor_view import EditorView
from views.action_manager import ActionManager

class MainView(QtWidgets.QMainWindow):
    """
    Main Window that assembles the Editor and the Actions.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        # 1. Setup Main Window Properties
        self.setMinimumSize(995, 900)
        self.move(450, 25)
        self.setWindowTitle("Writer")
        self.setWindowIcon(QtGui.QIcon("icons/icon.png"))

        # 2. Setup Central Widget (Editor)
        self.editor_view = EditorView(self)
        self.setCentralWidget(self.editor_view)

        # 3. Setup Actions and Bars (Delegate to Manager)
        # O Manager vai popular 'self' com actions (self.newAction, etc.)
        self.action_manager = ActionManager(self)
        
        # 4. Setup Status Bar
        self._init_statusbar()

    # --- Properties to maintain compatibility with Controller ---
    # Isso permite que o Controller chame self.view.text ou self.view.printer
    # sem saber que eles estão dentro de editor_view
    @property
    def text(self):
        return self.editor_view.text
    
    @property
    def printer(self):
        return self.editor_view.printer

    @property
    def scrollArea(self):
        return self.editor_view.scroll_area

    def _init_statusbar(self):
        self.status = self.statusBar()
        self.status.setStyleSheet("background-color: #A0A0A0;")
        self.pageCountLabel = QtWidgets.QLabel("", self)
        self.status.addPermanentWidget(self.pageCountLabel)
        self.status.resize(400, 50)

    # --- UI Logic Delegated methods ---
    
    def set_document_margin(self, margin):
        self.editor_view.set_document_margin(margin)

    def set_minimum_height(self, height):
        self.text.setMinimumHeight(height)

    def update_status_bar(self, line, col):
        self.status.showMessage(f"Line: {line} | Column: {col}")

    def update_page_label(self, current_page, total_pages):
        self.pageCountLabel.setText(f"Page {current_page} of {total_pages}")

    def toggle_toolbar(self):
        self.toolbar.setVisible(not self.toolbar.isVisible())

    def toggle_formatbar(self):
        self.formatbar.setVisible(not self.formatbar.isVisible())

    def toggle_statusbar(self):
        self.status.setVisible(not self.status.isVisible())

    # --- Dialogs ---

    def show_unsaved_changes_dialog(self):
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
        popup = QtWidgets.QMessageBox(
            QtWidgets.QMessageBox.Icon.Critical,
            title,
            message,
            QtWidgets.QMessageBox.StandardButton.Ok,
            self
        )
        popup.show()