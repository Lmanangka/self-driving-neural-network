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
        self.client.connect((ip, port))
        self.conn = self.client.makefile('wb')

    def vision(self):
        with picamera.Picamera() as camera:
            camera.rotation = 180
            camera.resolution = (320, 240)
            camera.framerate = 15
            time.sleep(2)
            start = time.time()
            stream = io.BytesIO()

            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                self.conn.write(struct.pack('L', stream.tell()))
                self.conn.flush()
                stream.seek(0)
                self.conn.write(stream.read())
                stream.seek(0)
                stream.truncate()
        self.conn.write(struct.pack('L', 0))

    def remote(self):
        stat = True
        while stat:
            msg = self.client.recv(1024).decode()

            if msg == 'w':
                self.i2c.write_byte(self.address, 0)

            elif msg == 'a':
                self.i2c.write_byte(self.address, 1)

            elif msg == 'd':
                self.i2c.write_byte(self.address, 2)

            elif msg == 's':
                self.i2c.write_byte(self.address, 3)

            elif msg == 'q':
                self.i2c.write_byte(self.address, 4)


if __name__ == '__main__':
    addr = '192.168.43.216'
    p = 1234
    s = car(addr, p)

    try:
        thr1 = threading.Thread(target = s.vision)
        thr2 = threading.Thread(target = s.remote)

        thr1.start()
        thr2.start()

        thr1.join()
        thr2.join()

    finally:
