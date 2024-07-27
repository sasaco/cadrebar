import os
import glob
import matplotlib.pyplot as plt

from cadrebar import rebar_rectangle, imwrite


def main():
    files =  glob.glob("./test_data/*")
    rs3_image_path = files[0]
    re_rect = rebar_rectangle()
    rebar_locations, rs3_image = re_rect.rebar_locations(rs3_image_path)

    result_image_path = os.path.splitext(rs3_image_path)[0] + '_re' + os.path.splitext(rs3_image_path)[1]
    imwrite(result_image_path, rs3_image)

    plt.imshow(rs3_image, cmap='gray')
    plt.title('Detected Rebars')
    plt.show()


if __name__ == "__main__":
    main()