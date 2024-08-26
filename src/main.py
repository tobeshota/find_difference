import cv2
from treat import pretreat, aftertreat

# パラメータ ##########
# 読み込む画像
input_path_1 = '../img/input/ok_in.png'
input_path_2 = '../img/input/ko_out.png'

# 書き込む画像
output_path = '../img/output/diff.png'
#####################



# 画像を読み込む
no_instrusion_img = cv2.imread(input_path_1)
instrusion_img = cv2.imread(input_path_2)

# 前処理する
instrusion_img, no_instrusion_img = pretreat(instrusion_img, no_instrusion_img)

# カラー画像をグレースケール画像に変換する
instrusion_img_grey = cv2.cvtColor(instrusion_img, cv2.COLOR_BGR2GRAY)
no_instrusion_img_grey = cv2.cvtColor(no_instrusion_img, cv2.COLOR_BGR2GRAY)

# 画像の色調の差を補正する（エッジ処理）
week_edge = 50
strong_edge = 300
no_instrusion_edge_img = cv2.Canny(instrusion_img_grey, week_edge, strong_edge)
instrusion_edge_img = cv2.Canny(no_instrusion_img_grey, week_edge, strong_edge)

# 画像の差異を検出する（背景差異法）
diff = cv2.absdiff(no_instrusion_edge_img, instrusion_edge_img)

# 後処理する
diff = aftertreat(diff, cv2.imread(input_path_2))

# 差異の画像を書き込む
cv2.imwrite(output_path, diff)
