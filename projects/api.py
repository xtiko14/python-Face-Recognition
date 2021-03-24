import flask
from flask import Flask, request
import face_recognition
import urllib.request
import json

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def faceLoop(array):
  baseImg = array[0]['img']
  baseImg = urllib.request.urlopen(baseImg)
  baseEncode = face_recognition.load_image_file(baseImg)
  baseEncode = face_recognition.face_encodings(baseEncode)[0]
  for obj in array:
    testImg = urllib.request.urlopen(obj['img'])
    imageTest = face_recognition.load_image_file(testImg)
    imageTest = face_recognition.face_encodings(imageTest)[0]
    # Compare faces
    results = face_recognition.compare_faces(
        [baseEncode], imageTest)

    if results[0]:
        obj['verified'] = 1
    else:
        obj['verified'] = 0
  return array


@app.route('/', methods=['GET'])
def home():
  return "<h1>Image classifier.</p>"
@app.route('/classify', methods=['POST'])
def classify_image():
  data = request.json
  objRes = faceLoop(data)
  return json.dumps(objRes), 200
app.run()