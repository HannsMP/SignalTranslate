import numpy as np
import logging

# flask: 3.0.3
from flask import Flask, request, jsonify, render_template
import base64
# cvzone: 1.6.1
# mediapipe: 0.10.14
from cvzone.HandTrackingModule import HandDetector
# opencv-contrib-python: 4.9.0.80
# opencv-python: 4.9.0.80
import cv2

print("http://127.0.0.1:5000")

app = Flask(__name__, template_folder='Server/')

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

detector = HandDetector(maxHands=2)


@app.route('/')
def index():
    return render_template('camara.html')


@app.route('/process_frame', methods=['POST'])
def process_frame():
    try:
        data = request.json['image']
        # Decode the image
        image_data = base64.b64decode(data.split(',')[1])
        np_arr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        _, img = detector.findHands(img)

        _, buffer = cv2.imencode('.jpg', img)
        img_base64 = base64.b64encode(buffer).decode('utf-8')
        img_base64 = 'data:image/jpeg;base64,' + img_base64

        return jsonify({'image': img_base64})

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': 'Ocurrió un error al procesar la imagen'})


if __name__ == '__main__':
    app.run(debug=True)
