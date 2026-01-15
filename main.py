"""
Main Application Entry Point
Assembles the MVC components
"""
import sys
from PyQt6 import QtWidgets

# Ajuste 1: Importando as classes com os nomes corretos definidos anteriormente
from models.main_model import MainModel
from views.main_view import MainView
from controllers.main_controller import MainController

class WriterApplication:
    """Main application class that initializes MVC components"""

    def __init__(self):
        # Create Qt Application
        self.app = QtWidgets.QApplication(sys.argv)
        self.app.setApplicationName("Writer")

        # Create MVC components
        # Ajuste 2: Instanciando as classes Facade corretas
        self.model = MainModel()
        self.view = MainView()
        
        # A Injeção de Dependência acontece aqui:
        self.controller = MainController(self.model, self.view, self.app)

        # Override close event to handle unsaved changes
        # Ajuste 3: Conectando ao método que criamos no MainController
        # Isso faz com que, ao clicar no X da janela, o Controller decida o que fazer
        self.view.closeEvent = self.controller.handle_close_request

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