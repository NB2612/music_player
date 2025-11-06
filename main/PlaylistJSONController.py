import json
import os
from PlayList import PlayList
from Composition import Composition

class PlaylistJSONController:
    """Контроллер для сохранения и загрузки плейлистов в отдельные JSON-файлы"""
    def __init__(self, folder="playlists"):
        self.folder = folder
        self.ensure_dir()

    def ensure_dir(self):
        if not os.path.exists(self.folder):
            os.makedirs(self.folder)

    def playlist_file(self, name):
        safe_name = name.replace(" ", "_")
        return os.path.join(self.folder, f"playlist_{safe_name}.json")

    def save_playlist(self, name, playlist: PlayList):
        """Сохраняет один плейлист в отдельный JSON-файл"""
        data = [{"title": c.title, "duration": c.duration, "path": c.path} for c in playlist.get_all_songs()]
        with open(self.playlist_file(name), "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def delete_playlist_file(self, name):
        """Удаляет JSON-файл плейлиста"""
        path = self.playlist_file(name)
        if os.path.exists(path):
            os.remove(path)

    def load_playlists(self):
        """Загружает все плейлисты из папки"""
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