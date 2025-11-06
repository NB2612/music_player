import wx

from main.UI import AudioPlayerFrame

if __name__ == "__main__":
    app = wx.App(False)
    frame = AudioPlayerFrame()
    app.MainLoop()