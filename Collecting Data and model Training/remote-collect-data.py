import socket
import cv2
import numpy as np
import time
import os
import pygame

class collect_data(object):
    def __init__(self, ip, port, inputSize):
        self.server = socket.socket()
        self.server.bind((ip, port))
        self.server.listen(0)

        self.conn, self.addr = self.server.accept()
        self.connection = self.conn.makefile('rb')
        print(self.addr)

        self.inputSize = inputSize
        self.inArray = np.zeros((4,4), 'float')
        for i in range(4):
            self.inArray[i, i] = 1

        self.stat = True

        pygame.init()
        pygame.display.set_mode((100, 100))

    def collect(self):
        savedFrame = 0
        totalFrame = 0

        start = cv2.getTickCount()
        x = np.empty((0, self.inputSize))
        y = np.empty((0, 4))

        try:
            stream_bytes = b''
            frame = 1

            while self.stat:
                stream_bytes += self.connection.read(1024)
                first = stream_bytes.find(b'\xff\xd8')
                last = stream_bytes.find(b'\xff\xd9')

                if first != -1 and last != -1:
                    jpg = stream_bytes[first : last + 2]
                    stream_bytes = stream_bytes[last + 2:]
                    image = cv2.imdecode(np.frombuffer(jpg, dtype = np.uint8), cv2.IMREAD_GRAYSCALE)

                    height, width = image.shape
                    roi = image[int(height / 2) : height, :]

                    cv2.imshow('image', image)

                    temp_array = roi.reshape(1, int(height / 2) * width).astype(np.float32)

                    frame += 1
                    totalFrame += 1

                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            input = pygame.key.get_pressed()

                            if input[pygame.K_w]:
                                savedFrame +=1
                                x = np.vstack((x, temp_array))
                                y = np.vstack((y, self.inArray[0]))
                                self.conn.sendall(str.encode('w'))
                                print("forward")

                            elif input[pygame.K_d]:
                                savedFrame +=1
                                x = np.vstack((x, temp_array))
                                y = np.vstack((y, self.inArray[1]))
                                self.conn.sendall(str.encode('d'))
                                print("right")

                            elif input[pygame.K_a]:
                                savedFrame +=1
                                x = np.vstack((x, temp_array))
                                y = np.vstack((y, self.inArray[2]))
                                self.conn.sendall(str.encode('a'))
                                print("left")

                            elif input[pygame.K_s]:
                                self.conn.sendall(str.encode('s'))
                                print("reverse")

                            elif input[pygame.K_x]:
                                print("exit")
                                self.conn.sendall(str.encode('e'))
                                self.stat = False
                                break

                        elif event.type == pygame.KEYUP:
                            self.conn.sendall(str.encode('q'))

                    if cv2.waitKey(1) & 0xFF == ord('x'):
                        break

            fileName = str(int(time.time()))
            directory = "training_data"
            if not os.path.exists(directory):
                os.makedirs(directory)

            try:
                np.savez(directory + '/' + fileName + '.npz', train = x, train_labels = y)
            except IOError as e:
                print(e)

            end = cv2.getTickCount()
            print("duration:, %.2fs" % ((end - start) / cv2.getTickFrequency()))

            print(x.shape)
            print(y.shape)
            print("Total frame: ", totalFrame)
            print("Saved frame: ", savedFrame)
            print("Dropped frame: ", totalFrame - savedFrame)

        finally:
            self.connection.close()
            self.server.close()

if __name__ == '__main__':
    ip = '0.0.0.0'
    port = 1234
    res = 120 * 320

    data = collect_data(ip, port, res)
    data.collect()
