from datetime import datetime
from excecoes_mytwiiter import UJCException, UNCException, PDException, PEException, PIException, MFPException, SIException

'''
Arquivo python com todas as classes de Mytwitter
'''

def gerador_id():
    """
    Função geradora responsável por fornecer IDs únicos
    para cada Tweet. Deve ser utilizada com a função next().
    """
    i = 1
    while True:
        yield i
        i += 1

class Tweet:
    """
    Classe que representa um Tweet.
    """
    def __init__(self, nome_usuario: str, texto: str):
        self.__id = next(gerador_id())
        self.__usuario = nome_usuario
        self.__mensagem = texto
        self.__data_postagem = datetime.today()
    
    def get_id(self) -> int:
        return self.__id

    def get_usuario(self) -> str:
        return self.__usuario

    def get_mensagem(self) -> str:
        return self.__mensagem

    def get_data_postagem(self) -> datetime:
        return self.__data_postagem
    
    def __str__(self):
        return f"Tweet(ID: {self.__id}, Usuário: {self.__usuario}, Mensagem: {self.__mensagem}, Data: {self.__data_postagem})"
    
    
class Perfil:
    """
    Classe que representa um perfil de usuário no MyTwitter.
    """
    def __init__(self, nome_usuario: str):
        self.__usuario = nome_usuario
        self.__seguidos = []
        self.__seguidores = []
        self.__tweets = []
        self.__ativo = True

    def add_seguidor(self, perfil: 'Perfil') -> None:
        if perfil not in self.__seguidores:
            self.__seguidores.append(perfil)

    def add_seguidos(self, perfil: 'Perfil') -> None:
        if perfil not in self.__seguidos:
            self.__seguidos.append(perfil)
    
    def get_seguidores(self) -> list:
        return self.__seguidores

    def get_seguidos(self) -> list:
        return self.__seguidos

    def add_tweet(self, tweet: 'Tweet') -> None:
        if tweet not in self.__tweets:
            self.__tweets.append(tweet)
    
    def get_tweets(self) -> list[Tweet]:
        return sorted(self.__tweets, key=lambda tweet: tweet.get_data_postagem())
    
    def get_tweet(self, tweet_id: int) -> 'Tweet | None':
        for tweet in self.__tweets:
            if tweet_id == tweet.get_id():
                return tweet
        return None
    
    def get_timeline(self) -> list[Tweet]:
        timeline = self.__tweets[:]
        for seguido in self.__seguidos:
            timeline.extend(seguido.get_tweets())
        return sorted(timeline, key=lambda tweet: tweet.get_data_postagem())

    def get_usuario(self) -> str:
        return self.__usuario
    
    def set_usuario(self, novo_usuario: str) -> None:
        self.__usuario = novo_usuario

    def is_ativo(self) -> bool:
        return self.__ativo

    def set_ativo(self, ativo: bool) -> None:
        self.__ativo = ativo
    
    def __str__(self):
        return f"Perfil({self.__usuario}, Seguidores: {len(self.__seguidores)}, Seguidos: {len(self.__seguidos)}, Ativo: {self.__ativo})"

    
    
class PessoaFisica(Perfil):
    """
    Subclasse de perfil.
    """
    def __init__(self, nome_usuario: str, cpf: str):
        super().__init__(nome_usuario)
        self.__cpf = cpf
    
    def get_cpf(self) -> str:
        return self.__cpf

    def __str__(self):
        return f"Pessoa Física({self.get_usuario()}, CPF: {self.__cpf})"

class PessoaJuridica(Perfil):
    """
    Subclasse de perfil.
    """
    def __init__(self, nome_usuario: str, cnpj: str):
        super().__init__(nome_usuario)
        self.__cnpj = cnpj
    
    def get_cnpj(self) -> str:
        return self.__cnpj
    
    def __str__(self):
        return f"Pessoa Jurídica({self.get_usuario()}, CNPJ: {self.__cnpj})"
class RepositorioUsuarios:
    """
    Classe que gerencia o armazenamento de perfis.
    """
    def __init__(self):
        self.__usuarios = []

    def cadastrar(self, perfil: 'Perfil') -> None:
        for usuario in self.__usuarios:
            if perfil.get_usuario() == usuario.get_usuario():
                raise UJCException(perfil.get_usuario())
        self.__usuarios.append(perfil)

    def buscar(self, nome_usuario: str) -> 'Perfil | None':
        for usuario in self.__usuarios:
            if usuario.get_usuario() == nome_usuario:
                return usuario
        return None
    
    def atualizar(self, perfil: 'Perfil') -> None:
        for indice, usuario in enumerate(self.__usuarios):
            if perfil.get_usuario() == usuario.get_usuario():
                self.__usuarios[indice] = perfil
                return None
        raise UNCException(perfil.get_usuario())
    
    def __str__(self):
        return f"Repositório de Usuários({len(self.__usuarios)} perfis cadastrados)"

class MyTwitter:
    """
    Classe que faz as operações nos perfis do repositório
    """
    def __init__(self, repositorio_usuarios: 'RepositorioUsuarios'): 
        self.__repositorio = repositorio_usuarios

    def criar_perfil(self, perfil: 'Perfil') -> None:
        if self.__repositorio.buscar(perfil.get_usuario()) is not None:
            raise PEException(perfil.get_usuario())
        self.__repositorio.cadastrar(perfil)

    def cancelar_perfil(self, usuario: str) -> None:
        perfil = self.__repositorio.buscar(usuario)
        if perfil is None:
            raise PIException(usuario)
        if not perfil.is_ativo():
            raise PDException(usuario)
        perfil.set_ativo(False)

    def tweetar(self, usuario: str, mensagem: str) -> None:
        perfil = self.__repositorio.buscar(usuario)
        if perfil is None:
            raise PIException(usuario)
        if not perfil.is_ativo():
            raise PDException(usuario)
        if not (1 <= len(mensagem) <= 140):
            raise MFPException()
        tweet = Tweet(usuario, mensagem)
        perfil.add_tweet(tweet)

    def timeline(self, usuario: str) -> list:
        perfil = self.__repositorio.buscar(usuario)
        if perfil is None:
            raise PIException(usuario)
        if not perfil.is_ativo():
            raise PDException(usuario)
        return perfil.get_timeline()

    def tweets(self, usuario: str) -> list:
        perfil = self.__repositorio.buscar(usuario)
        if perfil is None:
            raise PIException(usuario)
        if not perfil.is_ativo():
            raise PDException(usuario)
        return perfil.get_tweets()

    def seguir(self, seguidor: str, seguido: str) -> None:
        perfil_seguidor = self.__repositorio.buscar(seguidor)
        perfil_seguido = self.__repositorio.buscar(seguido)
        if perfil_seguidor is None:
            raise PIException(seguidor)
        if perfil_seguido is None:
            raise PIException(seguido)
        if not perfil_seguido.is_ativo():
            raise PDException(seguido)
        if not perfil_seguidor.is_ativo():
            raise PDException(seguidor)
        if seguidor == seguido:
            raise SIException()
        perfil_seguidor.add_seguidos(perfil_seguido)
        perfil_seguido.add_seguidor(perfil_seguidor)

    def num_seguidores(self, usuario: str) -> int:
        perfil = self.__repositorio.buscar(usuario)
        if perfil is None:
            raise PIException(usuario)
        if not perfil.is_ativo():
            raise PDException(usuario)
        return len(perfil.get_seguidores())

    def seguidores(self, usuario: str) -> int:
        perfil = self.__repositorio.buscar(usuario)
        if perfil is None:
            raise PIException(usuario)
        if not perfil.is_ativo():
            raise PDException(usuario)
        return perfil.get_seguidores()  

    def seguidos(self, usuario: str) -> int:
        perfil = self.__repositorio.buscar(usuario)
        if perfil is None:
            raise PIException(usuario)
        if not perfil.is_ativo():
            raise PDException(usuario)
        return perfil.get_seguidos()