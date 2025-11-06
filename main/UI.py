import wx
import wx.adv
from pygame import mixer

from Composition import Composition
from PlayList import PlayList
from PlayerController import PlayerController
from PlaylistJSONController import PlaylistJSONController

class AudioPlayerFrame(wx.Frame):
    def __init__(self, parent=None, title="🎵 Audio Player", size=(600, 600)):
        super().__init__(parent, title=title, size=size)


        self.SetBackgroundColour(wx.Colour(240, 240, 240))
        panel = wx.Panel(self)

        # === Контроллер и данные ===
        self.controller = PlayerController()
        self.playlists = {}  # имя плейлиста -> PlayList
        self.current_playlist = None

        self.json_controller = PlaylistJSONController()
        self.playlists = self.json_controller.load_playlists()


        # Таймер для обновления прогресса
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_progress, self.timer)
        self.timer.Start(500)  # обновление каждые 0.5 секунды

        # === Главный сайзер ===
        root_sizer = wx.BoxSizer(wx.VERTICAL)

        # ====== Верхняя панель: заголовок ======
        title_text = wx.StaticText(panel, label="Аудиоплеер", style=wx.ALIGN_CENTER)
        font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title_text.SetFont(font)

        # ====== Центральная область: списки ======
        main_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # ==== Левая колонка — Плейлисты ====
        playlist_box = wx.StaticBox(panel, label="Плейлисты")
        playlist_sizer = wx.StaticBoxSizer(playlist_box, wx.VERTICAL)
        self.playlist_list = wx.ListBox(panel)
        btn_add_playlist = wx.Button(panel, label="➕ Создать")
        btn_delete_playlist = wx.Button(panel, label="🗑 Удалить")
        pl_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        pl_btn_sizer.Add(btn_add_playlist, 1, wx.ALL, 3)
        pl_btn_sizer.Add(btn_delete_playlist, 1, wx.ALL, 3)
        playlist_sizer.Add(self.playlist_list, 1, wx.ALL | wx.EXPAND, 5)
        playlist_sizer.Add(pl_btn_sizer, 0, wx.ALL | wx.EXPAND, 5)

        # ==== Центральная колонка — Композиции ====
        composition_box = wx.StaticBox(panel, label="Композиции")
        composition_sizer = wx.StaticBoxSizer(composition_box, wx.VERTICAL)
        self.composition_list = wx.ListBox(panel)
        btn_add_track = wx.Button(panel, label="➕ Добавить")
        btn_delete_track = wx.Button(panel, label="🗑 Удалить")
        btn_up = wx.Button(panel, label="⬆ Вверх")
        btn_down = wx.Button(panel, label="⬇ Вниз")
        track_btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        track_btn_sizer.Add(btn_add_track, 1, wx.ALL, 3)
        track_btn_sizer.Add(btn_delete_track, 1, wx.ALL, 3)
        track_btn_sizer.Add(btn_up, 1, wx.ALL, 3)
        track_btn_sizer.Add(btn_down, 1, wx.ALL, 3)
        composition_sizer.Add(self.composition_list, 1, wx.ALL | wx.EXPAND, 5)
        composition_sizer.Add(track_btn_sizer, 0, wx.ALL | wx.EXPAND, 5)

        # Добавляем панели в main_sizer
        main_sizer.Add(playlist_sizer, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(composition_sizer, 2, wx.EXPAND | wx.ALL, 5)

        # ====== Нижняя панель управления ======
        control_box = wx.StaticBox(panel, label="Управление воспроизведением")
        control_sizer = wx.StaticBoxSizer(control_box, wx.VERTICAL)

        # Первая строка — кнопки управления
        button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_prev = wx.Button(panel, label="⏮")
        self.btn_play = wx.Button(panel, label="▶")
        self.btn_pause = wx.Button(panel, label="▶/⏸")
        self.btn_stop = wx.Button(panel, label="⏹")
        self.btn_next = wx.Button(panel, label="⏭")
        for b in (self.btn_prev, self.btn_play, self.btn_pause, self.btn_stop, self.btn_next):
            button_sizer.Add(b, 0, wx.ALL, 5)

        # Вторая строка — прогресс и громкость
        progress_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.progress = wx.Gauge(panel, range=100, size=wx.Size(300, 20))
        #self.volume_slider = wx.Slider(panel, value=50, minValue=0, maxValue=100,
        #                               style=wx.SL_HORIZONTAL | wx.SL_LABELS)
        progress_sizer.Add(wx.StaticText(panel, label="Прогресс:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        progress_sizer.Add(self.progress, 1, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 15)
        #progress_sizer.Add(wx.StaticText(panel, label="Громкость:"), 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)
        #progress_sizer.Add(self.volume_slider, 0, wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, 5)

        control_sizer.Add(button_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 5)
        control_sizer.Add(progress_sizer, 0, wx.EXPAND | wx.ALL, 5)

        # ====== Общая компоновка ======
        root_sizer.Add(title_text, 0, wx.ALL | wx.EXPAND, 5)
        root_sizer.Add(main_sizer, 1, wx.EXPAND | wx.ALL, 5)
        root_sizer.Add(control_sizer, 0, wx.EXPAND | wx.ALL, 10)
        panel.SetSizer(root_sizer)

        # === Привязка событий к методам интеграции ===
        btn_add_playlist.Bind(wx.EVT_BUTTON, self.on_add_playlist)
        btn_delete_playlist.Bind(wx.EVT_BUTTON, self.on_delete_playlist)
        btn_add_track.Bind(wx.EVT_BUTTON, self.on_add_composition)
        btn_delete_track.Bind(wx.EVT_BUTTON, self.on_delete_composition)
        btn_up.Bind(wx.EVT_BUTTON, self.on_move_up)
        btn_down.Bind(wx.EVT_BUTTON, self.on_move_down)
        self.btn_play.Bind(wx.EVT_BUTTON, self.on_play)
        self.btn_pause.Bind(wx.EVT_BUTTON, self.on_pause)
        self.btn_stop.Bind(wx.EVT_BUTTON, self.on_stop)
        self.btn_prev.Bind(wx.EVT_BUTTON, self.on_prev)
        self.btn_next.Bind(wx.EVT_BUTTON, self.on_next)
        self.playlist_list.Bind(wx.EVT_LISTBOX, self.on_select_playlist)

        # Подгружаем плейлисты из json
        for name in self.playlists:
            self.playlist_list.Append(name)
        self.playlist_list.SetSelection(0)

        # Принудительно вызвать обработчик выбора
        event = wx.CommandEvent(wx.wxEVT_LISTBOX, self.playlist_list.GetId())
        event.SetInt(0)
        self.on_select_playlist(event)

        self.Centre()
        self.Show()

    # === Методы интеграции с PlayList и Composition ===
    def on_add_playlist(self, event):
        dlg = wx.TextEntryDialog(self, "Введите название нового плейлиста:", "Создать плейлист")
        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue()
            if name and name not in self.playlists:
                # Создаем новый плейлист
                self.playlists[name] = PlayList()
                # Добавляем в список интерфейса
                self.playlist_list.Append(name)

                # Автоматически выбираем новый плейлист
                index = self.playlist_list.GetCount() - 1
                self.playlist_list.SetSelection(index)

                # Принудительно вызвать обработчик выбора
                event = wx.CommandEvent(wx.wxEVT_LISTBOX, self.playlist_list.GetId())
                event.SetInt(index)
                self.on_select_playlist(event)

                #Сохраняем плейлист в JSON файл
                self.json_controller.save_playlist(name, self.playlists[name])
            else: wx.MessageBox("Такой плейлист уже существует", "Ошибка", wx.OK | wx.ICON_WARNING)
        dlg.Destroy()

    def on_delete_playlist(self, event):
        sel = self.playlist_list.GetSelection()
        if sel != wx.NOT_FOUND:
            name = self.playlist_list.GetString(sel)
            del self.playlists[name]
            self.playlist_list.Delete(sel)
            self.composition_list.Clear()
            self.current_playlist = None
            self.json_controller.delete_playlist_file(name)

    def on_select_playlist(self, event):
        sel = event.GetSelection()
        if sel != wx.NOT_FOUND:
            name = self.playlist_list.GetString(sel)
            self.current_playlist = self.playlists[name]
            self.refresh_composition_list()

    def refresh_composition_list(self):
        self.composition_list.Clear()
        if self.current_playlist:
            for c in self.current_playlist.get_all_songs():
                self.composition_list.Append(c.get_title())

    def on_add_composition(self, event):
        if self.current_playlist is None:
            wx.MessageBox("Выберите плейлист!", "Ошибка", wx.OK | wx.ICON_WARNING)
            return
        with wx.FileDialog(self, "Выберите аудиофайл", wildcard="Audio files (*.mp3;*.wav)|*.mp3;*.wav",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dlg:
            if dlg.ShowModal() == wx.ID_CANCEL:
                return
            path = dlg.GetPath()
            title = path.split("\\")[-1]
            duration = mixer.Sound(path).get_length()
            comp = Composition(title, duration, path)
            # Проверка на дубли
            if any(s.get_title() == title for s in self.current_playlist.get_all_songs()):
                wx.MessageBox("Такой трек уже есть!", "Ошибка", wx.OK | wx.ICON_WARNING)
                return
            self.current_playlist.add_song(comp)
            self.composition_list.Append(comp.get_title())
            # Обновляем JSON плейлиста
            self.json_controller.save_playlist(self.playlist_list.GetString(self.playlist_list.GetSelection()),
                                               self.current_playlist)


    def on_delete_composition(self, event):
        sel = self.composition_list.GetSelection()
        if sel != wx.NOT_FOUND and self.current_playlist:
            title = self.composition_list.GetString(sel)
            for s in self.current_playlist.get_all_songs():
                if s.get_title() == title:
                    self.current_playlist.remove_song(s)
                    break
            self.composition_list.Delete(sel)

    def on_move_up(self, event):
        sel = self.composition_list.GetSelection()
        if sel > 0:
            title = self.composition_list.GetString(sel)
            self.composition_list.Delete(sel)
            self.composition_list.Insert(title, sel - 1)
            self.composition_list.SetSelection(sel - 1)

    def on_move_down(self, event):
        sel = self.composition_list.GetSelection()
        if sel != wx.NOT_FOUND and sel < self.composition_list.GetCount() - 1:
            title = self.composition_list.GetString(sel)
            self.composition_list.Delete(sel)
            self.composition_list.Insert(title, sel + 1)
            self.composition_list.SetSelection(sel + 1)

    # === Кнопки воспроизведения ===
    def on_play(self, event):
        if not self.current_playlist or not self.current_playlist.first_item:
            wx.MessageBox("Выберите плейлист с композициями!", "Ошибка", wx.OK | wx.ICON_WARNING)
            return

        sel = self.composition_list.GetSelection()

        # Если ничего не выбрано, ставим первую композицию
        if sel == wx.NOT_FOUND:
            first_comp = self.current_playlist.first_item.data
            self.current_playlist.current_node = self.current_playlist.first_item
            self.composition_list.SetSelection(0)
            self.controller.play(first_comp)
        else:
            title = self.composition_list.GetString(sel)
            for c in self.current_playlist.get_all_songs():
                if c.get_title() == title:
                    node = self.current_playlist.find_node(c)
                    self.current_playlist.current_node = node
                    self.controller.play(c)
                    break

    def on_pause(self, event):
        self.controller.pause()

    def on_stop(self, event):
        self.controller.stop()

    def on_prev(self, event):
        if not self.current_playlist or not self.current_playlist.first_item:
            return

        prev_c = self.current_playlist.previous_song()

        # Если текущий трек был первым, идем к последнему
        if not prev_c:
            self.current_playlist.current_node = self.current_playlist.last_item
            prev_c = self.current_playlist.current_node.data

        self.controller.play(prev_c)

        # Обновляем выделение в ListBox
        all_titles = [c.get_title() for c in self.current_playlist.get_all_songs()]
        index = all_titles.index(prev_c.get_title())
        self.composition_list.SetSelection(index)

    def on_next(self, event):
        if not self.current_playlist or not self.current_playlist.first_item:
            return

        next_c = self.current_playlist.next_song()

        # Если текущий трек был последним, идем к первому
        if not next_c:
            self.current_playlist.current_node = self.current_playlist.first_item
            next_c = self.current_playlist.current_node.data

        self.controller.play(next_c)

        # Обновляем выделение в ListBox
        all_titles = [c.get_title() for c in self.current_playlist.get_all_songs()]
        index = all_titles.index(next_c.get_title())
        self.composition_list.SetSelection(index)

    # === Метод обновления прогресса ===
    def update_progress(self, event):
        if self.controller.is_playing and self.controller.current_track:
            percent = self.controller.get_pos()
            self.progress.SetValue(percent)


if __name__ == "__main__":
    app = wx.App(False)
    frame = AudioPlayerFrame()
    app.MainLoop()
