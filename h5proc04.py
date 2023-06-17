# encoding: utf-8
import numpy as np
import h5py

# copy from keitaroyam's gist

def data_as_int32_masked(data, apply_pixel_mask, h5handle):
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
                data = data_as_int32_masked(data, apply_pixel_mask, h5)
            yield data
# extract_data()

def extract_data(h5master, frameno, apply_pixel_mask=True, return_raw=False):
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

    return data_as_int32_masked(data, apply_pixel_mask, h5)
# extract_data()

def init(h5master):
    h5 = h5py.File(h5master, "r")
    for k in sorted(h5["/entry/data"].keys()):
        print(k)
        if not h5["/entry/data"].get(k): continue
        image_nr_low = h5["/entry/data"][k].attrs["image_nr_low"]
        image_nr_high = h5["/entry/data"][k].attrs["image_nr_high"]
        print(image_nr_high, image_nr_low)

import sys
info(sys.argv[1])
data = extract_data(sys.argv[1],1)
# print(data)
