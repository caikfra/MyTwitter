from datetime import datetime

def gerador_id():
    i = 1
    while True:
        yield i
        i += 1

class Tweet:
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
    
class Perfil:
    def __init__(self, nome_usuario: str):
        self.__usuario = f'@{nome_usuario}'
        self.__seguidos = []
        self.__seguidores = []
        self.__tweets = []
        self.__ativo = True

    def add_seguidor(self, perfil) -> None:
        if perfil not in self.__seguidores:
            self.__seguidores.append(perfil)

    def add_seguidos(self, perfil) -> None:
        if perfil not in self.__seguidos:
            self.__seguidos.append(perfil)
    
    def add_tweet(self, tweet) -> None:
        if tweet not in self.__tweets:
            self.__tweets.append(tweet)
    
    def get_tweets(self) -> list:
        return sorted(self.__tweets, key= lambda tweet: tweet.get.data_postagem())
    
    def get_tweet(self, tweet_id) -> str | None :
        for tweet in self.__tweets:
            if tweet_id == tweet.get_id():
                return tweet
        return None
    
    def get_timeline(self) -> list:
        timeline = self.__tweets[:]
        for seguido in self.__seguidos:
            timeline.extend(seguido.get_tweets())
        return sorted(timeline, key= lambda tweet: tweet.get_data_postagem())

    def get_usuario(self) -> str:
        return self.__usuario
    
    def set_usuario(self, novo_usuario) -> None:
        self.__usuario = novo_usuario

    def is_ativo(self) -> bool:
        return self.__ativo

    def set_ativo(self) -> None:
        self.__ativo = not self.__ativo

class PessoaFisica(Perfil):
    def __init__(self, nome_usuario, cpf: str):
        super().__init__(nome_usuario)
        self.__cpf = cpf
    
    def get_cpf(self):
        return self.__cpf

class PessoaJuridica(Perfil):
    def __init__(self, nome_usuario, cnpj: str):
        super().__init__(nome_usuario)
        self.__cnpj = cnpj
    
    def get_cpf(self):
        return self.__cnpj

class RepositorioUsuarios:
    def __init__(self):
        self.__usuarios = []

    def cadastrar(self, perfil):
        for usuario in self.__usuarios:
            if perfil.get_usuario() == usuario.get_usuario():
                raise Exception("Usuário já cadastrado.")  # mudar para (UJCException)
        self.__usuarios.append(perfil)

    def buscar(self, usuario):
        return self.__usuarios(usuario, None)
    
    

'''Perguntas:
1 Devo criar um arquivo de exceções?

'''