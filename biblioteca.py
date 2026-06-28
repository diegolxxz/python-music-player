<<<<<<< HEAD
class Playlist:
    def __init__(self, nome):
        self._nome = nome
        self._musicas = []

    @property
    def nome(self):
        return self._nome

    def adicionar(self, musica):
        self._musicas.append(musica)

    def remover(self, musica):
        if musica in self._musicas:
            self._musicas.remove(musica)

    def listar_musicas(self):
        return self._musicas

    def tamanho(self):
        return len(self._musicas)

    def __str__(self):
        return f"Playlist '{self._nome}' ({self.tamanho()} músicas)"

class Biblioteca:
    def __init__(self):
        self._musicas = []
        self._playlists = []

    def adicionar_musica(self, musica):
        self._musicas.append(musica)

    def listar_musicas(self):
        return self._musicas

    def criar_playlist(self, nome):
        playlist = Playlist(nome)
        self._playlists.append(playlist)
        return playlist

    def remover_playlist(self, playlist):
        if playlist in self._playlists:
            self._playlists.remove(playlist)

    def listar_playlists(self):
        return self._playlists

    def buscar(self, busca):
        busca = busca.lower()
        return [m for m in self._musicas
                if busca in m.titulo.lower() or busca in m.artista.lower()]

