import cv2
import numpy as np

def get_img_size(img):
	height = img.shape[0]
	width = img.shape[1]
	img_size = (int(width), int(height))
	return img_size

# 画像の傾きの差を補正する（画像の特徴量を検出・マッチングして透視変換する）
def transform_perspective(transformed_file, relative_file):
    # 特徴量検出器を作成する
    akaze = cv2.AKAZE_create()
    # 二つの画像の特徴点を抽出する
    kpA, desA = akaze.detectAndCompute(relative_file, None)
    kpB, desB = akaze.detectAndCompute(transformed_file, None)

    ## 特徴量をマッチングする
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(desA,desB)
    matches = sorted(matches, key = lambda x:x.distance)
    good = matches[:int(len(matches) * 0.2)]
    src_pts = np.float32([kpA[m.queryIdx].pt for m in good]).reshape(-1,1,2)
    dst_pts = np.float32([kpB[m.trainIdx].pt for m in good]).reshape(-1,1,2)
    M, mask = cv2.findHomography(dst_pts, src_pts, cv2.RANSAC,5.0)
    # 透視変換する
    transformed_file = cv2.warpPerspective(transformed_file, M, get_img_size(relative_file))
    return transformed_file



# クリックされた座標を保持するリスト
click_positions = []

# マウスクリックイベントのコールバック関数
def click_event(event, x, y, flags, param):
    global img
    if event == cv2.EVENT_LBUTTONDOWN:
        # クリックされた位置をリストに追加する
        click_positions.append((x, y))
        if len(click_positions) == 1:
            print(f"left top corner: ({x}, {y})")
        if len(click_positions) == 2:
            print(f"right bottom corner: ({x}, {y})")

# 画像を比較しない領域を取得する
def get_region_of_uninterest(img_to_click):
    # ウィンドウを表示する
    cv2.imshow('click the point of uncompared areas', img_to_click)

    # マウスイベントを設定する
    cv2.setMouseCallback('click the point of uncompared areas', click_event)

    # クリックが2回になるまで繰り返す
    while len(click_positions) < 2:
        cv2.waitKey(1)  # 1ミリ秒待機して再描画する

    # クリックが2回になったらウィンドウを閉じる
    cv2.destroyAllWindows()
    return click_positions[0], click_positions[1]



### 画像の特定の色を別の色に変更する
# dest_color 指定色
# src_color 変更後の色
def convert_coloer(img, dest_color, src_color):
	# 画像の縦横
	h, w = img.shape[:2]

	# 色を変える
	for i in range(h):
		for j in range(w):
			b, g, r = img[i, j]
			if (b, g, r) == dest_color:
				img[i, j] = src_color
			else:
				img[i, j] = (255, 255, 255)
