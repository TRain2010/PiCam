from django.db import models
import socket
import sys
import cv2
import pickle
import struct
import threading
import zlib


class VideoFeeds(object):

    def __init__(self, port):
        print("22222222222222")
        self.port = port
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("aaaaaaaaaaaaa")
        s.bind(('', self.port))
        self.conn, self.addr = s.accept()
        print("bbbbbbbbbbbb")
        self.data = b""
        self.payload_size = struct.calcsize(">L")
        threading.Thread(target=self.update, args=()).start()
        


    def get_frame(self):
        print("333333333333333333")
        return self.frame

    def update(self):
        print("444444444444444")
        while True:
            while (len(self.data) < self.payload_size):
                self.data += self.conn.recv(4096)
            packed_msg_size = self.data[:payload_size]
            self.data = self.data[payload_size:]
            msg_size = struct.unpack(">L", packed_msg_size)[0]
            while len(self.dat) < msg_size:
                self.data += self.conn.recv(4096)
            frame_data = self.data[:msg_size]
            self.data = self.data[msg_size:]

            self.frame=pickle.loads(frame_data, fix_imports=True, encoding="bytes")
