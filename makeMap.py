# encoding: utf-8
import cv2
import numpy as np
import pandas as pd
import sys

# 画像を読み込む
image_path = sys.argv[1]
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# 画像のサイズを取得
height, width = img.shape

# 各ピクセルの座標と明るさを格納するための空のリストを作成
data = []

# 各ピクセルをループ処理
for y in range(height):
    for x in range(width):
        # 明るさ（0-255）を取得
        brightness = img[y, x]

        # brightnessが負の場合には0にする
        if brightness < 0:
            print("negative")
            brightness = 0
        # 座標と明るさをリストに追加
        data.append([x, y, brightness])

# データをデータフレームに変換
df = pd.DataFrame(data, columns=['x', 'y', 'height'])

# df 'height' が　負の値の行を0にする
df.loc[df['height'] < 0, 'height'] = 0

# CSVファイルに出力
df.to_csv('output.csv', index=False)
