from controllers.file_controller import FileController
from controllers.format_controller import FormatController
from controllers.editor_controller import EditorController

class MainController:
    def __init__(self, model, view, app):
        self.model = model
        self.view = view
        self.app = app
        
        # Inicializa o estado visual
        self._setup_initial_state()

        # Instancia os sub-controladores
        # Eles se auto-conectam aos sinais no __init__ deles
        self.file_ctrl = FileController(model, view, app)
        self.format_ctrl = FormatController(view)
        self.editor_ctrl = EditorController(model, view, app)

        # Conexões básicas da View que não precisam de lógica complexa
        self._connect_basic_view_actions()

    def _setup_initial_state(self):
        self.view.set_document_margin(self.model.document_margin)
        self.view.set_minimum_height(self.model.page_height)
        # update_cursor_position agora pertence ao editor_ctrl, 
        # mas só podemos chamar depois de instanciá-lo, ou mover essa chamada para lá.

    def _connect_basic_view_actions(self):
        """Conecta ações simples que não requerem lógica de negócio profunda"""
        # Edit operations simples (delegadas direto para o widget de texto)
        self.view.cutAction.triggered.connect(self.view.text.cut)
        self.view.copyAction.triggered.connect(self.view.text.copy)
        self.view.pasteAction.triggered.connect(self.view.text.paste)
        self.view.undoAction.triggered.connect(self.view.text.undo)
        self.view.redoAction.triggered.connect(self.view.text.redo)

        # View toggles
        self.view.toolbarToggleAction.triggered.connect(self.view.toggle_toolbar)
        self.view.formatbarToggleAction.triggered.connect(self.view.toggle_formatbar)
        self.view.statusbarToggleAction.triggered.connect(self.view.toggle_statusbar)
    
    # Este método é chamado pela View quando o usuário tenta fechar a janela
    def handle_close_request(self, event):
        # Delega a decisão para o controlador de arquivo
        self.file_ctrl.handle_close_event(event)