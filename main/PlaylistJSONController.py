import json
import os
from .Playlist import PlayList
from .composition import Composition

class PlaylistJSONController:
    """
    Контроллер для сохранения и загрузки плейлистов в отдельные JSON-файлы.

    Attributes:
        folder (str): Папка для хранения JSON-файлов плейлистов.
    """
    def __init__(self, folder="playlists"):
        """
        Инициализация контроллера.

        Создает папку для хранения файлов плейлистов, если она не существует.

        Args:
           folder (str): Папка для хранения JSON-файлов плейлистов. По умолчанию "playlists".
        """
        self.folder = folder
        self.ensure_dir()

    def ensure_dir(self):
        """
        Проверяет существование папки для хранения плейлистов и создает ее при необходимости.
        """
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    def playlist_file(self, name):
        """
        Генерирует путь к JSON-файлу плейлиста по его имени.

        Args:
            name (str): Имя плейлиста.

        Returns:
            str: Полный путь к JSON-файлу плейлиста.
        """
        safe_name = name.replace(" ", "_")
        return os.path.join(self.folder, f"playlist_{safe_name}.json")

    def save_playlist(self, name, playlist: PlayList):
        """
        Сохраняет плейлист в отдельный JSON-файл.

        Args:
            name (str): Имя плейлиста.
            playlist (PlayList): Объект плейлиста для сохранения.
        """
        data = [{"title": c.title, "duration": c.duration, "path": c.path} for c in playlist.get_all_songs()]
        with open(self.playlist_file(name), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def delete_playlist_file(self, name):
        """
        Удаляет JSON-файл плейлиста, если он существует.

        Args:
            name (str): Имя плейлиста для удаления.
        """
        path = self.playlist_file(name)
        if os.path.exists(path):
            os.remove(path)

    def load_playlists(self):
        """
        Загружает все плейлисты из папки.

        Файлы должны начинаться с "playlist_" и заканчиваться ".json".

        Returns:
            dict[str, PlayList]: Словарь, где ключ — имя плейлиста, значение — объект PlayList.
        """
        playlists = {}
        if not os.path.exists(self.folder):
            return playlists
        for filename in os.listdir(self.folder):
            if filename.startswith("playlist_") and filename.endswith(".json"):
                name = filename[9:-5].replace("_", " ")
                path = os.path.join(self.folder, filename)
                with open(path, "r", encoding="utf-8") as f:
                    tracks = json.load(f)
                pl = PlayList()
                for t in tracks:
                    comp = Composition(t["title"], t["duration"], t["path"])
                    pl.add_song(comp)
                playlists[name] = pl
        return playlists