import cv2,sys

# image を読み込む
img = cv2.imread(sys.argv[1])

# dimensionを表示する
print(img.shape)