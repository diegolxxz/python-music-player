import random
import pygame


class EstadoReproducao:
    def __init__(self):
        self._indice_atual = 0
        self._volume = 0.5
        self._tocando = False
        self._aleatorio = False
        self._repetir = False
        self._ordem = []
        self._pos_aleatoria = 0

    @property
    def indice_atual(self):
        return self._indice_atual

    @indice_atual.setter
    def indice_atual(self, valor):
        self._indice_atual = valor

    @property
    def volume(self):
        return self._volume

    @volume.setter
    def volume(self, valor):
        self._volume = valor

    @property
    def tocando(self):
        return self._tocando

    @tocando.setter
    def tocando(self, valor):
        self._tocando = valor

    @property
    def aleatorio(self):
        return self._aleatorio

    def alternar_aleatorio(self):
        self._aleatorio = not self._aleatorio

    @property
    def repetir(self):
        return self._repetir

    def alternar_repetir(self):
        self._repetir = not self._repetir

    def _gerar_ordem_aleatoria(self, total):
        self._ordem = list(range(total))
        random.shuffle(self._ordem)
        self._pos_aleatoria = 0

    def _mover_aleatorio(self, total, passo):
        if len(self._ordem) != total:
            self._gerar_ordem_aleatoria(total)
        else:
            self._pos_aleatoria = (self._pos_aleatoria + passo) % len(self._ordem)
        return self._ordem[self._pos_aleatoria]

    def _mover(self, total, passo):
        if total == 0:
            return 0
        elif self._repetir:
            return self._indice_atual
        elif self._aleatorio:
            self._indice_atual = self._mover_aleatorio(total, passo)
        else:
            self._indice_atual = (self._indice_atual + passo) % total
        return self._indice_atual

    def avancar_indice(self, total):
        return self._mover(total, 1)

    def retroceder_indice(self, total):
        return self._mover(total, -1)


class MotorAudio:
    def __init__(self):
        try:
            pygame.mixer.init()
            self._ativo = True
        except pygame.error:
            self._ativo = False

    def carregar(self, caminho):
        if self._ativo:
            pygame.mixer.music.load(caminho)

    def play(self):
        if self._ativo:
            pygame.mixer.music.play()

    def pause(self):
        if self._ativo:
            pygame.mixer.music.pause()

    def unpause(self):
        if self._ativo:
            pygame.mixer.music.unpause()

    def stop(self):
        if self._ativo:
            pygame.mixer.music.stop()

    def definir_volume(self, v):
        if self._ativo:
            pygame.mixer.music.set_volume(v)

    def musica_terminou(self):
        if not self._ativo:
            return True
        return not pygame.mixer.music.get_busy()


class Player:
    def __init__(self):
        self._estado = EstadoReproducao()
        self._motor = MotorAudio()
        self._playlist_atual = None

    @property
    def estado(self):
        return self._estado

    @property
    def playlist_atual(self):
        return self._playlist_atual

    def carregar_playlist(self, playlist):
        self._playlist_atual = playlist
        self._estado.indice_atual = 0

    def _musica_atual(self):
        if self._playlist_atual is None:
            return None
        musicas = self._playlist_atual.listar_musicas()
        if not musicas:
            return None
        return musicas[self._estado.indice_atual]

    def tocar(self):
        musica = self._musica_atual()
        if musica is None:
            return
        caminho = musica.diretorio_musica()
        self._motor.carregar(caminho)
        self._motor.definir_volume(self._estado.volume)
        self._motor.play()
        self._estado.tocando = True

    def pausar(self):
        self._motor.pause()
        self._estado.tocando = False

    def retomar(self):
        self._motor.unpause()
        self._estado.tocando = True

    def proxima(self):
        if self._playlist_atual is None:
            return
        self._estado.avancar_indice(self._playlist_atual.tamanho())
        self.tocar()

    def anterior(self):
        if self._playlist_atual is None:
            return
        self._estado.retroceder_indice(self._playlist_atual.tamanho())
        self.tocar()

    def definir_volume(self, v):
        self._estado.volume = v
        self._motor.definir_volume(v)

    def alternar_aleatorio(self):
        self._estado.alternar_aleatorio()

    def alternar_repetir(self):
        self._estado.alternar_repetir()