import wx
import ThumbPanel
import ThumbNailer
import ViewSummaryDat
from CustomEvent import myEVT_CUSTOM, EVT_CUSTOM, CustomEvent

summary_path = 'summary.dat'

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)

        self.panel = wx.Panel(self)

        self.heatmap_button = wx.Button(self.panel, label='Heatmap Operation')
        self.heatmap_display = ThumbNailer.ThumNailer(self.panel, -1,"title_name")

        self.image_button = wx.Button(self.panel, label='Image Operation')
        self.image_display = ViewSummaryDat.ViewSummaryDat(self.panel, -1, "title_name", summary_path)

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
        self.Bind(EVT_CUSTOM, self.on_custom)

    def on_custom(self, event):
        coordinates = event.GetValue()
        print("PPPPPPPPPPPPPPPPPP=",coordinates)
        self.heatmap_display.update_with_coordinates(coordinates)

if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame(None, -1, 'Double Panel Example')
    frame.Show()
    app.MainLoop()
