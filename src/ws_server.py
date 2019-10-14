
import asyncio
import websockets
import base64
import prediction_svm
import face_recognition
import numpy as np
from PIL import Image
import cv2
import io
from datauri import DataURI
import json
ENABLE_TMPIMAGE = False


def readb64(base64_string):
    imgdata = DataURI(base64_string)

    if ENABLE_TMPIMAGE:
        with open('../tmp/frame.png', 'wb') as f:
            f.write(imgdata.data)
    pimg = Image.open(io.BytesIO(imgdata.data))
    return cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)


async def hello(websocket, path):
    async for msg in websocket:
        d = json.dumps(prediction_svm.predict_frame(
            readb64(msg), model_path='../modelset/trained_svm_model.clf',))
        print(d)
        await websocket.send(d)


start_server = websockets.serve(hello, "localhost", 8080)
print('WS Server started')
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
