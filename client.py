import cv2
import io
import socket
import struct
import time
import pickle
import zlib
from obj_detect import *

server_ip = '10.0.0.27'
server_port = 8888
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_ip, server_port))
connection = client_socket.makefile('wb')

cam = cv2.VideoCapture(0)

cam.set(3, 640)
cam.set(4, 480)


encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    ret, frame = cam.read()
    result, frame = cv2.imencode('.jpg', frame, encode_param)
    data = pickle.dumps(frame, 0)
    size = len(data)
    client_socket.sendall(struct.pack(">L", size) + data)

cam.release()