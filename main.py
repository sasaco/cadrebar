import os
import glob
import matplotlib.pyplot as plt

from cadrebar import rebar_rectangle, imwrite


def main():
    # テストファイルを選ぶ
    files =  glob.glob("./test_data/*")
    rs3_image_path = files[0]
    
    # 鉄筋加工図に相当するエリアを検出する
    re_rect = rebar_rectangle()
    rebar_locations, rs3_image = re_rect.rebar_locations(rs3_image_path)

    # # 末尾に'-re'を付けたファイルに保存する
    # result_image_path = os.path.splitext(rs3_image_path)[0] + '-re' + os.path.splitext(rs3_image_path)[1]
    # imwrite(result_image_path, rs3_image)

    # matplotlibで表示する
    plt.imshow(rs3_image, cmap='gray')
    plt.title('Detected Rebars')
    plt.show()


if __name__ == "__main__":
    main()