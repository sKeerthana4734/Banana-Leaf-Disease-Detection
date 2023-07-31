from flask import Flask, render_template, Response, request, redirect, url_for, jsonify
import cv2
import os
import sys
import numpy as np
import tensorflow as tf

app = Flask(__name__, template_folder='./templates')


# Load the saved model
pb_model_dir = "inference_graph/saved_model"
model = tf.saved_model.load(pb_model_dir)
category_index = {1: {'id': 1, 'name': 'BBS'},
                  2: {'id': 2, 'name': 'BBW'},
                  3: {'id': 3, 'name': 'Pestalotiopsis'}}


def format_image(image):
    image = tf.keras.preprocessing.image.img_to_array(image)
    image = tf.expand_dims(image, axis=0)
    image = tf.image.resize(image, [224, 224])
    image = tf.cast(image, tf.uint8)
    print("Image Formatting Successful")
    return image


def predict_disease():
    image = cv2.imread("F:/Work/BLDD/leaves/img.jpg")
    image = format_image(image)
    detections = model(image)
    threshold = 0.5  # Set the threshold for detection confidence
    detected_names = []
    for i in range(len(detections['detection_scores'][0])):
        score = detections['detection_scores'][0][i]
        if score >= threshold:
            class_id = int(detections['detection_classes'][0][i])
            class_name = category_index[class_id]['name']
            detected_names.append(class_name)
    output = {'detected_names': detected_names}
    print("Possibilities--{}".format(output))
    if output['detected_names']:
        return output['detected_names'][0]
    else:
        return "None"


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/index.html')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    image = request.files['image']
    image.save(os.path.join("leaves", "img.jpg"))
    response = predict_disease()
    print(response)
    # if response == "BBS":
    #     response = "Sigatoka Spots"
    # elif response == "BBW":
    #     response = "Bacterial Wilt"
    result = {}
    if response == "Pestalotiopsis":
        result['disease'] = response + "- A fungal disease"
        result['causes'] = "High Humidity, Poor plant Hygiene, Root rotting"
        result['prevention'] = "Proper water drainage, Fungicide Treatment"
    elif response == "BBS":
        result['disease'] = "Sigatoka Spots " + "- A fungal disease"
        result['causes'] = "Lack of nutrients, Warm weather"
        result['prevention'] = "Supply fertilizers rich in nutrients, Remove or burn infected leaves"

    elif response == "BBW":
        result['disease'] = "Bacterial Wilt"
        result['causes'] = "Infected soil, contaminated tools, Poor drainage"
        result['prevention'] = "Soil management, chemical treatment, proper irrigation"

    else:
        result['disease'] = "No disease detected"
        result['causes'] = ""
        result["prevention"] = ""
    print(result)

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
