from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from datetime import datetime
from werkzeug.utils import secure_filename
from os import path
import env
import helper

import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.utils import load_img, img_to_array
import numpy as np

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False
app.json.sort_keys = False
app.config['UPLOAD_FOLDER'] = "storages"
app.secret_key = "frutify"
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


def get_local_time():
    import pytz
    utc_time = datetime.utcnow()
    jakarta_timezone = pytz.timezone('Asia/Jakarta')
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(jakarta_timezone)
    return local_time

def composeReply(status, message, payload = None, statuscode = 200):
    reply = {}
    reply["SENDER"] = "BDMSTH - AI"
    reply["STATUS"] = status
    reply["MESSAGE"] = message
    reply["PAYLOAD"] = payload
    resp = jsonify(reply)
    resp.headers.add("Access-Control-Allow-Origin", "*")
    resp.status_code = statuscode
    return resp

def allowed_file(filename):
    IMAGE_ALLOWED_EXTENSION = ["png", "jpg", "jpeg"]
    return "." in filename and filename.rsplit(".", 1)[1].lower() in IMAGE_ALLOWED_EXTENSION

def saveFile(file):
    try:
        filename = str(get_local_time()).replace(":", "-") + secure_filename(file.filename)
        basedir = path.abspath(path.dirname(__file__))
        file.save(path.join(basedir, "uploads", filename))
        return filename
    except TypeError as error : return False


@app.route("/predict", methods = ["POST"])
def predict():
    
    file = request.files["image"]
    if "image" not in request.files: return composeReply("ERROR", "Gagal memuat file #1")
    if file.filename == "": return composeReply("ERROR", "Gagal memuat file #2")
    if not (file and allowed_file(file.filename)): 
        return composeReply("ERROR", "Gagal memuat file #3")
    filename = saveFile(file)

    loaded_model = tf.keras.models.load_model("Model.h5")
    model = loaded_model
    pathi = 'uploads\\' + filename
    img = load_img(pathi, target_size=(150, 150))
    x = img_to_array(img)
    x /= 255
    x = np.expand_dims(x, axis=0)
    images = np.vstack([x])

    labels = [
        "fresh",
        "parasite"
    ]
    probabilities = model.predict(images, batch_size=10)
    cls = np.argmax(probabilities[0])
    predicted_probability = probabilities[0][cls]
    predicted_label = labels[(cls)]

    print(probabilities)

    print(f"Probabilitas untuk kelas '{predicted_label}': {predicted_probability * 100:.2f}%")
    print(f"File {pathi} adalah {predicted_label}")

    data = {
        "filename": filename,
        "result": predicted_label,
        "precentage" : f"{predicted_probability * 100:.2f}%",
        "keterangan" : f"hati dinyatakan {'terdapat parasi' if predicted_label == 'parasite' else 'segar' }, dengan presentase {predicted_probability * 100:.2f}%"
    }

    return composeReply("SUCCESS", "prediction result", data)


@app.route("/uploads")
def uploads():
    path = request.args.get("path")
    return send_file("uploads\\" + path)
    

if __name__ == '__main__':
    app.run(host = env.runHost, port = env.runPort, debug = env.runDebug)