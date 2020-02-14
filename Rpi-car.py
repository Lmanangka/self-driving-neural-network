import socket
import picamera
import smbus
import threading
import io
import time
import struct

class car(object):
    def __init__(self, ip, port):
        self.address = 0x04
        self.i2c = smbus.SMBus(1)

        self.client = socket.socket()
        self.client.connect(('ip', port))
        self.conn = self.client.makefile('wb')

    def vision(self):
        with picamera.Picamera() as camera:
            self.camera.rotation = 180
            self.camera.resolution = (320, 240)
            self.camera.framerate = 15
            self.time.sleep(2)
            self.start = time.time()
            self.stream = io.BytesIO()

        for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
            self.conn.write(struct.pack('L', stream.tell()))
            self.conn.flush()
            self.stream.seek(0)
            self.conn.write(stream.read())
            self
