import math

# cvzone: 1.6.1
# mediapipe: 0.10.14
from cvzone.FaceMeshModule import FaceMeshDetector
# opencv-contrib-python: 4.9.0.80
# opencv-python: 4.9.0.80
import cv2
# numpy: 1.26.24
import numpy as np

cap = cv2.VideoCapture(0)

detector = FaceMeshDetector()

offset = 20

imgSize = 500

imgWhite = np.ones((imgSize, imgSize, 3), np.uint8)

while True:
    success, img = cap.read()

    if not success:
        continue

    img, faces = detector.findFaceMesh(img, draw=False)

    if len(faces):
        face = faces[0]
        bbox = [float("inf"), float("inf"), float("-inf"), float("-inf")]

        for x, y in face:
            bbox[0] = min(bbox[0], x)
            bbox[1] = min(bbox[1], y)
            bbox[2] = max(bbox[2], x)
            bbox[3] = max(bbox[3], y)

            cv2.circle(img, (x, y), 0, (0, 0, 0), -1)

        w = bbox[2] - bbox[0]

        h = bbox[3] - bbox[1]
        x = bbox[0]
        y = bbox[1]

        try:
            imgCrop = img[y - offset: y + h + offset, x - offset: x + w + offset]

            imgWhite[:] = 255

            aspecRadio = h / w

            if aspecRadio > 1:
                k = imgSize / h

                wCal = math.ceil(k * w)

                imgResize = cv2.resize(imgCrop, (wCal, imgSize))

                wGap = math.ceil((imgSize - wCal) / 2)

                imgWhite[:, wGap: wGap + wCal] = imgResize

            else:

                k = imgSize / w

                hCal = math.ceil(k * h)

                imgResize = cv2.resize(imgCrop, (imgSize, hCal))

                hGap = math.ceil((imgSize - hCal) / 2)

                imgWhite[hGap:hCal + hGap, :] = imgResize

            cv2.imshow("DetectorWhite", imgWhite)

        except:
            print("fuera de rango")

    cv2.imshow("Camara", img)

    cv2.waitKey(1)
