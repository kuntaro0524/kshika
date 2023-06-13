import wx
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.patches import Rectangle
from matplotlib.figure import Figure
import pandas as pd
import numpy as np

matplotlib.use('WXAgg')

class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title)

        self.panel = wx.Panel(self)
        self.fig = Figure()
        self.ax1 = self.fig.add_subplot(111)
        self.canvas = FigureCanvas(self.panel, -1, self.fig)

        self.map_section = wx.BoxSizer(wx.HORIZONTAL)
        self.map_section.Add(self.canvas, 1, flag=wx.LEFT | wx.TOP | wx.GROW)
        
        self.size_ctrl = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.max_ctrl = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.button = wx.Button(self.panel, label='実行')

        self.operation_section = wx.BoxSizer(wx.HORIZONTAL)
        self.operation_section.Add(wx.StaticText(self.panel, label='サイズ:'))
        self.operation_section.Add(self.size_ctrl)
        self.operation_section.Add(wx.StaticText(self.panel, label='最大個数:'))
        self.operation_section.Add(self.max_ctrl)
        self.operation_section.Add(self.button)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.map_section, 1, flag=wx.EXPAND)
        self.sizer.Add(self.operation_section, 0, flag=wx.EXPAND)

        self.panel.SetSizerAndFit(self.sizer)  

        self.Bind(wx.EVT_BUTTON, self.on_button)
        self.canvas.mpl_connect('button_press_event', self.on_click)

        # データの読み込み
        # マップデータ読み込み部分の修正
        df = pd.read_csv('map_data.csv')
        max_x = df['x'].max() + 1
        max_y = df['y'].max() + 1
        self.matrix = np.zeros((max_y, max_x))
        for _, row in df.iterrows():
            self.matrix[int(row['y']), int(row['x'])] = row['height']
        
        # マップ表示部分の修正
        self.ax1.imshow(self.matrix, cmap='hot', interpolation='none')

    def on_button(self, event):
        size = self.size_ctrl.GetValue()
        max_num = self.max_ctrl.GetValue()
        wx.MessageBox(f'サイズ: {size}\n最大個数: {max_num}', '情報', wx.OK | wx.ICON_INFORMATION)


    def on_click(self, event):
        # 前回描画した長方形を削除
        if hasattr(self, 'rectangle'):
            self.rectangle.remove()
        
        # マップ上でクリックした位置を取得し、四角形を作成
        rect_x = round(event.xdata)
        rect_y = round(event.ydata)
        self.rectangle = Rectangle((rect_x, rect_y), 1, 1, edgecolor='blue', facecolor='none')
        self.ax1.add_patch(self.rectangle)
    
        if event.dblclick:
            # wx.MessageBox(f'X座標: {rect_x}\nY座標: {rect_y}\nダブルクリック！', '情報', wx.OK | wx.ICON_INFORMATION)
            print(f'X座標: {rect_x}\nY座標: {rect_y}\nダブルクリック！', '情報', wx.OK | wx.ICON_INFORMATION)
        else:
            height = self.matrix[rect_y, rect_x]
            # wx.MessageBox(f'X座標: {rect_x}\nY座標: {rect_y}\nheight: {height}', '情報', wx.OK | wx.ICON_INFORMATION)
            print(f'X座標: {rect_x}\nY座標: {rect_y}\nheight: {height}', '情報', wx.OK | wx.ICON_INFORMATION)
    
        # キャンバスを再描画
        self.canvas.draw()


if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame(None, -1, 'wxPython Heatmap')
    frame.Show()
    app.MainLoop()

