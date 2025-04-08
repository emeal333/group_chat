import socket
from threading import Thread

def handleClient(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            message = data.decode()
            print("Client:", message)
            reply = "Server: " + message
            sock.send(reply.encode())
        except:
            break
    sock.close()

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 5000))
server_socket.listen(1)

print("Server is listening on port 5000...")

while True:
    connection_socket, _ = server_socket.accept()
    t = Thread(target=handleClient, args=(connection_socket,))
    t.start()
