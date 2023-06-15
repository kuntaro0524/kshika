import wx,sys
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.patches import Rectangle
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import cv2
from CustomEvent import myEVT_CUSTOM, EVT_CUSTOM, CustomEvent

matplotlib.use('WXAgg')

import SummaryDat

class ViewSummaryDat(wx.Panel):
    def __init__(self, parent, id, title, summary_path):
        wx.Frame.__init__(self, parent, id)

        # Summary dat
        sd = SummaryDat.SummaryDat(summary_path)

        # CSVファイルを読む
        df = sd.makePlotData()

        width = df['fast_index'].max()*4 + 1
        height = df['slow_index'].max()*4 + 1

        # width/height
        self.width_max = df['fast_index'].max()
        self.height_max = df['slow_index'].max()

        # グリッドの表示の際のアスペクト比を固定
        beamh=10.0
        beamv=15.0
        self.aspect = beamv/beamh

        # ウィンドウサイズを設定（画像のサイズ + マージン）
        super(ViewSummaryDat, self).__init__(parent, size=(width+100, height+100))
        
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
        df = sd.makePlotData()
        max_x = df['fast_index'].max() + 1
        max_y = df['slow_index'].max() + 1
        self.matrix = np.zeros((max_y, max_x))
        for _, row in df.iterrows():
            self.matrix[int(row['slow_index']), int(row['fast_index'])] = row['height']
        
        # マップ表示部分の修正
        # 縦横のグリッドのアスペクト比を固定
        self.ax1.imshow(self.matrix, cmap='hot', interpolation='none',aspect=self.aspect)

        # キーボード入力イベントのリスナーを追加
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_event)

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
        print(rect_x, rect_y)
        height = self.matrix[rect_y, rect_x]
        print("CLICK:",rect_x, rect_y,height)

        #-q: Rectangleの最初の座標は何を示している？
        #-a: 左下の座標を示している 
        #-q: 次の、1,1は何を示している？
        #-a: 幅と高さを示している
        rec_startx = rect_x - 0.5
        rec_starty = rect_y - 0.5
        self.rectangle = Rectangle((rec_startx, rec_starty), 1, 1, edgecolor='blue', facecolor='none')
        self.ax1.add_patch(self.rectangle)

        import subprocess   

        if event.dblclick:
            # wx.MessageBox(f'X座標: {rect_x}\nY座標: {rect_y}\nダブルクリック！', '情報', wx.OK | wx.ICON_INFORMATION)
            print(f'X座標: {rect_x} Y座標: {rect_y} ダブルクリック！', '情報', wx.OK | wx.ICON_INFORMATION)
            # through index 
            t_index = rect_y * self.width_max + rect_x
            # カスタムイベントの定義
            evt = CustomEvent(myEVT_CUSTOM, -1, (rect_x, rect_y, t_index))
            self.GetEventHandler().ProcessEvent(evt)
        
        else:
            # wx.MessageBox(f'X座標: {rect_x}\nY座標: {rect_y}\nheight: {height}', '情報', wx.OK | wx.ICON_INFORMATION)
            print(f'X座標: {rect_x} Y座標: {rect_y} single click！', '情報', wx.OK | wx.ICON_INFORMATION)

        # キャンバスを再描画
        self.canvas.draw()

    def on_key_event(self, event):
        keycode = event.GetKeyCode()

        if hasattr(self, 'rectangle'):
            # 現在の四角形の座標を取得
            x = int(self.rectangle.get_x() + 0.5)
            y = int(self.rectangle.get_y() + 0.5)

            # 現在の四角形を削除
            self.rectangle.remove()

            # 上下左右のキーに応じて座標を移動
            if keycode == wx.WXK_UP and y > 0:
                y -= 1
            elif keycode == wx.WXK_DOWN and y < self.matrix.shape[0] - 1:
                y += 1
            elif keycode == wx.WXK_LEFT and x > 0:
                x -= 1
            elif keycode == wx.WXK_RIGHT and x < self.matrix.shape[1] - 1:
                x += 1

            # 新しい四角形を作成
            self.rectangle = Rectangle((x - 0.5, y - 0.5), 1, 1, edgecolor='blue', facecolor='none')
            self.ax1.add_patch(self.rectangle)

            #新しい座標とheightの数値を表示
            rect_y = self.matrix.shape[0] - y - 1
            height = self.matrix[rect_y, x]
            # wx.MessageBox(f'X座標: {x}\nY座標: {y}\nheight: {height}', '情報', wx.OK | wx.ICON_INFORMATION)
            print(f'X座標: {x}\nY座標: {y}\nheight: {height}', '情報', wx.OK | wx.ICON_INFORMATION)

            # through index 
            t_index = y * self.width_max + x
            # カスタムイベントの定義
            evt = CustomEvent(myEVT_CUSTOM, -1, (x, y, t_index))
            self.GetEventHandler().ProcessEvent(evt)

            # キャンバスを再描画
            self.canvas.draw()

        event.Skip()

if __name__ == "__main__":
    app = wx.App()
    summary_path = sys.argv[1]
    frame = MyFrame(None, -1, 'wxPython Heatmap', summary_path)
    frame.Show()
    app.MainLoop()