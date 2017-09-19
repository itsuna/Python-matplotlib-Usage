# Written by itsuna on September 18, 2017

# モジュールをインポートする
# データ解析をサポートする"pandas"というモジュールを"pd"という名前でインポート
import pandas as pd
# グラフ作成に必要な"matplotlib"の中の"pyplot"を"plt"という名前でインポート
import matplotlib.pyplot as plt

# グラフにしたいデータの入っているExcelファイルの場所と名前を入れる
excel_path = ".\\"
excel_file_name = "time-series_ex.xlsx"
# そのExcelファイルをexcel_dataという名前で読み込む
excel_data = pd.ExcelFile(excel_path + excel_file_name)

# Excelファイルの"Sheet1"の中身をdataframe型にする．
df = excel_data.parse("Sheet1")
# 項目"Sample"の中で"A"が入っている列だけ取り出し保存
df_slow = df[df["Sample"].isin(["A"])]
# 項目"Sample"の中で"B"が入っている列だけ取り出し保存
df_fast = df[df["Sample"].isin(["B"])]

# 図の枠組みを作る
fig = plt.figure()
ax = fig.add_subplot(111)
# 図の背景を白("w")にする. というか，この行を書かなければ白
fig.set_facecolor("w")
# グラフの背景を灰色("#f0f0f0")にする．もちろんカラーコードでOK
ax.set_facecolor("#f0f0f0")

# df_slowの"Time"をx軸に，"Value"をy軸にして，シアン色("c")でプロット
ax.plot(df_slow["Time"], df_slow["Value"], "c", label="A")
# df_fastの"Time"をx軸に，"Value"をy軸にして，マゼンタ色("m")でプロット
ax.plot(df_fast["Time"], df_fast["Value"], "m", label="B")

# グラフのタイトルを緑色("g")かつフォントサイズを18にして，"Time-Series"として追加
ax.set_title("Time-Series", fontsize=18, color="g")
# グラフのx軸名をオレンジ色("#ff8c00")かつフォントサイズを12にして，"Time (sec)"として追加
ax.set_xlabel("Time (sec)", fontsize=12, color="#ff8c00")
# グラフのy軸名をネイビー色("#000080")かつフォントサイズを12にして，"Intensity (a.u.)"として追加
ax.set_ylabel("Intensity (a.u.)", fontsize=12, color="#000080")

# グラフの枠を青色("b")にする
for spine in ax.spines.values():
	spine.set_color("b")
# x軸の範囲を0から10にする．この行を書かなければ自動で決まる
ax.set_xlim(0, 10)
# y軸の範囲を0から1.3にする．この行を書かなければ自動で決まる
ax.set_ylim(0, 1.3)
# x, y軸の目盛りのフォントを12に, 目盛りを赤色("r")に, 目盛りの文字色を黄色("y")にする
ax.tick_params(labelsize=12, color="r", labelcolor="y")
# legend
ax.legend(bbox_to_anchor=(1,1))

# 図の余白を減らす
fig.tight_layout()

# 図を見る
plt.show()
# 保存するなら，plt.show()を消し，下のplt.savefig()を有効にする
# plt.savefig("time-series_ex1.png")

# 図の情報をすべて捨てる
plt.close()
