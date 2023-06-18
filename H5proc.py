# encoding: utf-8
import numpy as np
import h5py

# copy from keitaroyam's gist

class H5proc:
    def __init__(self, master_file):
        self.h5 = h5py.File(master_file, "r")
        self.data = None

    def data_as_int32_masked(self, data, apply_pixel_mask, h5handle):
        bad_sel = data == 2**(data.dtype.itemsize*8)-1
        data = data.astype(np.int32)
        data[bad_sel] = -3 # To see pixels not masked by pixel mask.
        if apply_pixel_mask and "/entry/instrument/detector/detectorSpecific/pixel_mask" in h5handle:
            mask = h5handle["/entry/instrument/detector/detectorSpecific/pixel_mask"][:]
            data[mask==1] = -1
            data[mask>1] = -2

        return data
    # data_as_int32()

    def data_iter(h5master, apply_pixel_mask=True, return_raw=False):
        h5 = h5py.File(h5master, "r")
        data = None

        for k in sorted(h5["/entry/data"].keys()):
            if not h5["/entry/data"].get(k): continue
            for data in h5["/entry/data"][k]:
                if not return_raw:
                    data = self.data_as_int32_masked(data, apply_pixel_mask, h5)
                yield data
    # extract_data()

    def extract_data(self, h5master, frameno, apply_pixel_mask=True, return_raw=False):
        h5 = h5py.File(h5master, "r")
        data = None

        if 0:
            i_seen = 0
            for k in sorted(h5["/entry/data"].keys()):
                print(k)
                try:
                    for i in range(h5["/entry/data"][k].shape[0]):
                        i_seen += 1
                        if i_seen == frameno:
                            data = h5["/entry/data"][k][i,]
                except KeyError:
                    break
        else:
            for k in sorted(h5["/entry/data"].keys()):
                if not h5["/entry/data"].get(k): continue
                image_nr_low = h5["/entry/data"][k].attrs["image_nr_low"]
                image_nr_high = h5["/entry/data"][k].attrs["image_nr_high"]
                if image_nr_low <= frameno <= image_nr_high:
                    idx = int(frameno - image_nr_low)
                    print("KKKK",k,idx)
                    data = h5["/entry/data"][k][idx,]
                    break

        if data is None:
            print("Data not found")
            return data

        if return_raw:
            return data

        return self.data_as_int32_masked(data, apply_pixel_mask, h5)
    # extract_data()

    def init(self):
        for k in sorted(self.h5["/entry/data"].keys()):
            if not self.h5["/entry/data"].get(k): continue
            image_nr_low = self.h5["/entry/data"][k].attrs["image_nr_low"]
            image_nr_high = self.h5["/entry/data"][k].attrs["image_nr_high"]
            print("TTESTTST:",image_nr_high, image_nr_low)

    def peakSearch(self, data):
        from scipy import ndimage

        # ピクセルの平均値を計算
        mean_value = np.mean(data)
        
        # 平均値の3倍以上のピクセルを有効ピクセルとする
        mask = data > 3 * mean_value
        
        # 連続する有効ピクセルを一つのピークとしてラベル付け
        #-q: 以下は何をしていますか？
        #-a: 連続する有効ピクセルを一つのピークとしてラベル付けしている
        #-q: label付とは具体的に何をしていますか？
        #-a: 連続する有効ピクセルを一つのピークとしてラベル付けしている

        labeled, num_peaks = ndimage.label(mask)

        # labelしたピークがわかるように画像を保存
        import matplotlib.pyplot as plt
        plt.imshow(labeled)
        plt.show()
        
        # ピークの大きさが50を超える場合、そのピークを無効にする
        sizes = ndimage.sum(mask, labeled, range(1, num_peaks+1))
        mask_size = sizes < 50
        peak_mask = mask_size[labeled]
        
        # 最終的なピークの数を計算
        final_num_peaks = len(np.unique(labeled[peak_mask])) - 1
        
        print('Number of peaks:', final_num_peaks)

import sys

h5m = H5proc(sys.argv[1])
h5m.init()
data = h5m.extract_data(sys.argv[1],1)

# data はdata[i][j]で数値を有する
# ピクセルの平均値を取得し、その３倍以上の値を持つピクセルを抜き出す
# その座標を表示する
mean = np.mean(data)
print("mean: ", mean)

# thresholdはmeanの３倍
threshold = mean * 5
print("threshold: ", threshold)

# dataのなかで数値がthresholdより大きいものを抜き出す
# それ以外のピクセルは０にする
data[data < threshold] = 0

# threshold以上のピクセル数を数える
# これが結果となる
print("result: ", np.count_nonzero(data))

# peak search
h5m.peakSearch(data)

# data はdata[i][j]で数値を有する
# これを画像として表示する
import matplotlib.pyplot as plt
# heatmap
plt.imshow(data)
plt.colorbar()
plt.show()