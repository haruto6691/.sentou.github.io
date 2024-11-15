import cv2
import numpy as np

# 画像の読み込み
img = cv2.imread('img.png')

# 指定色 (黄色)
target_color = (255, 255, 255)

# 変更後の色 (例: 黒色)
change_color = (101, 150, 100)

# 色の変更
# 各ピクセルが指定された色と一致する場合、その色を変更
img = np.where(np.all(img == target_color, axis=-1, keepdims=True), change_color, img)

# ファイル名を変更後の色のRGB値で作成
filename = f"{change_color[0]:03}_{change_color[1]:03}_{change_color[2]:03}.png"

# 変更後の画像を新しいファイル名で保存
cv2.imwrite(filename, img)

