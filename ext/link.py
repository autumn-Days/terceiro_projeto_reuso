from PyQt6 import QtGui, QtCore, QtWidgets
from PyQt6.QtCore import Qt
from bs4 import BeautifulSoup
import re

def currentHyperlink(cursor):
    cursor.select(QtGui.QTextCursor.SelectionType.WordUnderCursor)

    html_content = cursor.selection().toHtml()
    
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Grab <a> tag
    a = soup.a

    # Try to find and return a link, else None
    return a.get("href") if a else None
    
def openHyperlink(hyperlink):
    # Parse link
    link = QtCore.QUrl.fromUserInput(hyperlink)
    
    # Open url in default browser
    QtGui.QDesktopServices.openUrl(link)

def removeHyperlink(cursor):
    # This function is called when the url is already selected
    # so we can get the selected text right away
    text = cursor.selectedText()

    # Replace hyperlink with the unformatted text
    cursor.insertText(text, QtGui.QTextCharFormat())

class Link(QtWidgets.QDialog):
    
    def __init__(self, parent=None, forEditing=False):
        super().__init__(parent)

        self.parent = parent
        self.cursor = self.parent.text.textCursor()
        self.forEditing = forEditing

        self.initUI()

    def initUI(self):

        # Label and LineEdit for Hyperlink
        urlLabel = QtWidgets.QLabel("Hyperlink to:", self)
        self.urlField = QtWidgets.QLineEdit(self)

        # Label and LineEdit for text field (to display link as)
        textLabel = QtWidgets.QLabel("Display as: ", self)
        self.textField = QtWidgets.QLineEdit(self)

        if self.forEditing:
            # Set url to current link if for editing
            link = currentHyperlink(self.cursor)
            self.urlField.setText(link if link else "") 

            # And fill the text field with the current selection
            self.textField.setText(self.cursor.selectedText())
        else:
            # Set current selection as URL (if any, else empty string)
            self.urlField.setText(self.cursor.selectedText())

        # Button for inserting link
        insertButton = QtWidgets.QPushButton("Insert", self)
        insertButton.clicked.connect(self.insert)

        # Layout
        layout = QtWidgets.QGridLayout()

        layout.addWidget(urlLabel, 0, 0)
        layout.addWidget(self.urlField, 0, 1)

        layout.addWidget(textLabel, 1, 0)
        layout.addWidget(self.textField, 1, 1)

        layout.addWidget(insertButton, 2, 0, 1, 2)

        self.setLayout(layout)

        # Set fixed size (no resizing possible)
        self.setFixedSize(300, 150)
        self.move(500, 500)
        
        self.setWindowTitle("Insert hyperlink")

    def insert(self):
        # Get text from LineEdits and make use of QUrl's
        # parsing (e.g. add http:// if necessary)
        url = QtCore.QUrl.fromUserInput(self.urlField.text())
        text = self.textField.text()

        # HTML link (convert url back to parsed url string)
        link = '<a href="{}">{}</a>'.format(url.toString(), text)

        # If we need to remove the word beneath
        if self.forEditing:
            # CORREÇÃO: Enum estrito novamente
            self.cursor.select(QtGui.QTextCursor.SelectionType.WordUnderCursor)

            # Remove it
            self.cursor.removeSelectedText()
        
        # Insert this link
        self.cursor.insertHtml(link)

        # Close window after
        self.close()