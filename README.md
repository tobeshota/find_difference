# 概要
間違い探しを解くプログラムです．  
プログラムは2つの画像を比較し，その差異を検知（異常検知）します．
![example](https://github.com/user-attachments/assets/1865557b-f201-47c7-a233-87c9a2bb4a59)

# 応用事例
異常検知機能は立入禁止エリアへの侵入検知機能と捉えることができます．  
この場合，異常検知機能は次の事例への応用が期待できます．
- 駅構内の安全性向上施策への応用（線路内や踏切内への人立入の検知）
- デジタルゲームのテストプレイの自動化への応用（デジタル空間におけるプレイヤーの侵入不可地点の侵入検知）
- 自動車の安全性向上施策への応用（自動車の接近の検知）

# 使い方
### 必要条件
```shell
pip install opencv-python
pip install numpy
```

### 実行
```shell
git clone https://github.com/tobeshota/find_difference.git
cd find_difference/src
python main.py
```
### 実行(立入可能エリアを指定する場合)
プログラムは，立入可能エリア（長方形で表される2つの画像の差異を検知しないエリア）を定めることができます．
1. コマンドライン引数に`rou`を指定する
```shell
git clone https://github.com/tobeshota/find_difference.git
cd find_difference/src
python main.py rou
```
2. 表示されたウィンドウから指定したい立入可能エリアの左隅角，右隅角をクリックする



# 使用した技術
### 使用したライブラリ
| 名称 | バージョン | 提供元 | ライセンス | 利用目的 |
| --- | --- | --- | --- | --- |
| [OpenCV](https://opencv.org/) | 4.8.0 | OpenCV.org | Apache License 2.0 | 画像処理のため |
| [NumPY](https://numpy.org/) | 1.26.1 | NumPy.org | BSD License |数値計算のため|

### 処理のフロー
1. 画像を読み込む
<details>
  <summary>2. 前処理する</summary>

    1. 画像の傾きの差を補正する
      - 画像の特徴量を抽出・マッチングし透視変換する
    2. 指定された領域（立入可能エリア）の差異の検出を防ぐ
      - 指定された領域を白マスクする
    3. 画像の色調の差を補正する
      - エッジを抽出する
</details>
<details>
  <summary>3. 画像の差異を検出する</summary>

    1. 異常検知する
      - 背景差分法により画像の差異を検知する
      - 画像の差異を閾値を設けて二値化する
</details>
<details>
  <summary>4. 後処理する</summary>

    1. 差異をクロージングする
    2. 差異を赤色にする
    3. 画像の差異を比較元画像と重ね合わせる
</details>

5. 差異を示す画像を生成する

# 参考文献
- Junichi Higuchi. "pythonで２つの画像を比較してその差異を分かりやすく示すための画像を新たに生成するプログラムを作ってみた #Python", Qiita. <https://qiita.com/jun_higuche/items/e3c3263ba50ea296f7bf>. 2024年8月26日閲覧
- grv2688. "【Python】OpenCVで間違い探しをする #Python", Qiita. <https://qiita.com/grv2688/items/44f9e0ddd429afbb26a2>. 2024年8月26日閲覧
- いらすとや. "酔っぱらいのイラスト「サラリーマン」". <https://www.irasutoya.com/2013/08/blog-post_30.html>. 2024年8月26日閲覧
- Cranberry. "駅に停車している電車（上から見た図）イラスト - No: 963022", イラストAC. <https://www.ac-illust.com/main/detail.php?id=963022>. 2024年8月26日閲覧
