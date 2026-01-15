from PyQt6 import QtGui, QtCore, QtWidgets, QtPrintSupport

class EditorView(QtWidgets.QWidget):
    """
    Component responsible for the document area:
    TextEdit, ScrollArea, and Page Layout.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.printer = None
        self.text = None
        self.scroll_area = None
        self._init_ui()

    def _init_ui(self):
        # Printer setup
        self.printer = QtPrintSupport.QPrinter()
        self.printer.setPageMargins(
            QtCore.QMarginsF(0, 0, 0, 0),
            QtGui.QPageLayout.Unit.Point
        )

        # Text editor configuration
        self.text = QtWidgets.QTextEdit(self)
        self.text.setStyleSheet("background-color: #FFFFFF;")
        self.text.setFrameShape(QtWidgets.QFrame.Shape.NoFrame)
        self.text.setFixedWidth(595) # A4 width approximation
        self.text.setTabStopDistance(33)
        self.text.setVerticalScrollBarPolicy(
            QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        # Document settings
        doc = self.text.document()
        doc.setPageSize(QtCore.QSizeF(595, 841)) # A4 Height

        # Container styling
        container = QtWidgets.QWidget(self)
        container.setStyleSheet("background-color: #A0A0A0;")

        # Layout inside the gray container
        layout = QtWidgets.QGridLayout(container)
        layout.addWidget(QtWidgets.QWidget(), 0, 0) # Spacer
        layout.addWidget(self.text, 1, 0)
        container.setLayout(layout)

        # Main Layout for this component (ScrollArea)
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        self.scroll_area = QtWidgets.QScrollArea(self)
        self.scroll_area.setWidget(container)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setAlignment(QtCore.Qt.AlignmentFlag.AlignHCenter)
        
        main_layout.addWidget(self.scroll_area)

    def set_document_margin(self, margin):
        doc = self.text.document()
        rootFrame = doc.rootFrame()
        fmt = rootFrame.frameFormat()
        fmt.setMargin(margin)
        rootFrame.setFrameFormat(fmt)