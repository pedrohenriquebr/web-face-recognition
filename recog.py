#!/usr/bin/env python3
import requests
import json
import os
import argparse

RECOGNITION_HOST=os.getenv('RECOGNITION_HOST','webfacerecognition.local')

def send_image(image_path):
   url = 'http://{RECOGNITION_HOST}:5000/api/recognition/svm'.format(
      RECOGNITION_HOST=RECOGNITION_HOST)
   files = {'file': open(image_path, 'rb')}
   r = requests.post(url, files=files,)
   response = []
   print('Retrieved ',len(r.text),' characters')
   
   if len(r.text) == 0 :
      print('Response is None')
      print(r.text)
      exit(1)
   
   try:
      response = json.loads(r.text)
   except Exception as e:
      print('I can\'t decode data to JSON: \n',r.text,'\n\n')

   return response


def main():
    parser = argparse.ArgumentParser(description='Face recognition CLI')
    parser.add_argument('image',help='Image file path')

    args = vars(parser.parse_args())

    recog = send_image(args['image'])
    for face in recog:
       print(face[0])


main()