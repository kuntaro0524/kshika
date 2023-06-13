#encoding: utf-8
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# データを読み込む
df = pd.read_csv('summary.dat', delim_whitespace=True)

# kindが "n_spots" の行だけを選択する
df_spots = df[df['kind'] == 'n_spots']

# x, y, dataの列を取り出して新しいデータフレームを作成する
heatmap_data = df_spots[['x', 'y', 'data']]

# データフレームをピボットしてヒートマップを作成する
heatmap_data_pivot = heatmap_data.pivot(index='y', columns='x', values='data')

# ヒートマップを表示する
plt.figure(figsize=(8, 6))
sns.heatmap(heatmap_data_pivot, cmap='viridis')
plt.show()

# CSV ファイルとして書き出す
# ラベルは x, y, data -> x, y, height として出力
# データは heatmap_data
heatmap_data.to_csv('heatmap.csv', index=False, header=['x', 'y', 'height'])