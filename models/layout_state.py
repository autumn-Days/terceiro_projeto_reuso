from PyQt6.QtCore import QObject, pyqtSignal

class LayoutState(QObject):
    """Manages visual state: Pagination, Margins, and Cursor Position"""

    page_changed = pyqtSignal(int, int)  # current, total
    cursor_position_changed = pyqtSignal(int, int)  # line, column

    def __init__(self):
        super().__init__()
        self._page_count = 0
        self._page_current = 0
        self._page_height = 841 # A4 Height approx in pixels/points
        self._document_margin = 50
        self._last_document_height = self._page_height

    @property
    def page_count(self):
        return self._page_count

    @page_count.setter
    def page_count(self, value):
        if self._page_count != value:
            self._page_count = value
            self.page_changed.emit(self._page_current, self._page_count)

    @property
    def page_current(self):
        return self._page_current

    @page_current.setter
    def page_current(self, value):
        if self._page_current != value:
            self._page_current = value
            self.page_changed.emit(self._page_current, self._page_count)

    @property
    def page_height(self):
        return self._page_height

    @property
    def document_margin(self):
        return self._document_margin

    @property
    def last_document_height(self):
        return self._last_document_height

    @last_document_height.setter
    def last_document_height(self, value):
        self._last_document_height = value

    def update_cursor(self, line, column):
        self.cursor_position_changed.emit(line, column)
        
    def update_page_info(self, current, total):
        # Evita loops infinitos de setter
        self._page_current = current
        self._page_count = total
        self.page_changed.emit(current, total)

    def reset(self):
        self.page_count = 0
        self.page_current = 0