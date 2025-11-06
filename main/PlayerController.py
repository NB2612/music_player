from pygame import mixer

# Класс управления плеером через pygame

class PlayerController:
    """Обертка над pygame для управления музыкой"""
    def __init__(self):
        mixer.init()
        self.is_playing = False
        self.is_paused = False
        self.current_track = None

    def play(self, composition, target=0):
        """Запуск новой композиции."""
        if not composition:
            return

        try:
            mixer.music.load(composition.get_path())
            mixer.music.play(start=target)
            self.current_track = composition
            self.is_playing = True
            self.is_paused = False
        except Exception as e:
            print(f"Ошибка при воспроизведении: {e}")

    def get_pos(self):
        """Получение длинны композиции"""
        if not self.is_playing:
            return 0
        length = self.current_track.get_duration()
        pos = mixer.music.get_pos() / 1000.0
        percent = min(int(pos / length * 100), 100)
        return percent

    def stop(self):
        mixer.music.stop()
        self.is_playing = False
        self.is_paused = False
        self.current_track = None

    def pause(self):
        """Пауза и возобновление."""
        if not self.is_playing:
            return  # Нечего ставить на паузу

        if not self.is_paused:
            mixer.music.pause()
            self.is_paused = True
            return
        if self.is_paused:
            mixer.music.unpause()
            self.is_paused = False
            return

    @staticmethod
    def is_busy():
        return mixer.music.get_busy()