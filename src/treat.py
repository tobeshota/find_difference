import cv2, sys
import numpy as np
from utils import transform_perspective, get_region_of_uninterest, convert_coloer

# 前処理する
def pretreat(imgA, imgB):
	# 画像の傾きの差を補正する（透視変換する）
	imgA = transform_perspective(imgA, imgB)

	# 画像の差異を検出しない領域(立入可能エリア)に白マスクをかける
	if len(sys.argv) > 1 and sys.argv[1] == 'rou':
		left_top_corner, right_btm_corner = get_region_of_uninterest(imgB)
		white = (255, 255, 255)
		imgB = cv2.rectangle(imgB, left_top_corner, right_btm_corner, white, cv2.FILLED)
		imgA = cv2.rectangle(imgA, left_top_corner, right_btm_corner, white, cv2.FILLED)

	# シャープネスを上げる
	blurred_imgA = cv2.GaussianBlur(imgA, (9,9), 10.0)
	blurred_imgB = cv2.GaussianBlur(imgB, (9,9), 10.0)
	imgA = cv2.addWeighted(imgA, 2.0, blurred_imgA, -1.0, 0, imgA)
	imgB = cv2.addWeighted(imgB, 2.0, blurred_imgB, -1.0, 0, imgB)

	# コントラストと明るさを調整する
	contrast = 3
	brightness = 0.7
	imgA = cv2.convertScaleAbs(imgA, alpha=contrast, beta=brightness)
	imgB = cv2.convertScaleAbs(imgB, alpha=contrast, beta=brightness)

	return imgA, imgB



### 後処理する
# diff_img 差異を示す画像
# weighted_img diff_imgに重ねる画像
def aftertreat(diff_img, weighted_img):
	# 二値化する
	_, diff_bin = cv2.threshold(diff_img, 50, 255, cv2.THRESH_BINARY) # 閾値は50

	# モフォロジー処理する
	kernel = np.ones((5,5),np.uint8)
	diff_bin = cv2.morphologyEx(diff_bin, cv2.MORPH_CLOSE, kernel)

	# 差異を白色から唐紅色にする
	diff_bin_rgb = cv2.cvtColor(diff_bin, cv2.COLOR_GRAY2RGB)
	white = (255, 255, 255)
	karakurenai = (25, 0, 244)
	convert_coloer(diff_bin_rgb, white, karakurenai)

	# 侵入がある画像と重ねる
	diff_img = cv2.addWeighted(weighted_img, 0.5, diff_bin_rgb, 0.5, 2.2) # ２.２はガンマ値。大きくすると白っぽくなる
	return diff_img
