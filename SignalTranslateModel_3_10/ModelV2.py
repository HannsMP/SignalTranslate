import math
import time
import numpy as np

# opencv-contrib-python: 4.9.0.80
# opencv-python: 4.9.0.80
import cv2
# cvzone: 1.6.1
# tensorflow: 2.16.1
# mediapipe: 0.10.14
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier

# obtenemos la camara
cap = cv2.VideoCapture(0)
# obtenemos el detector de manos
detector = HandDetector(maxHands=1)

classifier = Classifier("Models/letters_100/keras_model.h5", "Models/letters_100/labels.txt")

#from Models.letters_100.labels import labels

# desface del hitbox de la mano
offset = 20
# tamaño por defecto de la mano procesada a renderizar
imgSize = 300
# creamos un plano tridimencional de (ancho, alto, color(R,G,B))
imgWhite = np.ones((imgSize, imgSize, 3), np.uint8)

inputWord = []
strWord = ""

inputLetters = []
strLetters = ""

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


# siempre vigilante a la camara
while True:

    # estado de la lectura
    # img: fotograma de la camara
    success, img = cap.read()

    if not success:
        continue

    imgOutPut = img.copy()

    # hands: data vectorial de la mano
    # img: reemplaza al fotograma, por uno con articulacion y una hitbox
    hands, img = detector.findHands(img)

    # verifica si existe la data
    if hands:
        # extraccion de la data
        hand = hands[0]
        # los vectores
        x, y, w, h = hand['bbox']

        try:
            # =====================================================
            # ============ Fotograma solo de la hitbox ============
            # =====================================================

            # aplicamos un desface al ditbox
            imgCrop = img[y - offset: y + h + offset, x - offset: x + w + offset]
            # se abre una ventana donde muestra el fotograma con desface
            # // cv2.imshow("DetectorCrop", imgCrop)

            # =====================================================
            # ======= Fotograma de la hitbox Redimencianada =======
            # =====================================================

            # en el plano tridimencional se reestablece el color(R,G,B) en 255: blanco
            imgWhite[:] = 255
            # hallamos la relacion de expacion
            aspecRadio = h / w

            # si la expacion es Vertical
            if aspecRadio > 1:

                # factor de escala para ajustar la altura
                k = imgSize / h
                # nuevo ancho del fotograma
                wCal = math.ceil(k * w)
                # redimencion del fotograma relativo al ancho
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                # desface para la simetria horizontal
                wGap = math.ceil((imgSize - wCal) / 2)
                # establece el fotograma de la mano redimencionada en el plano tridimencional
                imgWhite[:, wGap: wGap + wCal] = imgResize

            # sino la expacion es Horizontal
            else:

                # factor de escala para ajustar el ancho
                k = imgSize / w
                # nuevo ancho del fotograma
                hCal = math.ceil(k * h)
                # redimencion del fotograma relativo a la altura
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                # desface para la simetria vertical
                hGap = math.ceil((imgSize - hCal) / 2)
                # establece el fotograma de la mano redimencionada en el plano tridimencional
                imgWhite[hGap:hCal + hGap, :] = imgResize

            # =====================================================
            # ======= Prediccion Letra - Seña=======
            # =====================================================

            prediction, index = classifier.getPrediction(imgWhite, draw=False)

            from Models.letters_100.labels import labels

            label = labels[index]

            # coordenadas para el calculo de la posicion de la mano
            list = hand["lmList"]
            ix, iy, iz = list[5]
            mx, my, mz = list[17]

            dx, dy = mx - ix, my - iy

            angle = math.atan2(dy, dx)

            pos = position(angle, hand["type"] == "Right")

            word = label[pos]

            print(pos, word)

            if word != input:
                inputLetters.append(word)
                strLetters = word

            cv2.putText(
                imgOutPut,
                word,
                (x, y - 20),
                cv2.FONT_HERSHEY_COMPLEX,
                2,
                (255, 0, 255),
                2
            )

            cv2.rectangle(
                imgOutPut,
                (x - offset, y - offset),
                (x + w + offset, y + h + offset),
                (255, 0, 255),
                4
            )

        except Exception:
            pass

        # // cv2.imshow("DetectorWhite", imgWhite)

    cv2.imshow("Camara", imgOutPut)

    key = cv2.waitKey(5)

    if key == ord("s"):
        cv2.imwrite(f'screen/Imagen_{time.time()}.jpg', imgOutPut)
