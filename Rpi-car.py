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
        self.conn.client.makefile('wb')

    def vision(self):
        with picamera.Picamera() as camera:
            camera.rotation = 180
            camera.resolution = (320, 240)
            camera.framerate = 15
            time.sleep(2)
