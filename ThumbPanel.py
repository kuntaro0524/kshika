import cv2
import wx
class ThumbPanel(wx.Panel):
    def __init__(self, parent, id, img_path):
        wx.Panel.__init__(self, parent, id)

        # 画像表示処理

        # ここに画像を表示する処理を書く

        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        height, width = img.shape[:2]
        img = wx.Bitmap.FromBuffer(width, height, img)

        self.img_ctrl = wx.StaticBitmap(self, wx.ID_ANY, wx.Bitmap(img))
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.img_ctrl, 0, wx.ALL, 5)
        self.SetSizer(sizer)
