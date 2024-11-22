import time
import math
import os

# cvzone: 1.6.1
# mediapipe: 0.10.14
from cvzone.HandTrackingModule import HandDetector
# opencv-contrib-python: 4.9.0.80
# opencv-python: 4.9.0.80
import cv2
# numpy: 1.26.24
import numpy as np

# https://teachablemachine.withgoogle.com/train

# obtenemos la camara
cap = cv2.VideoCapture(0)
# obtenemos el detector de manos
detector = HandDetector(maxHands=2)

# desface del hitbox de la mano
offset = 20
# tamaño por defecto de la mano procesada a renderizar
imgSize = 300
# creamos un plano tridimencional de (ancho, alto, color(R,G,B))
imgWhite = np.ones((imgSize, imgSize, 3), np.uint8)
# carpeta
folder = "DataSets/Letters/test/A"
os.makedirs(folder, exist_ok=True)
# Contador
counter = 0

# siempre vigilante a la camara
while True:

    # estado de la lectura
    # img: fotograma de la camara
    success, img = cap.read()

    if not success:
        continue

    # hands: data vectorial de la mano
    # img: reemplaza al fotograma, por uno con articulacion y una hitbox
    hands, img = detector.findHands(img)

    # verfica si existe la data
    if hands:

        if len(hands) == 1:
            # extraccion de los vectores
            x, y, w, h = hands[0]['bbox']


        else:
            # extraccion de los vectores
            x1, y1, w1, h1 = hands[0]['bbox']
            x2, y2, w2, h2 = hands[1]['bbox']

            # hitbox global
            x, y = min(x1, x2), min(y1, y2)
            w = max(x1 + w1, x2 + w2) - x
            h = max(y1 + h1, y2 + h2) - y

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

            cv2.imshow("DetectorWhite", imgWhite)

        except:
            print("fuera de rango")

    cv2.imshow("Camara", img)
    key = cv2.waitKey(1)

    if key == ord("s"):
        counter += 1
        print(f'foto numero {counter}')
        cv2.imwrite(f'{folder}/Imagen_{time.time()}.jpg', imgWhite)

    if counter > 200:
        break
