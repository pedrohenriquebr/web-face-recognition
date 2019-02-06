#!/usr/bin/env python3
import requests
import json
import os
import argparse
from dotenv import load_dotenv

load_dotenv()

RECOGNITION_HOST=os.getenv('HOST_RUN','0.0.0.0')


def send_image(image_path):
   url = 'http://{RECOGNITION_HOST}:5000/api/recognition'.format(
      RECOGNITION_HOST=RECOGNITION_HOST)
   files = {'file': open(image_path, 'rb')}
   r = requests.post(url, files=files)
   return json.loads(r.text)



def main():
    parser = argparse.ArgumentParser(description='Face recognition CLI')
    parser.add_argument('image',help='Image file path')

    args = vars(parser.parse_args())

    recog = send_image(args['image'])
    for face in recog:
       print(face[0])


main()