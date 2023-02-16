import cv2 as cv
import numpy as np

def detectImg(needle_img_path, temp_img, threshold = 0.5, debug_mode = None):
     

    needle_img = cv.imread(needle_img_path, cv.IMREAD_UNCHANGED)

    needle_w = needle_img.shape[1]
    needle_h = needle_img.shape[0]

    method = cv.TM_CCOEFF_NORMED
    result = cv.matchTemplate(temp_img, needle_img, method)

    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))


    rectangles = []

    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
        rectangles.append(rect)

    rectangles, weights = cv.groupRectangles(rectangles, 1, 0.5)

    points = []
    if len(rectangles):
        print('Found needle')

        line_color = (0, 255, 0)
        line_type = cv.LINE_4
        marker_color = (255, 0, 255)
        marker_type = cv.MARKER_CROSS

        for (x, y, w, h) in rectangles:

            center_x = x + int(w/2)
            center_y = y + int(h/2)

            points.append((center_x, center_y))

            if debug_mode == 'rectangles':
 
                top_left = (x, y)
                bot_right = (x + w, y + h)

                cv.rectangle(temp_img, top_left, bot_right, line_color, line_type)
                
            elif debug_mode == 'points':
                cv.drawMarker(temp_img, (center_x, center_y), marker_color, marker_type)
        
    if debug_mode:
        cv.imshow('Matches', temp_img)
        
    return points
