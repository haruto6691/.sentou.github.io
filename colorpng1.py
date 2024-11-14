import cv2
import numpy as np

# 画像の読み込み
img = cv2.imread('img.png')

# 画像が正常に読み込まれたか確認
if img is None:
    print("画像の読み込みに失敗しました。ファイルパスとファイル名を確認してください。")
    exit()  # プログラムを終了

# 指定色 (黄色)
target_color = (255, 255, 255)

# 変更後の色 (例: 黒色)
change_color = (101, 150, 100)

# 透過にしたい色 (赤色)
transparent_color = (100, 0, 0)

# 画像がBGR形式(3チャンネル)の場合はBGRA形式(4チャンネル)に変換
if img.shape[2] == 3:  # 画像がBGR (3チャンネル) なら
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)  # BGRA (4チャンネル) に変換

# 指定色 (target_color) を変更後の色に変更
# (target_color) の色を変更後の色に置換
for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        if np.array_equal(img[y, x, :3], target_color):  # BGR部分を比較
            img[y, x, :3] = change_color  # 色変更
            img[y, x, 3] = 255  # アルファチャンネルを完全不透明に設定

# 透過にしたい色 (transparent_color) をアルファチャンネルを0に設定
for y in range(img.shape[0]):
    for x in range(img.shape[1]):
        if np.array_equal(img[y, x, :3], transparent_color):  # BGR部分を比較
            img[y, x, 3] = 0  # アルファチャンネルを透明に設定

# ファイル名を変更後の色のRGB値で作成
filename = f"{change_color[0]:03}_{change_color[1]:03}_{change_color[2]:03}.png"

# 変更後の画像を新しいファイル名で保存
cv2.imwrite(filename, img)

print("画像の保存が完了しました。")

