import wx
import cv2
import numpy as np
import os

# Your image size and file path configuration
IMG_WIDTH = 600
IMG_HEIGHT = 600
IMG_FOLDER = '/Users/kuntaro/kundev/kshika/thumbnail'

class ThumNailer(wx.Panel):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id)

        self.panel = wx.Panel(self)
        self.image_ctrl = wx.StaticBitmap(self.panel)

        # self.text_box の横幅を固定する
        self.text_box = wx.TextCtrl(self.panel, style=wx.TE_PROCESS_ENTER)
        self.text_box.SetMinSize((100, -1))
        self.text_box.Bind(wx.EVT_TEXT_ENTER, self.on_enter)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.image_ctrl, 1, wx.EXPAND)
        sizer.Add(self.text_box, 0, wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, 10)
        self.panel.SetSizerAndFit(sizer)
    
    def on_enter(self, event):
        num = int(self.text_box.GetValue())
        filename = self.find_file(num)
        if filename is not None:
            img = cv2.imread(os.path.join(IMG_FOLDER, filename))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB for wx.BitmapFromBuffer
            tile_num = (num - 1) % 100  # index within the tile
            row, col = divmod(tile_num, 10)
            start_y = row * IMG_HEIGHT
            start_x = col * IMG_WIDTH
            print(start_x, start_y)
            tile = img[start_y:start_y + IMG_HEIGHT, start_x:start_x + IMG_WIDTH]
            print(tile.shape)
            self.display_image(tile)
        else:
            wx.MessageBox('Image number out of range.', 'Error', wx.OK | wx.ICON_ERROR)
    
    def find_file(self, num):
        for filename in os.listdir(IMG_FOLDER):
            print(filename)
            if filename.endswith('.jpg'):
                start, end = map(int, filename.split('.')[0].split('_')[1].split('-'))
                print(start,end)
                if start <= num <= end:
                    print("found!: ", filename)
                    return filename
        return None

    def display_image(self, img):
        h, w, _ = img.shape
        img_flat = img.flatten()
        img_wx = wx.Image(w, h, img_flat)
        img_wx = img_wx.ConvertToBitmap()
        self.image_ctrl.SetBitmap(img_wx)
        self.panel.Layout()

if __name__ == "__main__":
    app = wx.App()
    frame = MyFrame(None, -1, 'Image Viewer')
    frame.Show()
    app.MainLoop()
