#encoding: utf-8
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

class SummaryDat():
    def __init__(self, file_path):
        self.file_path = file_path
        self.isInit=False

    def init(self):
        print("TTTTT")
        # データを読み込む
        self.df = pd.read_csv(self.file_path, delim_whitespace=True)
        # kindが "n_spots" の行だけを選択する
        self.df_spots = self.df[self.df['kind'] == 'n_spots']

        # x, y, dataの列を取り出して新しいデータフレームを作成する
        self.heatmap_data = self.df_spots[['x', 'y', 'data']]

        # データフレームをピボットしてヒートマップを作成する
        self.heatmap_data_pivot = self.heatmap_data.pivot(index='y', columns='x', values='data')
        self.isInit=True
        print("INIT")

    def drawHeatmap(self):
        if self.isInit==False:
            self.init() 
        # ヒートマップを表示する
        plt.figure(figsize=(8, 6))
        sns.heatmap(self.heatmap_data_pivot, cmap='viridis')
        plt.show()

    def writeCSV(self, outfile):
        # CSV ファイルとして書き出す
        # ラベルは x, y, data -> x, y, height として出力
        # データは heatmap_data
        self.heatmap_data.to_csv(outfile, index=False, header=['x', 'y', 'height'])

# mainが定義されていなかったら
if __name__ == '__main__':
    cc = SummaryDat('summary.dat')
    cc.drawHeatmap()