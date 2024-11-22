import math
import ujson
import time
import numpy as np

# opencv-contrib-python: 4.9.0.80
# opencv-python: 4.9.0.80
import cv2
# cvzone: 1.6.1
# tensorflow: 2.15.0
# mediapipe: 0.10.14
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier

# obtenemos la camara
cap = cv2.VideoCapture(0)
# obtenemos el detector de manos
detector = HandDetector(maxHands=1)

classifier = Classifier("Models/letters_100/keras_model.h5", "Models/letters_100/labels.txt")

with open("Models/letters_100/labels.json", "r") as file:
    labels = ujson.load(file)

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

    # verfica si existe la data
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

            prediction, index = classifier.getPrediction(imgWhite, draw=False)

            word = labels[index]

            if (word != input):
                inputLetters.append(word)
                strLetters = word

            cv2.putText(
                imgOutPut,
                word,
                (x, y - 25),
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

    cv2.imshow("Camara", imgOutPut)

    key = cv2.waitKey(1)

    if key == ord("s"):
        cv2.imwrite(f'screen/Imagen_{time.time()}.jpg', imgOutPut)