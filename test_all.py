#!/usr/bin/env python3
import requests
import json
import os

RECOGNITION_HOST='0.0.0.0'

def send_image(image_path):
   url = 'http://{RECOGNITION_HOST}:5000/api/recognition'.format(
      RECOGNITION_HOST=RECOGNITION_HOST)
   files = {'file': open(image_path, 'rb')}
   r = requests.post(url, files=files)
   return json.loads(r.text)

def load_labels(filepath):
    labels = {}
    with open(filepath,'rt') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            labels[i+1] = lines[i].strip()

    return labels

def predict_testnames(testdir):
    test_names = {}
    for img in os.listdir(testdir):
        if img == "labels.txt":
            continue
        full_path = os.path.join(testdir,img)
        print(full_path)
        name = send_image(full_path)
        person_id = int(img.split('.')[0])
        test_names[person_id]=name[0][0]

    return test_names

def main():
    testdir='testset'
    test_names = predict_testnames(testdir)
    labels = load_labels(os.path.join(testdir,'labels.txt'))
    hits = 0
    rate = 0

    for j in range(len(labels)):
        if labels[j+1] == test_names[j+1]:
            hits+=1

    rate = hits/len(labels)*100


    print(
    """
    Hits: {}
    Rate: {:0.2f}%
    Total: {}
    """.format(hits,rate,len(labels)))

main()