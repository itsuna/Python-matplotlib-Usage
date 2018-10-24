# モジュールをインポートする
# 数値計算を効率的に行う"numpy"というモジュールを"np"という名前でインポート
import numpy as np
# データ解析をサポートする"pandas"というモジュールを"pd"という名前でインポート
import pandas as pd
# グラフ作成に必要な"matplotlib"の中の"pyplot"を"plt"という名前でインポート
import matplotlib.pyplot as plt

# グラフにしたいデータの入っているExcelファイル("angle_distribution_ex.xlsx)の場所と名前を入れる
excel_path = ".\\"
excel_file_name = "angle_distribution_ex.xlsx"
# そのExcelファイルをexcel_dataという名前で読み込む
excel_data = pd.ExcelFile(excel_path + excel_file_name)
# 一番始めのSheetの中身をdataframe型にする
df = excel_data.parse(excel_data.sheet_names[0])
# 項目"Sample"の中で"A"が入っている列だけ取り出し保存
df_A = df[df["Sample"]=="A"]
# 項目"Sample"の中で"B"が入っている列だけ取り出し保存
df_B = df[df["Sample"]=="B"]

# 角度の度数分布表を作成する関数
def create_angular_frequency_distribution_table(df, div_num, MAX_DEGREE=180):
    # １つのエリアの幅を計算する。(ex. MAX_DEGREE=180°かつdiv_num=9の場合, 1つのエリアの幅は20°)
    each_angle_size = MAX_DEGREE / div_num
    # 各エリアの角度を入れる。(+1により最後の角度も入る)
    angle_list = [i * each_angle_size for i in range(div_num + 1)]
    # 度数分布表を辞書型で初期化する
    angular_distribution = {angle: 0 for angle in angle_list[:-1]}
    # dataframeを一行ずつ読み込む
    for index, row in df.iterrows():
        # ある行の角度が度数分布表のどこに入るかを探す
        for i in range(len(angle_list)-1):
            # もしある行の角度が, angle_list[i]以上angle_list[i+1]未満ならその度数分布表を+1してループを抜ける
            if ((row["Angle"] >= angle_list[i]) and (row["Angle"] < angle_list[i+1])):
                angular_distribution[angle_list[i]] += 1
                break
    print(angular_distribution)
    return [angular_distribution, angle_list]

def plot_angular_distribution(ax, angle_dist, angle_list, r_max, r_tick_width, MAX_DEGREE=180):
    import math
    # 偏角Θの範囲を決める
    ax.set_xlim([0, np.pi*MAX_DEGREE/180])
    # 30°刻みにtickを入れる
    ax.set_xticks([i * np.pi / 6 for i in range(int(math.floor(MAX_DEGREE/30)+1))])
    # 動径rの範囲を引数r_maxから設定する
    ax.set_ylim([0, r_max])
    #　r_tick_width刻みにtickを入れる
    ax.set_yticks([r_tick_width * i for i in range(int(math.ceil(r_max/r_tick_width)))])
    
    for i in range(len(angle_list)-1):
        # 扇形の閉曲線を作る
        theta = np.array(
            [angle_list[i]*np.pi/180, angle_list[i]*np.pi/180] + 
            [theta*np.pi/180 for theta in np.linspace(angle_list[i], angle_list[i+1], num=int(angle_list[i+1]-angle_list[i]))] +
            [angle_list[i+1]*np.pi/180, angle_list[i+1]*np.pi/180]
        )
        r = np.array(
            [0, angle_dist[angle_list[i]]] + 
            [angle_dist[angle_list[i]] for theta in np.linspace(angle_list[i], angle_list[i+1], num=int(angle_list[i+1]-angle_list[i]))] + 
            [angle_dist[angle_list[i]], 0]
        )
        # 作った扇形をプロット
        ax.plot(theta, r, color="#333333", linewidth=1)
        # 扇の内側を塗りつぶす
        ax.fill(theta, r, "#aaaaaa")
    return ax

# ここからグラフを作成
# 1行2列のグラフの土台を作成
fig, axes = plt.subplots(1, 2, subplot_kw=dict(projection="polar"))
# グラフのサイズ指定
fig.set_size_inches(12, 5)

# df_Aからangular_distributionとangle_listを計算する
angle_dist_A, angle_list_A = create_angular_frequency_distribution_table(df_A, 9)
# 1行1列目のグラフにプロット
axes[0] = plot_angular_distribution(axes[0], angle_dist_A, angle_list_A, 22, 10)

# df_Bからangular_distributionとangle_listを計算する
angle_dist_B, angle_list_B = create_angular_frequency_distribution_table(df_B, 9)
# 1行2列目のグラフにプロット
axes[1] = plot_angular_distribution(axes[1], angle_dist_B, angle_list_B, 22, 10)

for ax, name in zip(axes, ["Sample A", "Sample B"]):
    # タイトルをフォントサイズ14で"Sample B"とし、位置調整
    ax.set_title(name, y=0.85, fontsize=14)
    # xlabelをフォントサイズ14で"Frequency"に
    ax.set_xlabel("Frequency", fontsize=14)
    # xlabelの位置調整
    ax.xaxis.set_label_coords(0.5, 0.15)
fig.tight_layout()

# saveするかどうかのboolean
save = False
# 保存先のpathとファイル名を指定
save_path = ".//"
save_file_name = "20181024 angle_distribution_plot_ex"
# saveするなら以下で保存 (ex. png and svg)
if save==True:
    plt.savefig(save_path + save_file_name + ".png")
    plt.savefig(save_path + save_file_name + ".svg")

# グラフを見る
plt.show()
# グラフの情報を捨てる
plt.close()
