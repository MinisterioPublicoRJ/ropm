class OperationNotCompleteException(Exception):
    def __init__(self):
        message = "Operação deve estar completa para haver notificacão"
        super().__init__(message)
