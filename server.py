from threading import Thread
import socket
import signal
import sys

#List keeps track of all connected clients
clients = []

def handleClient(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            message = data.decode()
            print("Client:", message)
            for client in clients:
                    try:
                        client.send(message.encode())
                    except:
                        pass
        except:
            break

    #Remove client form active clients when they disconnect
    clients.remove(sock)
    sock.close()

#set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 5000))
server_socket.listen(5)

print("server is listening on port 5000, waiting for response")


#Main server loop 
while True:
    connection_socket, _ = server_socket.accept()
    t = Thread(target=handleClient, args=(connection_socket,))
    t.start()
    # server_socket.close()