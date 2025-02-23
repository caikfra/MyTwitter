import unittest
from datetime import datetime

from mytwitter_classes import (
    MyTwitter,
    RepositorioUsuarios,
    Perfil,
    PessoaFisica,
    PessoaJuridica,
    Tweet,
    gerador_id
)

from excecoes_mytwiiter import (
    UJCException,
    UNCException,
    PDException,
    PEException,
    PIException,
    MFPException,
    SIException
)

class TestTweet(unittest.TestCase):
    def test_tweet_creation(self):
        """Verifica se o Tweet é criado corretamente."""
        usuario = "@teste"
        mensagem = "Olá mundo!"
        tweet = Tweet(usuario, mensagem)

        self.assertEqual(tweet.get_usuario(), usuario)
        self.assertEqual(tweet.get_mensagem(), mensagem)
        self.assertIsInstance(tweet.get_data_postagem(), datetime)
        self.assertIsInstance(tweet.get_id(), int)


class TestPerfil(unittest.TestCase):
    def setUp(self):
        """Configura um perfil básico para uso nos testes."""
        self.perfil = Perfil("@alice")

    def test_criacao_perfil(self):
        """Verifica se o perfil é criado como ativo e sem seguidores/seguidos."""
        self.assertEqual(self.perfil.get_usuario(), "@alice")
        self.assertTrue(self.perfil.is_ativo())
        self.assertEqual(len(self.perfil.get_tweets()), 0)

    def test_add_seguidor(self):
        """Verifica se adicionar um seguidor funciona corretamente."""
        outro_perfil = Perfil("@bob")
        self.perfil.add_seguidor(outro_perfil)
        # Acesso forçado ao atributo privado para confirmar
        self.assertIn(outro_perfil, self.perfil._Perfil__seguidores)

    def test_add_seguidos(self):
        """Verifica se adicionar um seguido funciona corretamente."""
        outro_perfil = Perfil("@charlie")
        self.perfil.add_seguidos(outro_perfil)
        self.assertIn(outro_perfil, self.perfil._Perfil__seguidos)

    def test_add_tweet(self):
        """Verifica se adicionar tweet funciona e mantém ordenação."""
        t1 = Tweet("@alice", "Primeiro tweet")
        t2 = Tweet("@alice", "Segundo tweet")
        self.perfil.add_tweet(t2)
        self.perfil.add_tweet(t1)

        # Verifica ordenação por data de postagem
        tweets = self.perfil.get_tweets()
        # A ordem depende da data de criação; esse teste supõe que um foi criado logo após o outro.
        self.assertLessEqual(tweets[0].get_data_postagem(), tweets[1].get_data_postagem())

    def test_get_tweet_inexistente(self):
        """Verifica se retorna None ao buscar Tweet inexistente."""
        tweet_retornado = self.perfil.get_tweet(-999)
        self.assertIsNone(tweet_retornado)

    def test_timeline(self):
        """Verifica se a timeline retorna tweets do próprio perfil + seguidos."""
        outro_perfil = Perfil("@bob")
        self.perfil.add_seguidos(outro_perfil)

        t1 = Tweet("@alice", "Tweet da Alice")
        t2 = Tweet("@bob", "Tweet do Bob")

        self.perfil.add_tweet(t1)
        outro_perfil.add_tweet(t2)

        timeline = self.perfil.get_timeline()
        self.assertEqual(len(timeline), 2)
        # Ordenados por data
        self.assertIn(t1, timeline)
        self.assertIn(t2, timeline)


class TestPessoaFisica(unittest.TestCase):
    def test_criacao_pessoafisica(self):
        """Verifica se a PessoaFisica herda corretamente de Perfil e guarda cpf."""
        pf = PessoaFisica("@maria", "111.222.333-44")
        self.assertEqual(pf.get_usuario(), "@maria")
        self.assertEqual(pf.get_cpf(), "111.222.333-44")
        self.assertTrue(pf.is_ativo())


class TestPessoaJuridica(unittest.TestCase):
    def test_criacao_pessoajuridica(self):
        """Verifica se a PessoaJuridica herda corretamente de Perfil e guarda cnpj."""
        pj = PessoaJuridica("@empresa", "12.345.678/0001-99")
        self.assertEqual(pj.get_usuario(), "@empresa")
        self.assertEqual(pj.get_cnpj(), "12.345.678/0001-99")
        self.assertTrue(pj.is_ativo())


class TestRepositorioUsuarios(unittest.TestCase):
    def setUp(self):
        self.repo = RepositorioUsuarios()

    def test_cadastrar_e_buscar(self):
        """Verifica se é possível cadastrar e buscar um perfil."""
        perfil = Perfil("@teste")
        self.repo.cadastrar(perfil)
        encontrado = self.repo.buscar("@teste")
        self.assertIsNotNone(encontrado)
        self.assertEqual(encontrado, perfil)

    def test_cadastrar_usuario_ja_existente(self):
        """Verifica se tentar cadastrar usuário duplicado levanta UJCException."""
        perfil1 = Perfil("@teste")
        perfil2 = Perfil("@teste")
        self.repo.cadastrar(perfil1)
        with self.assertRaises(UJCException):
            self.repo.cadastrar(perfil2)

    def test_atualizar_usuario_inexistente(self):
        """Verifica se atualizar usuário inexistente levanta UNCException."""
        perfil = Perfil("@inexistente")
        with self.assertRaises(UNCException):
            self.repo.atualizar(perfil)

    def test_atualizar_usuario_existente(self):
        """Verifica se atualizar usuário existente substitui corretamente o objeto na lista."""
        perfil = Perfil("@teste")
        self.repo.cadastrar(perfil)
        perfil.set_ativo(False)
        self.repo.atualizar(perfil)
        atualizado = self.repo.buscar("@teste")
        self.assertFalse(atualizado.is_ativo())


class TestMyTwitter(unittest.TestCase):
    def setUp(self):
        self.repo = RepositorioUsuarios()
        self.sistema = MyTwitter(self.repo)

    def test_criar_perfil_duplicado(self):
        """Verifica se criar_perfil levanta PEException ao duplicar."""
        pf = PessoaFisica("@joao", "000.000.000-00")
        self.sistema.criar_perfil(pf)
        with self.assertRaises(PEException):
            self.sistema.criar_perfil(pf)  # mesmo usuário

    def test_cancelar_perfil_inexistente(self):
        """Verifica se cancelar_perfil levanta PIException com usuário inexistente."""
        with self.assertRaises(PIException):
            self.sistema.cancelar_perfil("@naoexiste")

    def test_cancelar_perfil_ja_desativado(self):
        """Verifica se cancelar_perfil levanta PDException ao desativar um perfil já inativo."""
        pf = PessoaFisica("@ana", "123.456.789-00")
        self.sistema.criar_perfil(pf)
        # Primeiro desativa
        self.sistema.cancelar_perfil("@ana")
        # Tenta desativar novamente
        with self.assertRaises(PDException):
            self.sistema.cancelar_perfil("@ana")

    def test_tweetar_perfil_inexistente(self):
        """Verifica se tweetar com perfil inexistente levanta PIException."""
        with self.assertRaises(PIException):
            self.sistema.tweetar("@naoexiste", "Mensagem válida")

    def test_tweetar_perfil_inativo(self):
        """Verifica se tweetar com perfil inativo levanta PDException."""
        pf = PessoaFisica("@joana", "999.888.777-66")
        self.sistema.criar_perfil(pf)
        self.sistema.cancelar_perfil("@joana")
        with self.assertRaises(PDException):
            self.sistema.tweetar("@joana", "Alguma coisa")

    def test_tweetar_mensagem_fora_do_padrao(self):
        """Verifica se tweetar mensagem fora de 1..140 levanta MFPException."""
        pf = PessoaFisica("@carlos", "111.222.333-44")
        self.sistema.criar_perfil(pf)

        with self.assertRaises(MFPException):
            self.sistema.tweetar("@carlos", "")  # vazio

        with self.assertRaises(MFPException):
            self.sistema.tweetar("@carlos", "X" * 141)  # > 140 chars

    def test_timeline_ok(self):
        """Verifica se a timeline funciona com perfis ativos."""
        pf1 = PessoaFisica("@perfil1", "111.222.333-01")
        pf2 = PessoaFisica("@perfil2", "111.222.333-02")
        self.sistema.criar_perfil(pf1)
        self.sistema.criar_perfil(pf2)

        # pf1 segue pf2
        self.sistema.seguir("@perfil1", "@perfil2")
        # pf1 tweeta
        self.sistema.tweetar("@perfil1", "Olá, eu sou o Perfil1!")
        # pf2 tweeta
        self.sistema.tweetar("@perfil2", "Eu sou o Perfil2!")

        timeline_p1 = self.sistema.timeline("@perfil1")
        self.assertEqual(len(timeline_p1), 2)  # tweets de pf1 + pf2

    def test_timeline_perfil_inexistente(self):
        with self.assertRaises(PIException):
            self.sistema.timeline("@naoexiste")

    def test_timeline_perfil_inativo(self):
        pf = PessoaFisica("@perfil3", "111.222.333-03")
        self.sistema.criar_perfil(pf)
        # Desativa
        self.sistema.cancelar_perfil("@perfil3")
        with self.assertRaises(PDException):
            self.sistema.timeline("@perfil3")

    def test_seguir_mesmo_usuario(self):
        pf = PessoaFisica("@exemplo", "123.456.789-00")
        self.sistema.criar_perfil(pf)
        with self.assertRaises(SIException):
            self.sistema.seguir("@exemplo", "@exemplo")

    def test_seguir_perfil_inexistente(self):
        pf = PessoaFisica("@exemplo2", "123.456.789-00")
        self.sistema.criar_perfil(pf)
        with self.assertRaises(PIException):
            self.sistema.seguir("@exemplo2", "@naoexiste")

    def test_seguir_perfil_inativo(self):
        pf = PessoaFisica("@exemplo3", "123.456.789-00")
        pf2 = PessoaFisica("@exemplo4", "987.654.321-00")
        self.sistema.criar_perfil(pf)
        self.sistema.criar_perfil(pf2)
        # desativa pf2
        self.sistema.cancelar_perfil("@exemplo4")
        with self.assertRaises(PDException):
            self.sistema.seguir("@exemplo3", "@exemplo4")

    def test_seguidores(self):
        pf = PessoaFisica("@exemplo5", "123.456.789-10")
        pf2 = PessoaFisica("@exemplo6", "123.456.789-11")
        self.sistema.criar_perfil(pf)
        self.sistema.criar_perfil(pf2)

        # pf2 segue pf
        self.sistema.seguir("@exemplo6", "@exemplo5")
        num_seg = self.sistema.num_seguidores("@exemplo5")
        self.assertEqual(num_seg, 1)

    def test_seguidores_perfil_inexistente(self):
        with self.assertRaises(PIException):
            self.sistema.seguidores("@naoexiste")

    def test_seguidores_perfil_inativo(self):
        pf = PessoaFisica("@exemplo7", "123.456.789-12")
        self.sistema.criar_perfil(pf)
        self.sistema.cancelar_perfil("@exemplo7")
        with self.assertRaises(PDException):
            self.sistema.seguidores("@exemplo7")

    def test_seguidores_e_seguidos(self):
        pf1 = PessoaFisica("@teste1", "000.000.000-00")
        pf2 = PessoaFisica("@teste2", "111.111.111-11")
        pf3 = PessoaFisica("@teste3", "222.222.222-22")
        self.sistema.criar_perfil(pf1)
        self.sistema.criar_perfil(pf2)
        self.sistema.criar_perfil(pf3)

        # pf2 e pf3 seguem pf1
        self.sistema.seguir("@teste2", "@teste1")
        self.sistema.seguir("@teste3", "@teste1")

        segs = self.sistema.seguidores("@teste1")
        num_segs = self.sistema.num_seguidores("@teste1")
        self.assertEqual(num_segs, 2)  # pf2 e pf3
        self.assertIn(pf2, segs)
        self.assertIn(pf3, segs)

        # pf2 segue pf3
        self.sistema.seguir("@teste2", "@teste3")
        seguidos_p2 = self.sistema.seguidos("@teste2")
        self.assertEqual(len(seguidos_p2), 2)  # pf1 e pf3

    def test_seguidores_inexistente(self):
        with self.assertRaises(PIException):
            self.sistema.seguidores("@xexiste")

    def test_seguidores_inativo(self):
        pf = PessoaFisica("@teste4", "333.333.333-33")
        self.sistema.criar_perfil(pf)
        self.sistema.cancelar_perfil("@teste4")
        with self.assertRaises(PDException):
            self.sistema.seguidores("@teste4")

    def test_seguidos_inexistente(self):
        with self.assertRaises(PIException):
            self.sistema.seguidos("@invalido")

    def test_seguidos_inativo(self):
        pf = PessoaFisica("@teste5", "444.444.444-44")
        self.sistema.criar_perfil(pf)
        self.sistema.cancelar_perfil("@teste5")
        with self.assertRaises(PDException):
            self.sistema.seguidos("@teste5")


if __name__ == "__main__":
    unittest.main()
