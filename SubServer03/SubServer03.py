import socket
import pickle
import threading
import os
import time

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(("localhost", 5003))
s.listen(5)
print('Sub Server 3 listening')

count = 0

while True:
    conn, addr = s.accept()
    print('Connected to : ', addr)
    msg = conn.recv(1024)

    for root, dirs, files in os.walk("."):
        for name in files:
            if name == msg.decode():
                count = count + 1
                reply = ''
                reply = 'File name : ' + str(name) + ' File Size : '+ str(os.stat(name).st_size) + ' Date Created : ' + str(time.ctime(os.stat(name).st_ctime)) + ' Retrieved -> Sub Server 3'
    
    if (count > 0):
        conn.send(pickle.dumps(reply))
        reply = ''
        found = True
        conn.send(pickle.dumps(found))
    else :
        reply = 'File Not Found'
        conn.send(pickle.dumps(reply))
        found = False
        conn.send(pickle.dumps(found))