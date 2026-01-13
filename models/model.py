from PyQt6.QtCore import QObject, pyqtSignal

class Model(QObject):
    """Model class that manages document state and data"""

    # Signals to notify observers of changes
    content_changed = pyqtSignal()
    filename_changed = pyqtSignal(str)
    saved_state_changed = pyqtSignal(bool)
    cursor_position_changed = pyqtSignal(int, int)  # line, column
    page_changed = pyqtSignal(int, int)  # current page, total pages

    def __init__(self):
        super().__init__()

        # Document data
        self._filename = ""
        self._changes_saved = True
        self._content = ""

        # Page tracking
        self._page_count = 0
        self._page_current = 0
        self._page_height = 841
        self._last_document_height = self._page_height
        self._document_margin = 50

    # Filename properties
    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        if self._filename != value:
            self._filename = value
            self.filename_changed.emit(value)

    # Saved state properties
    @property
    def changes_saved(self):
        return self._changes_saved

    @changes_saved.setter
    def changes_saved(self, value):
        if self._changes_saved != value:
            self._changes_saved = value
            self.saved_state_changed.emit(value)

    # Content properties
    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if self._content != value:
            self._content = value
            self.content_changed.emit()
            if self._changes_saved:
                self.changes_saved = False

    # Page properties
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

    # Business logic methods
    def load_from_file(self, filename):
        """Load document content from file"""
        try:
            with open(filename, "rt", encoding="utf-8") as file:
                content = file.read()
            self.filename = filename
            self._content = content
            self.changes_saved = True
            return content
        except Exception as e:
            raise IOError(f"Failed to load file: {e}")

    def save_to_file(self, content, filename=None):
        """Save document content to file"""
        if filename:
            self.filename = filename

        if not self.filename:
            raise ValueError("No filename specified")

        # Append extension if not present
        if not self.filename.endswith(".writer"):
            self.filename += ".writer"

        try:
            with open(self.filename, "wt", encoding="utf-8") as file:
                file.write(content)
            self.changes_saved = True
        except Exception as e:
            raise IOError(f"Failed to save file: {e}")

    def update_cursor_position(self, line, column):
        """Update cursor position tracking"""
        self.cursor_position_changed.emit(line, column)

    def update_page_info(self, current_page, total_pages):
        """Update page information"""
        self._page_current = current_page
        self._page_count = total_pages
        self.page_changed.emit(current_page, total_pages)

    def reset(self):
        """Reset document to initial state"""
        self._filename = ""
        self._content = ""
        self._changes_saved = True
        self._page_count = 0
        self._page_current = 0
        self.content_changed.emit()
        self.filename_changed.emit("")
        self.saved_state_changed.emit(True)