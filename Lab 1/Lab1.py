# -*- coding: utf-8 -*-
"""
Created on Mon Feb  3 01:32:57 2020
@author: ebrahim
"""

import cv2
import numpy as np

# Returns the intersection point of two lines
def get_intersections(line_a, line_b):

    rho1, theta1 = line_a[0]
    rho2, theta2 = line_b[0]
    A = np.array([
        [np.cos(theta1), np.sin(theta1)],
        [np.cos(theta2), np.sin(theta2)]
    ])
    b = np.array([[rho1], [rho2]])
    x0, y0 = np.linalg.solve(A, b)
    x0, y0 = int(np.round(x0)), int(np.round(y0))

    return [ x0, y0 ]

vid = cv2.VideoCapture('Movie1.MOV')    # Read Video file
success, img = vid.read()   # Read video frame, return true if successful
frame_num = 0

while success:
    success, img = vid.read()
    if frame_num % 30 == 0:     # Process every 30th video frame
        vert_lines = []
        hor_lines = []

        size = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 300)  # The parameters are the thresholds for Canny
        lines = cv2.HoughLines(edges, 0.5, 0.01, 200)  # The parameters are accuracies and threshold

        # Exception handling for images with no lines
        try:
            num = len(lines)
        except TypeError:
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
                vert_lines.append(lines[n])

            else:
                cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                hor_lines.append(lines[n])

            # Loop over all of the lines, marking intersection points
            for i in range(len(vert_lines)):
                for j in range(len(hor_lines)):
                    line1 = vert_lines[i]
                    line2 = hor_lines[j]
                    x, y = get_intersections(line1, line2) # Returns the point of intersection
                    cv2.circle(img, (x, y), 8, (0, 0, 0), thickness=-1)

        cv2.imshow('Image', img)
        cv2.waitKey(0)
    frame_num += 1
