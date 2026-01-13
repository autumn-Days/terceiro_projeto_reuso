"""
Main Application Entry Point
Assembles the MVC components
"""
import sys
from PyQt6 import QtWidgets

from models.model import Model
from views.view import View
from controllers.controller import Controller


class WriterApplication:
    """Main application class that initializes MVC components"""

    def __init__(self):
        # Create Qt Application
        self.app = QtWidgets.QApplication(sys.argv)

        # Create MVC components
        self.model = Model()
        self.view = View()
        self.controller = Controller(self.model, self.view, self.app)

        # Override close event to handle unsaved changes
        self.view.closeEvent = self.controller.handle_close_event

    def run(self):
        """Run the application"""
        self.view.show()
        return sys.exit(self.app.exec())


def main():
    """Application entry point"""
    writer_app = WriterApplication()
    writer_app.run()


if __name__ == "__main__":
    main()