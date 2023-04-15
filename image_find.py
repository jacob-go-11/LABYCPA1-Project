import cv2
import numpy as np
from tkinter import filedialog

#upload the image
def fileSelect(n):
    fileName = filedialog.askopenfilename(
        title="Open "+n+" file",
        filetypes=(("image", ".jpeg"),
                   ("image", ".png"),
                   ("image", ".jpg"),))
    return fileName

#rotate an image by a specified angle
def rotate_scale_image(image, angle, scale):
    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, scale)
    adjusted = cv2.warpAffine(image, matrix, (w, h))
    return adjusted

print("Please select your source image.")
source = cv2.imread(fileSelect("source"))

print("Please select your template image")
template = cv2.imread(fileSelect("template"))

#angles and scales
angles = np.arange(0, 361, 1)
scales = [0.5, 1.0, 1.5, 2.0]

#maximum correlation coefficient
max_corr = -1

#loop through angles and scales
for angle in angles:
    for scale in scales:
        adj_template = rotate_scale_image(template, angle, scale)

        #dimensions of the rotated/scaled template image
        height, width = adj_template.shape[:2]

        #template matching
        matching = cv2.matchTemplate(source, adj_template, cv2.TM_CCOEFF_NORMED)
        val_min, val_max, loc_min, loc_max = cv2.minMaxLoc(matching)

        #checks if rotation angle gave a better correlation coefficient
        if val_max > max_corr:
            max_corr = val_max
            fin_angle = angle
            fin_scale = scale
            start_pt = loc_max
            end_pt = (start_pt[0] + width, start_pt[1] + height)

adj_template = rotate_scale_image(template, fin_angle, fin_scale)

#draw a rectangle around the matched area
cv2.rectangle(source, start_pt, end_pt, (0, 255, 255), 2)

#display the result
cv2.imshow('the image has been found', source)
cv2.waitKey(0)
