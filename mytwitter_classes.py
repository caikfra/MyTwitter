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
        self.__usuario = nome_usuario
        self.__seguidos = []
        self.__seguidores = []
        self.__tweets = []
        self.__ativo = True

    def add_seguidor(self, perfil):
        if perfil not in self.__seguidores:
            self.__seguidores.append(perfil)

    def add_seguidos(self, perfil):
        if perfil not in self.__seguidos:
            self.__seguidos.append(perfil)
    
    def add_tweet(self, tweet):
        if tweet not in self.__tweets:
            self.__tweets.append(tweet)
    
    def get_tweets(self) -> list:
        return sorted(self.__tweets, key= lambda t: t.get.data_postagem())
    
    def get_tweet(self, tweet_id):
        for tweet in self.__tweets:
            if tweet_id == tweet.get_id():
                return tweet
        return None
    
    def get_timeline(self):
        pass

    def get_usuario(self):
        return self.__usuario
    
    def set_usuario(self, novo_usuario):
        self.__usuario = novo_usuario

    
