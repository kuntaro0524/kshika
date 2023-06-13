import pandas as pd
import sys

# ファイルを読み込む
data = pd.read_csv(sys.argv[1], delim_whitespace=True)

# "kind"が "n_spots"の行だけを選択する
n_spots_data = data[data["kind"] == "n_spots"].copy()

# 座標をソート
n_spots_data.sort_values(by=['y', 'x'], inplace=True)

# ソートした座標に対して新たなインデックスをつける
n_spots_data['fast_index'] = n_spots_data.groupby('y').cumcount()
n_spots_data['slow_index'] = n_spots_data.groupby('x').cumcount()

# CSVに出力
n_spots_data.to_csv("n_spots_data.csv", index=False)
