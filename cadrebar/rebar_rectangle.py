import os
import numpy as np
import cv2
import glob

def imwrite(filename, img, params=None):
    try:
        ext = os.path.splitext(filename)[1]
        result, n = cv2.imencode(ext, img, params)

        if result:
            with open(filename, mode='w+b') as f:
                n.tofile(f)
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    
def imread(filename, flags=cv2.IMREAD_GRAYSCALE, dtype=np.uint8):
    try:
        n = np.fromfile(filename, dtype)
        img = cv2.imdecode(n, flags)
        return img
    except Exception as e:
        print(e)
        return None


def find_locations(main_image, template_images):
    detected_locations = {}
    main_image_gray = cv2.cvtColor(main_image, cv2.COLOR_BGR2GRAY) if len(main_image.shape) == 3 else main_image
    for name, template in template_images.items():
        w, h = template.shape[::-1]
        res = cv2.matchTemplate(main_image_gray, template, cv2.TM_CCOEFF_NORMED)
        threshold = 0.4 # 類似度のしきい値
        loc = np.where(res >= threshold)
        rectangles = []
        for pt in zip(*loc[::-1]):
            rect = {
                "top": pt[1],
                "left": pt[0],
                "bottom": (pt[1] + h),
                "right": (pt[0] + w)
            }
            rectangles.append(rect)
        detected_locations[name] = rectangles
    return detected_locations



class rebar_rectangle:
    
    def __init__(self):
        # Load the extracted images from 鉄筋加工図
        self.extracted_images = {}
        template_paths = glob.glob("./train_data/*")
        for path in template_paths:
            img = imread(path, cv2.IMREAD_GRAYSCALE)
            # imgがNoneでないことを確認
            if img is not None:
                self.extracted_images[path.split('/')[-1]] = img
                

    def rebar_locations(self, rs3_image_path):  

        # Load the image of Rs3高架橋-1.bmp
        rs3_image = imread(rs3_image_path, cv2.IMREAD_COLOR)

        # Perform the rebar location detection
        rebar_locations = find_locations(rs3_image, self.extracted_images)

        # Print the results
        print(rebar_locations)

        # Optionally, visualize the detected locations
        for name, locations in rebar_locations.items():
            for loc in locations:
                cv2.rectangle(
                    rs3_image, 
                    (int(loc['left']), int(loc['top'])),
                    (int(loc['right']), int(loc['bottom'])), 
                    (255, 0, 0), 
                    2
                )

        return rebar_locations, rs3_image
    



