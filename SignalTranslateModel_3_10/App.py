import math
import numpy as np
import logging

# flask: 3.0.3
from flask import Flask, request, jsonify, render_template
import base64
# opencv-contrib-python: 4.9.0.80
# opencv-python: 4.9.0.80
import cv2
# cvzone: 1.6.1
# mediapipe: 0.10.14
from cvzone.HandTrackingModule import HandDetector
from cvzone.ClassificationModule import Classifier

classifier = Classifier("Models/letters_100/keras_model.h5", "Models/letters_100/labels.txt")

PI = math.pi

angle45 = PI / 4

def position(angle, isRigth):
    # 45 a 135
    if angle45 < angle < 3 * angle45:
        return "V"
    # -135 a -45
    if -3 * angle45 < angle < -angle45:
        return "-V"

    if (isRigth):
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


print("http://127.0.0.1:5000")

app = Flask(__name__, template_folder='Server/')

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

detector = HandDetector(maxHands=2)
offset = 20
imgSize = 300

inputWord = []
strWord = ""

inputLetters = []
strLetters = ""

@app.route('/')
def index():
    return render_template('camara.html')


@app.route('/process_frame', methods=['POST'])
def process_frame():
    imgWhite = np.ones((imgSize, imgSize, 3), np.uint8)
    try:
        data = request.json['image']
        # Decode the image
        image_data = base64.b64decode(data.split(',')[1])
        np_arr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        imgOutPut = img.copy()
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
        _, buffer = cv2.imencode('.jpg', imgOutPut)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        img_base64 = 'data:image/jpeg;base64,' + img_base64

        return jsonify({'image': img_base64})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': 'Ocurrió un error al procesar la imagen'})


if __name__ == '__main__':
    app.run(debug=True)
