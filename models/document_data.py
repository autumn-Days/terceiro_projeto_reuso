from PyQt6.QtCore import QObject, pyqtSignal

class DocumentData(QObject):
    """Manages the core data of the document (Filename, Content, Dirty State)"""
    
    filename_changed = pyqtSignal(str)
    content_changed = pyqtSignal()
    saved_state_changed = pyqtSignal(bool)

    def __init__(self):
        super().__init__()
        self._filename = ""
        self._content = ""
        self._changes_saved = True

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        if self._filename != value:
            self._filename = value
            self.filename_changed.emit(value)

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if self._content != value:
            self._content = value
            self.content_changed.emit()
            # Se o conteúdo mudou, o arquivo não está salvo (exceto se for o carregamento inicial)
            if self._changes_saved:
                self.changes_saved = False

    @property
    def changes_saved(self):
        return self._changes_saved

    @changes_saved.setter
    def changes_saved(self, value):
        if self._changes_saved != value:
            self._changes_saved = value
            self.saved_state_changed.emit(value)

    def reset(self):
        self.filename = ""
        self.content = ""
        self.changes_saved = True