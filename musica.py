from abc import ABC, abstractmethod
import os
import yt_dlp
from yt_dlp.utils import sanitize_filename


class Musica(ABC):
    def __init__(self, titulo, artista, duracao):
        self._titulo = titulo
        self._artista = artista
        self._duracao = duracao

    @property
    def titulo(self):
        return self._titulo

    @property
    def artista(self):
        return self._artista

    @property
    def duracao(self):
        return self._duracao

    @abstractmethod
    def diretorio_musica(self):
        pass

    @abstractmethod
    def disponivel(self):
        pass

    def __str__(self):
        minutos, segundos = divmod(self._duracao, 60)
        return f"{self._titulo} - {self._artista} ({minutos}:{segundos:02d})"


class MusicaLocal(Musica):
    def __init__(self, titulo, artista, duracao, caminho_arquivo):
        super().__init__(titulo, artista, duracao)
        self._caminho_arquivo = caminho_arquivo

    def diretorio_musica(self):
        return self._caminho_arquivo

    def disponivel(self):
        return os.path.exists(self._caminho_arquivo)


class MusicaYouTube(Musica):
    def __init__(self, titulo, artista, duracao, url, caminho_cache=None):
        super().__init__(titulo, artista, duracao)
        self._url = url
        self._caminho_cache = caminho_cache

    def diretorio_musica(self):
        if self._caminho_cache is None or not os.path.exists(self._caminho_cache):
            downloader = Downloader()
            self._caminho_cache = downloader.baixar(
                self._url, nome=f"{self._artista} - {self._titulo}"
            )
        return self._caminho_cache

    def disponivel(self):
        if self._caminho_cache and os.path.exists(self._caminho_cache):
            return True
        return bool(self._url)


class Downloader:
    def __init__(self, pasta_destino="musicas"):
        self._pasta_destino = pasta_destino
        os.makedirs(self._pasta_destino, exist_ok=True)

    def baixar(self, url, nome=None):
        base = sanitize_filename(nome) if nome else "%(id)s"
        opcoes = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(self._pasta_destino, f"{base}.%(ext)s"),
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "quiet": True,
            "noplaylist": True,
        }
        with yt_dlp.YoutubeDL(opcoes) as ydl:
            info = ydl.extract_info(url, download=True)
            return os.path.splitext(ydl.prepare_filename(info))[0] + ".mp3"