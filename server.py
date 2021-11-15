"""
Benjamin Chen
Lab 5
Server Program
"""
import socket
import os
import threading
import sys

HOST = "localhost"      
PORT = 5551
max_clients = 3
timeout = 60
def getCurrentDir():
    #get current directory
    return os.getcwd()

def getListDir():
    #gets list of files and directories
    return os.listdir()

def changeDir(x):
    #changes directory to user selection
    try:
        os.chdir(os.getcwd() + '\\' + x)
    except FileNotFoundError:
        return 'Not Found'

def getDirectories():
    #recursively gets the directories of where os is
    listOfDir = []
    for (path, dirList, fileList) in os.walk(os.getcwd()):
        for d in dirList:
            listOfDir.append(os.path.join(path,d))
    return 'List of Directories found under ' + os.getcwd() + ':\n' + '\n'.join(listOfDir)

def run(conn, addr, dict):
    #method interacts with user and responds with user prompts
    #input: connection socket object, address from user, dictionary to get directories for each user
    while True:
        msg = dict[addr] + '\nc. change directory\nf. show files\nd. show directories\nq. quit'
        conn.send(msg.encode('utf-8'))
        fromClient = conn.recv(1024).decode('utf-8')
        if fromClient == 'g':
            os.chdir(dict[addr])
            conn.send(getCurrentDir().encode('utf-8'))
        elif fromClient == 'c':
            os.chdir(dict[addr])
            changePath = conn.recv(1024).decode('utf-8')
            x = changeDir(changePath)
            if x == 'Not Found': #checks if path exists, if not tell client
                conn.send('Path Does not Exist.'.encode('utf-8'))
            else:
                message = 'New Path:' + os.getcwd()
                conn.send(message.encode('utf-8'))
                dict[addr] = os.getcwd()
        elif fromClient == 'f':
            os.chdir(dict[addr])
            msg = 'List Of Files in '+ os.getcwd() + ':\n' + '\n'.join(getListDir())
            conn.send(msg.encode('utf-8'))
        elif fromClient == 'd':
            os.chdir(dict[addr])
            msg = getDirectories()
            conn.send(msg.encode('utf-8'))
        elif fromClient == 'q':
            break
        print("From client:", addr)
        print("Received:", fromClient)

#code for command line arguments
counter = 0
x = 0
y = 0
for n, arg in enumerate(sys.argv):
    counter +=1
    if counter == 1:
        x = counter
    if counter  == 2:
        y = counter
if counter == 1:
    pass
elif counter > 3:
    print('too many inputs!')
    sys.exit()
elif x == 0 or y == 0:
    print('usage: server.py numofclients timefortimer')
    sys.exit()
elif y > 120 and y < 3:
    print('timer is between 3 and 120 sec')
    sys.exit()
elif x > 5 or x < 0:
    print('num of clients < 5')
    sys.exit()

#main
s = socket.socket()
s.bind((HOST, PORT))
print("Server hostname:", HOST, "port:", PORT)
s.listen(max_clients)
threads = []
try:
    s.settimeout(timeout)
    counter = 0
    while True:
        (conn, addr) = s.accept()
        dict = {}
        dict[addr] = os.getcwd() #creates a dictonary of directories with addr as key
        t = threading.Thread(target = run, args = (conn, addr, dict))
        t.start()
        threads.append(t)
except Exception as e:
    for t in threads:
        t.join()
    print('The Server is exiting')