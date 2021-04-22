from django.shortcuts import render
from django.views.decorators import gzip
from django.http import StreamingHttpResponse, HttpResponse
from objdetect.obj_detect import getObjects

import socket
import sys
import cv2
import pickle
import numpy as np
import struct ## new
import zlib


# Create your views here.
listen = False

def generate(targets=[]):
    global listen
    if (not listen):
        HOST=''
        PORT=8888
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.bind((HOST,PORT))
        s.listen(10)
        conn,addr=s.accept()
    payload_size = struct.calcsize(">L")
    listen = True
    data = b""
    while True:
        while len(data) < payload_size:
            data += conn.recv(4096)
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]
        while len(data) < msg_size:
            data += conn.recv(4096)
        frame_data = data[:msg_size]
        data = data[msg_size:]
        frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
        result,objectInfo = getObjects(frame,0.45,0.2,objects=targets)
        send_notification(objectInfo, targets)
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
        _, result = cv2.imencode('.jpg', result, encode_param)
        yield(b'--frame\r\n'
              b'Content-Type: image/jpg\r\n\r\n' + result.tobytes() + b'\r\n\r\n')

@gzip.gzip_page
def live_feed(reqeust):
    #return HttpResponse("OK")
    try:
        return StreamingHttpResponse(generate(['person', 'tv', 'cat']), content_type="multipart/x-mixed-replace;boundary=frame")
    except:
        return HttpResponse("No streaming")


def home(request):
    return render(request, 'streaming/index.html')

def setup(request):
    pass

def send_notification(objects, targets):
    for i in objects:
        if i[1] in targets:
            print(i[1])
