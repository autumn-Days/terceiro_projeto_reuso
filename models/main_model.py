from PyQt6.QtCore import QObject, pyqtSignal
from models.document_data import DocumentData
from models.layout_state import LayoutState
from models.file_service import FileService

class MainModel(QObject):
    """
    Facade Model that aggregates DocumentData, LayoutState and FileService.
    Maintains compatibility with the original Controller interface.
    """

    # Re-exposing signals for compatibility with Controller
    content_changed = pyqtSignal()
    filename_changed = pyqtSignal(str)
    saved_state_changed = pyqtSignal(bool)
    cursor_position_changed = pyqtSignal(int, int)
    page_changed = pyqtSignal(int, int)

    def __init__(self):
        super().__init__()
        
        # Sub-models
        self.doc_data = DocumentData()
        self.layout = LayoutState()
        self.io = FileService()

        # Connect internal signals to external signals (Forwarding)
        self._connect_forwarding_signals()

    def _connect_forwarding_signals(self):
        # Quando o doc_data muda, o MainModel emite o sinal para fora
        self.doc_data.content_changed.connect(self.content_changed.emit)
        self.doc_data.filename_changed.connect(self.filename_changed.emit)
        self.doc_data.saved_state_changed.connect(self.saved_state_changed.emit)
        
        # Quando o layout muda, emite para fora
        self.layout.cursor_position_changed.connect(self.cursor_position_changed.emit)
        self.layout.page_changed.connect(self.page_changed.emit)

    # --- Property Proxies (Delegation) ---
    
    # Document Data Delegates
    @property
    def filename(self): return self.doc_data.filename
    @filename.setter
    def filename(self, value): self.doc_data.filename = value

    @property
    def content(self): return self.doc_data.content
    @content.setter
    def content(self, value): self.doc_data.content = value

    @property
    def changes_saved(self): return self.doc_data.changes_saved
    @changes_saved.setter
    def changes_saved(self, value): self.doc_data.changes_saved = value

    # Layout State Delegates
    @property
    def page_count(self): return self.layout.page_count
    @page_count.setter
    def page_count(self, value): self.layout.page_count = value

    @property
    def page_current(self): return self.layout.page_current
    @page_current.setter
    def page_current(self, value): self.layout.page_current = value

    @property
    def page_height(self): return self.layout.page_height

    @property
    def document_margin(self): return self.layout.document_margin

    @property
    def last_document_height(self): return self.layout.last_document_height
    @last_document_height.setter
    def last_document_height(self, value): self.layout.last_document_height = value

    # --- Business Logic (Using Sub-modules) ---

    def load_from_file(self, filename):
        # 1. Usa o serviço de IO para ler
        content = self.io.load(filename)
        
        # 2. Atualiza o estado do documento
        self.doc_data.filename = filename
        self.doc_data.content = content # Isso dispara content_changed
        self.doc_data.changes_saved = True # Força saved=True após carregar
        
        return content

    def save_to_file(self, content, filename=None):
        target_filename = filename if filename else self.doc_data.filename
        
        # 1. Usa o serviço de IO para salvar
        saved_filename = self.io.save(target_filename, content)
        
        # 2. Atualiza o estado
        self.doc_data.filename = saved_filename
        self.doc_data.changes_saved = True

    def update_cursor_position(self, line, column):
        self.layout.update_cursor(line, column)

    def update_page_info(self, current_page, total_pages):
        self.layout.update_page_info(current_page, total_pages)

    def reset(self):
        self.doc_data.reset()
        self.layout.reset()