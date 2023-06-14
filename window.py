import wx
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas

class MainWindow(wx.Frame):
    def __init__(self, parent, title):
        super(MainWindow, self).__init__(parent, title=title, size=(800, 600))

        self.panel = wx.Panel(self)
        self.fig = plt.figure()

        # マップ表示セクション
        self.canvas = FigureCanvas(self.panel, -1, self.fig)

        # 操作セクション
        self.size_box = wx.TextCtrl(self.panel)
        self.max_num_box = wx.TextCtrl(self.panel)
        self.run_button = wx.Button(self.panel, label='Run')

        self.run_button.Bind(wx.EVT_BUTTON, self.on_run)

        self.sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.sizer.Add(self.canvas, 1, wx.EXPAND)
        self.sizer.Add(self.size_box, 0, wx.ALL, 5)
        self.sizer.Add(self.max_num_box, 0, wx.ALL, 5)
        self.sizer.Add(self.run_button, 0, wx.ALL, 5)

        self.panel.SetSizerAndFit(self.sizer)
        self.Show()

    def on_run(self, event):
        size = self.size_box.GetValue()
        max_num = self.max_num_box.GetValue()

        dlg = wx.MessageDialog(self, 'Size: {}, Max number: {}'.format(size, max_num), 'Info', wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

app = wx.App(False)
frame = MainWindow(None, "Main Window")
app.MainLoop()

