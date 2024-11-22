import math
import cv2
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)

PI = math.pi

angle45 = PI / 4


def position(angle, isRigth):
    # 45 a 135
    if angle45 < angle < 3 * angle45:
        return "V"
    # -135 a -45
    if -3 * angle45 < angle < -angle45:
        return "-V"

    if(isRigth):
        # -45 a 45
        if -angle45 <= angle <= angle45:
            return "-H"
        # 135 a 180 o -180 a -135
        if 3 * angle45 <= angle <= PI or -PI <= angle <= -3 * angle45:
            return "H"
    else:
        # -45 a 45
        if -angle45 <= angle <= angle45:
            return "H"
        # 135 a 180 o -180 a -135
        if 3 * angle45 <= angle <= PI or -PI <= angle <= -3 * angle45:
            return "-H"

    return "I"

while True:
    success, img = cap.read()

    if not success:
        continue

    hands, img = detector.findHands(img)

    if hands:
        hand = hands[0]
        list = hand["lmList"]
        ix, iy, iz = list[5]
        mx, my, mz = list[17]

        dx, dy = mx - ix, my - iy

        angle = math.atan2(dy, dx)

        print(angle, position(angle, hand["type"] == "Right"))

        cv2.line(img, pt1=(ix, iy), pt2=(mx, my), color=(255, 255, 0), thickness=2)

    cv2.imshow("Camara", img)

    key = cv2.waitKey(1)
