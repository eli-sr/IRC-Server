#!/usr/bin/env python3
import socket
import sys
import signal
import threading

# Settings
RHOST = "192.168.1.134"
RPORT = 8000

# Setting up socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
try:
    s.connect((RHOST, RPORT))
except ConnectionRefusedError:
    print("[!] El servidor ha rechazado la conexion")
    s.close()
    sys.exit(-1)

# Closing the server
def close(sig, frame):
    print("\n[*] Closing connection...")
    s.close()
    sys.exit(0)
    
signal.signal(signal.SIGINT, close)

def receive():
    while True:
        try:
            data = s.recv(1024)
            print(data.decode("utf-8"))
        except:
            print('An error ocurred!')
            s.close()
            break

# Sign In
nick = input("Username: ")
s.sendall(nick.encode("utf-8"))
data = s.recv(1024)

thread = threading.Thread(target = receive)
thread.start()

while True:    
    # Message
    text = input()
    while text == "":
        text = input()
    msg  = text.encode("utf-8")
    
    # Sending the message
    try:
        s.sendall(msg)
        #data = s.recv(1024)

    except BrokenPipeError:
        print("[!] El servidor ha rechazado la conexion")
        s.close()
        sys.exit(-1)
