#encoding: utf-8
import h5py

def explore_datasets(h5_file):
    with h5py.File(h5_file, 'r') as f:
        def explore(name, node):
            if isinstance(node, h5py.Dataset):  # ノードがデータセットの場合
                print('path:', name)
                print('shape:', node.shape)
                print('type:', node.dtype)
                print('-----')
        f.visititems(explore)

import sys
explore_datasets(sys.argv[1])