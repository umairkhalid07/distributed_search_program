import socket
import pickle
import threading
import os
import time

SubServers = [['localhost',5001], ['localhost',5002], ['localhost',5003]]

def SubServerHandler(filename, responses, flags, index):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((SubServers[index][0],SubServers[index][1]))

    s.send(filename)
    response = pickle.loads(s.recv(1024))
    responses.append(response)
    flag = pickle.loads(s.recv(1024))
    flags.append(flag)

def SubServer(conn, address):
    print("Thread -> ", address)
    msg = conn.recv(1024)

    threads = []
    responses = []
    flags = []

    for x in range(3):
        temp_thread = threading.Thread(target=SubServerHandler, args = (msg, responses, flags, x))
        threads.append(temp_thread)
        temp_thread.start()

    for y in range(3):
        threads[y].join()

    flag_count = 0
    count = 0

    for temp1 in range(len(flags)):
        if (flags[temp1] == False):
            flag_count = flag_count + 1

    if (flag_count == 3 or flag_count > 3):
        message = 'File not found'
        conn.send(pickle.dumps(message))
    else:
        for temp2 in range(len(responses)):
            if (responses[temp2] == 'File Not Found'):
                responses[temp2] == ''
        for temp2 in range(len(responses)):
            if (responses[temp2] == ''):
                count = count + 1
        if (count == 3 or count > 3):
            message = 'File not found'
            conn.send(pickle.dumps(message))

        conn.send(pickle.dumps(responses))

    responses = []
    flags = []
    flag_count = 0
    
    conn.close()

def MainServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("localhost", 5000))
    s.listen(5)
    print('Main Server listening')

    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=SubServer, args = (conn, addr))
        thread.start()
        thread.join()

    s.close()

MainServer()