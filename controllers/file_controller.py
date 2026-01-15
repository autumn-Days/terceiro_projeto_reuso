from PyQt6 import QtWidgets, QtPrintSupport

class FileController:
    def __init__(self, model, view, app):
        self.model = model
        self.view = view
        self.app = app
        self._connect_signals()

    def _connect_signals(self):
        # Operações em arquivos
        self.view.newAction.triggered.connect(self.new_document)
        self.view.openAction.triggered.connect(self.open_document)
        self.view.saveAction.triggered.connect(self.save_document)
        self.view.printAction.triggered.connect(self.print_document)
        self.view.previewAction.triggered.connect(self.preview_document)

    def new_document(self):
        from main_view import MainView
        from document_model import DocumentModel

        new_model = DocumentModel()
        new_view = MainView()
        new_controller = MainController(new_model, new_view, self.app)
        new_view.show()

    def open_document(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self.view, 'Open File', '.', 'Writer Files (*.writer)'
        )
        if filename:
            try:
                content = self.model.load_from_file(filename)
                self.view.text.setText(content)
            except IOError as e:
                self.view.show_error_dialog("Open Error", str(e))

    def save_document(self):
        if not self.model.filename:
            filename, _ = QtWidgets.QFileDialog.getSaveFileName(
                self.view, 'Save File', '.', 'Writer Files (*.writer)'
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
        dialog = QtPrintSupport.QPrintDialog(self.view.printer, self.view)
        if dialog.exec() == QtWidgets.QDialog.DialogCode.Accepted:
            self.view.text.document().print(self.view.printer)

    def preview_document(self):
        preview = QtPrintSupport.QPrintPreviewDialog(self.view.printer)
        preview.paintRequested.connect(lambda p: self.view.text.print(p))
        preview.exec()

    def handle_close_event(self, event):
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