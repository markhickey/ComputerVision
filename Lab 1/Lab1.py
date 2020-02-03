# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 01:32:57 2020

@author: ebrahim
"""

import cv2
import numpy as np

vid = cv2.VideoCapture('Movie1.MOV')    # Read Video file
success, img = vid.read()   # Read video frame, return true if successful
frame_num = 0

while success:
    success, img = vid.read()
    if frame_num % 30 == 0:     # Process every 30th video frame

        size = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 300)  # The parameters are the thresholds for Canny
        lines = cv2.HoughLines(edges, 0.5, 0.01, 200)  # The parameters are accuracies and threshold

        # Exception handling for images with no lines
        try:
            num = len(lines)
        except TypeError:
            print('No lines detected in frame number {}'.format(frame_num))
            continue

        for n in range(num):    # Convert polar lines to cartesian
            rho, theta = lines[n][0]
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a * rho
            y0 = b * rho
            x1 = int(x0 + size[1] * (-b))
            y1 = int(y0 + size[0] * (a))
            x2 = int(x0 - size[1] * (-b))
            y2 = int(y0 - size[0] * (a))

            if 1.2 <= theta <= 1.9:     # Separate horizontal and vertical lines
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            else:
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        cv2.imshow('Image', img)
        cv2.waitKey(0)
    frame_num += 1


