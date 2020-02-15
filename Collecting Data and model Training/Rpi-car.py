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
        self.com = self.client.makefile('wb')

    def vision(self):
        with picamera.PiCamera() as camera:
            camera.rotation = 180
            camera.resolution = (320, 240)
            camera.framerate = 15
            time.sleep(2)
            start = time.time()
            stream = io.BytesIO()

            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port = True):
                self.com.write(struct.pack('L', stream.tell()))
                self.com.flush()
                stream.seek(0)
                self.com.write(stream.read())
                stream.seek(0)
                stream.truncate()
        self.com.write(struct.pack('L', 0))

    def drive(self):
        while True:
            msg = self.client.recv(1024).decode()

            if msg == 'w':
                self.i2c.write_byte(self.address, 0)
                # print("forward")

            elif msg == 'd':
                self.i2c.write_byte(self.address, 1)
                # print("right")

            elif msg == 'a':
                self.i2c.write_byte(self.address, 2)
                # print("right")

            elif msg == 's':
                self.i2c.write_byte(self.address, 3)
                # print("reverse")

            elif msg == 'q':
                self.i2c.write_byte(self.address, 4)
                # print("stop")

            elif msg == 'e':
                break

    def run(self):
        t1 = threading.Thread(target = self.vision)
        t2 = threading.Thread(target = self.drive)
        t1.start()
        t2.start()
        t1.join()
        t2.join()

    def disconnect(self):
        self.com.close()
        self.client.close()

if __name__ == '__main__':
    ip = '192.168.43.216'
    port = 1234
    c = car(ip, port)

    try:
        c.run()
    finally:
        c.disconnect()
