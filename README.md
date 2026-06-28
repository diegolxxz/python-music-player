# 🎵 Python Music Player

Player de música de desktop escrito em Python, no estilo Spotify. Toca arquivos
de áudio locais e também áudios baixados do YouTube (via `yt-dlp`), organiza as
músicas em playlists e suporta os modos aleatório e repetir.

## Funcionalidades

- Reproduzir músicas locais e baixadas do YouTube
- Baixar o áudio de vídeos do YouTube e convertê-lo para mp3
- Criar e gerenciar várias playlists
- Controles de reprodução: tocar, pausar, retomar, próxima, anterior, volume
- Modo aleatório
- Modo repetir para ficar na mesma música
- Busca de músicas por título ou artista

### Relações de POO demonstradas

| Relação | Onde aparece |
|---|---|
| **Herança** | `MusicaLocal` e `MusicaYouTube` herdam de `Musica` |
| **Polimorfismo** | `diretorio_musica()` e `disponivel()` têm implementação própria em cada subclasse |
| **Composição** | `Biblioteca` cria suas `Playlist`; `Player` cria `EstadoReproducao` e `MotorAudio` |
| **Agregação** | `Playlist` apenas referencia objetos `Musica` que vivem na `Biblioteca` |
| **Associação** | `Player` aponta para uma `Playlist` externa |
| **Dependência** | `MusicaYouTube` usa um `Downloader` temporário dentro de um método |

## Estrutura do projeto

```
.
├── main.py
├── musica.py          # Musica, MusicaLocal, MusicaYouTube, Downloader
├── biblioteca.py      # Playlist, Biblioteca
├── player.py          # EstadoReproducao, MotorAudio, Player
├── menu.py            # Interface de terminal
├── repositorio.py     # RepositorioJSON — Nível 3
├── app_gui.py         # Interface gráfica — Nível 4
├── requirements.txt   # Dependências do projeto
└── README.md
```

## Instalação

### Pré-requisitos
- Python
- **FFmpeg** — necessário para o `yt-dlp` converter o áudio para mp3:
  - Windows: `winget install ffmpeg`
  - Linux: `sudo apt install ffmpeg`

### Ambiente e dependências
```bash
python -m venv venv

# Windows
venv\Scripts\activate
# Linux
source venv/bin/activate         

pip install -r requirements.txt



