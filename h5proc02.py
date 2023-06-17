# encoding: utf-8
import h5py
import sys
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

filename = sys.argv[1]

# HDF5ファイルを開きます
with h5py.File(filename, 'r') as f:
    # データセットを取得します
    data = f['entry/data']
    print("##########################")
    print(type(data))

    # 画像データをnumpy配列に変換します
    image = np.array(data)

# 平均値と標準偏差を計算します
mean = np.mean(image)
std_dev = np.std(image)

print('平均: ', mean)
print('標準偏差: ', std_dev)

# 画像のヒストグラムを作成します
plt.hist(image.flatten(), bins=256, color='c')
plt.title('Image Histogram')
plt.show()

# scipyやsklearnを使って更に高度なパターン解析を行います
# ここでは例として、画像のモード(最頻値)を計算します
mode = stats.mode(image, axis=None)
print('モード: ', mode.mode[0])
