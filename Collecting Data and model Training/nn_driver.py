import cv2
import numpy as np
import socket
from nn_model import neuralnetwork

class nnDriver(object):

    def __init__(self, model_path):

        self.s = socket.socket()
        self.s.bind(('0.0.0.0', 1234))
        self.s.listen(0)

        self.conn, self.addr = self.s.accept()
        self.connection = self.conn.makefile('rb')
        print(self.addr)

        self.nn = neuralnetwork()
        self.nn.load_model(model_path)

    def drive(self):
        stream_bytes = b' '
        try:
            # stream video frames one by one
            while True:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')

                if first != -1 and last != -1:
                    jpg = stream_bytes[first:last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    gray = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_GRAYSCALE)
                    image = cv2.imdecode(np.frombuffer(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)

                    # lower half of the image
                    height, width = gray.shape
                    roi = gray[int(height/2):height, :]

                    # cv2.imshow('image', image)
                    # cv2.imshow('gray', gray)
                    # cv2.imshow('mlp_image', roi)

                    # reshape image
                    image_array = roi.reshape(1, int(height/2) * width).astype(np.float32)

                    self.prediction = self.nn.predict(image_array)

                    #if self.prediction == 0:
                    #    self.conn.sendall(str.encode('w'))
                    #    print("forward")

                    #elif self.prediction == 1:
                    #    self.conn.sendall(str.encode('a'))
                    #    print("left")

                    #elif self.prediction == 2:
                    #    self.conn.sendall(str.encode('d'))
                    #    print("right")

                    #elif cv2.waitKey(1) & 0xFF ==('x'):
                    #    self.conn.sendall(str.encode('q'))
                    #    print("stop")

                    if self.prediction == 0:
                        self.conn.sendall(str.encode('w'))
                        print("forward")

                    elif self.prediction == 2:
                        self.conn.sendall(str.encode('a'))
                        print("left")

                    elif self.prediction == 1:
                        self.conn.sendall(str.encode('d'))
                        print("right")

                    elif cv2.waitKey(1) & 0xFF ==('x'):
                        self.conn.sendall(str.encode('q'))
                        print("stop")


        finally:
            cv2.destroyAllWindows()
            self.connection.close()
            self.s.close()

if __name__ == '__main__':

    path = "saved_model/nn_model.xml"
    car = nnDriver(path)
    car.drive()
