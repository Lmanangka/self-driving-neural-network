import socket
import picamera
import smbus
import threading
import io
import time
import struct

class car(object):
    def __init__(self):
        self.address = 0x04
        self.i2c = smbus.SMBus(1)

        self.client = socket.socket()
        self.client.connect(('192.168.43.216', 1234))
        self.
