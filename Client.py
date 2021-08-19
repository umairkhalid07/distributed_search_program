import socket
import pickle
import threading
import os
import time

name = input("Enter file name : ")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.connect(("localhost", 5000))

s.send(name.encode())
reply = s.recv(1024)
print(pickle.loads(reply))

s.close()