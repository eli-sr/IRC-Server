#!/usr/bin/env python3
import socket
import threading

# Settings
LHOST = '192.168.1.134'
LPORT = 8000
connections = []
nicks = []

# Socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((LHOST,LPORT))
s.listen()

def broadcast(msg):
    for i in connections:
        i.send(msg.encode("utf-8"))

# Receive
def receive(conn,nick):
    while True:
        try:
            data = conn.recv(64)
            msg = data.decode("utf-8")
            if msg != "":
                msg = f"<{nick}> {msg}"
                broadcast(msg)
        except:
            print("error")
            print(connections)
            nicks.remove(nicks[connections.index(conn)])
            connections.remove(conn)
            conn.close()
            print()
            print(connections)
            break

# Main
print(f"[*] Starting server at {LHOST}:{LPORT}")
while True:
    # Waiting connection
    conn, cli_addr = s.accept() 

    # Adding nick and connection
    data = conn.recv(64)
    conn.send(data)
    nick = data.decode("utf-8")
    nicks.append(nick)
    connections.append(conn)

    print(f"[+] New client connected whit address: {cli_addr}")

    # Start the thread
    thread = threading.Thread(target = receive, args = (conn,nick,))
    thread.start()

