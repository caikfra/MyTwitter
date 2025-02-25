'''
Arquivo python com todas as exeções requisitadas em mytwitter_classes.py
'''

class UJCException(Exception):
    """Exceção levantada quando o usuário já está cadastrado."""
    def __init__(self, usuario: str):
        super().__init__(f"Usuário '{usuario}' já cadastrado.")

class UNCException(Exception):
    """Exceção levantada quando o usuário não está cadastrado."""
    def __init__(self, usuario: str):
        super().__init__(f"Usuário '{usuario}' não cadastrado.")

class PEException(Exception):
    """
    Exceção levantada quando se tenta criar um perfil
    que já existe no MyTwitter.
    """
    def __init__(self, usuario: str):
        super().__init__(f"Perfil '{usuario}' já existe.")

class PIException(Exception):
    """
    Exceção levantada quando o perfil não existe no MyTwitter.
    Também pode ser usada em caso de mais de um perfil inexistente,
    caso esse cenário apareça em alguma lógica (via o parâmetro 'multiple').
    """
    def __init__(self, usuario=None, multiple=False):
        if multiple:
            super().__init__("Um ou ambos os perfis informados não existem.")
        else:
            super().__init__(f"Perfil '{usuario}' não existe.")

class PDException(Exception):
    """
    Exceção levantada quando o perfil está desativado (inativo).
    Também pode ser usada para indicar mais de um perfil desativado
    (via o parâmetro 'multiple').
    """
    def __init__(self, usuario=None, ja_desativado=False, multiple=False):
        if multiple:
            super().__init__("Um ou ambos os perfis informados estão desativados.")
        elif ja_desativado:
            super().__init__(f"Perfil '{usuario}' já está desativado.")
        else:
            super().__init__(f"Perfil '{usuario}' está desativado.")

class MFPException(Exception):
    """
    Exceção levantada quando a mensagem não está dentro
    do limite de 1 a 140 caracteres.
    """
    def __init__(self):
        super().__init__("Mensagem fora do padrão (1 a 140 caracteres).")

class SIException(Exception):
    """
    Exceção levantada quando ocorre tentativa de seguir a si mesmo
    ou um seguidor inválido.
    """
    def __init__(self):
        super().__init__("Um usuário não pode seguir a si mesmo.")
