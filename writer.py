import sys
from PyQt6.QtWidgets import QApplication

# Importando os módulos que criamos anteriormente
from main_model import MainModel
from main_view import MainView
from main_controller import MainController

def main():
    #Criação de uma aplicação Qt
    app = QApplication(sys.argv)
    app.setApplicationName("Writer")

    #Instanciação do model
    model = MainModel()

    #Instanciação do View, ou seja, parte de visualização
    view = MainView()

    #Instanciação do Controller, que irá orquestrar o view e o controller
    controller = MainController(model, view, app)

    #Mostra a janela e inicia o loop
    view.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()