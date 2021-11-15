"""
Benjamin Chen
Lab 5
Client Program
"""
import socket
import sys
HOST = '127.0.0.1'
PORT = 5551

with socket.socket() as s :
    s.connect((HOST, PORT))
    print("Client connect to:", HOST, "port:", PORT)
    s.send('g'.encode('utf-8'))
    fromServer= s.recv(1024).decode('utf-8')
    print('Current Directory:', fromServer)
    mesg = input("Enter message to send or q to quit: ")

    if mesg == 'g' or mesg == 'd' or mesg == 'f':
        s.send(mesg.encode('utf-8'))
    elif mesg == 'c':
        s.send(mesg.encode('utf-8'))
        fromServer = s.recv(1024).decode('utf-8')
        mesg = input('Enter the file path:')
        s.send(mesg.encode('utf-8'))
    elif mesg == 'q':
        exit()
    fromServer = s.recv(1024).decode('utf-8')
    print(fromServer)
    while True:
            fromServer = s.recv(1024).decode('utf-8')
            print(fromServer)
            while True:
                mesg = input("Enter message to send or q to quit: ")
                if mesg == 'g' or mesg == 'd' or mesg == 'f' or mesg == 'q':
                    s.send(mesg.encode('utf-8'))
                    break
                elif mesg == 'c':
                    s.send(mesg.encode('utf-8'))
                    fromServer = s.recv(1024).decode('utf-8')
                    mesg = input('Enter the file path:')
                    s.send(mesg.encode('utf-8'))
                    break
            if mesg == 'q':
                s.close()
                break