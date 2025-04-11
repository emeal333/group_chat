from threading import Thread
import socket
import signal
import sys

clients = []

def server_shutdown(signal, frame):
    shutdown_message = "__SERVERSHUTDOWN__"
    print("Server disconneting...")
    for client in clients:
        try:
            client.send(shutdown_message.encode())
            client.close()
        except:
            pass

    server_socket.close()
    sys.exit(0)

signal.signal(signal.SIGINT, server_shutdown)

def handleClient(sock):
    clients.append(sock)
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            message = data.decode()
            print("Client:", message)
            # reply = "Server: " + message
            # sock.send(reply.encode())
        # except:
        #     break
            for client in clients:
                    if client != sock:
                        try:
                            client.send(message.encode())
                        except:
                            pass
        except:
            break

    clients.remove(sock)
    sock.close()

#set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 5000))
server_socket.listen(5)

print("server is listening on port 5000, waiting for response")


while True:
    connection_socket, _ = server_socket.accept()
    clients.append(connection_socket)  
    t = Thread(target=handleClient, args=(connection_socket,))
    t.start()
    # server_socket.close()
