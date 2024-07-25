import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob


def find_rebar_locations(main_image, template_images):
    detected_locations = {}
    for name, template in template_images.items():
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(main_image, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.8
        loc = np.where(res >= threshold)
        rectangles = []
        for pt in zip(*loc[::-1]):
            rect = {
                "top": pt[1] / main_image.shape[0],
                "left": pt[0] / main_image.shape[1],
                "bottom": (pt[1] + h) / main_image.shape[0],
                "right": (pt[0] + w) / main_image.shape[1]
            }
            rectangles.append(rect)
        detected_locations[name] = rectangles
    return detected_locations

# Load the image of Rs3高架橋-1.bmp
files = glob.glob("../test_data/*")
rs3_image_path = files[0]
rs3_image = cv2.imread(rs3_image_path, cv2.IMREAD_GRAYSCALE)

# Load the extracted images from 鉄筋加工図
extracted_images = {}
template_paths = glob.glob("../train_data/*")
for path in template_paths:
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    extracted_images[path.split('/')[-1]] = img

# Perform the rebar location detection
rebar_locations = find_rebar_locations(rs3_image, extracted_images)

# Print the results
print(rebar_locations)

# Optionally, visualize the detected locations
for name, locations in rebar_locations.items():
    for loc in locations:
        cv2.rectangle(rs3_image, (int(loc['left'] * rs3_image.shape[1]), int(loc['top'] * rs3_image.shape[0])),
                      (int(loc['right'] * rs3_image.shape[1]), int(loc['bottom'] * rs3_image.shape[0])), (255, 0, 0), 2)

plt.imshow(rs3_image, cmap='gray')
plt.title('Detected Rebars')
plt.show()
