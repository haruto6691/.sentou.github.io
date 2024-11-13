import cv2
import numpy as np

# 画像の読み込み
img = cv2.imread('img.png')

# 指定色 (白色)
target_color = (255, 255, 255)

# 変更後の色 
change_color = (110, 150, 100)

# 透過にしたい色 
transparent_color = (0, 0, 255)

# 画像がBGRA形式か確認し、違う場合は変換
if img.shape[2] == 3:  # 画像がBGR (3チャンネル) なら
    img = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)  # BGRA (4チャンネル) に変換

# 指定色 (target_color) を変更後の色に変更
img[np.all(img[:, :, :3] == target_color, axis=-1)] = [change_color[0], change_color[1], change_color[2], 255]

# 透過したい色 (transparent_color) をアルファチャンネルを0に設定
img[np.all(img[:, :, :3] == transparent_color, axis=-1)] = [transparent_color[0], transparent_color[1], transparent_color[2], 0]

# ファイル名を変更後の色のRGB値で作成
filename = f"{change_color[0]:03}_{change_color[1]:03}_{change_color[2]:03}.png"

# 変更後の画像を新しいファイル名で保存
cv2.imwrite(filename, img)
