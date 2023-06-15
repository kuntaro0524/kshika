import wx
import ThumbPanel
import ThumbNailer
class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)

        self.panel = wx.Panel(self)

        self.heatmap_button = wx.Button(self.panel, label='Heatmap Operation')
        self.heatmap_display = ThumbNailer.ThumNailer(self.panel, -1,"title_name")

        self.image_button = wx.Button(self.panel, label='Image Operation')
        self.image_display = ThumbPanel.ThumbPanel(self.panel, -1, 'koala.jpeg')  # ここを変更

        self.heatmap_sizer = wx.BoxSizer(wx.VERTICAL)
        self.heatmap_sizer.Add(self.heatmap_button, 0, flag=wx.EXPAND)
        self.heatmap_sizer.Add(self.heatmap_display, 1, flag=wx.EXPAND)

        self.image_sizer = wx.BoxSizer(wx.VERTICAL)
        self.image_sizer.Add(self.image_button, 0, flag=wx.EXPAND)
        self.image_sizer.Add(self.image_display, 1, flag=wx.EXPAND)

        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer.Add(self.heatmap_sizer, 1, flag=wx.EXPAND | wx.ALL, border=5)
        self.main_sizer.Add(self.image_sizer, 1, flag=wx.EXPAND | wx.ALL, border=5)

        self.panel.SetSizerAndFit(self.main_sizer) 


if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame(None, -1, 'Double Panel Example')
    frame.Show()
    app.MainLoop()
