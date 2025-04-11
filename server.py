from threading import Thread
import socket
import signal
import sys

#List keeps track of all connected clients
clients = []

def server_shutdown(signal, frame):
    """
    Handles graceful shutdown,
    Send message to clients tha server is shutting down.
    """
    shutdown_message = "__SERVER_SHUTDOWN__"
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
    """
    Handles communication with client,
    receives username and lsitend for messages to reflect back,
    notifies others when a client joins or leaves
    """
    try:
        username = sock.recv(1024).decode()
    except:
        return
    
    welcome_message = f"{username} has joined the chat."
    goodbye_message = f"{username} has left the chat."

    print(welcome_message)
    for client in clients:
        try:
            client.send(welcome_message.encode())
        except:
            pass

    #Add client to active client list
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
                     try:
                         client.send(message.encode())
         except:
             break

    #Remove client form active clients when they disconnect
    clients.remove(sock)
    sock.close()

#set up the server socket
    print(goodbye_message)

    #notify remaining clients another client has left
    for client in clients:
        try:
            client.send(goodbye_message.encode())
        except:
            pass

#Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('127.0.0.1', 5000))
server_socket.listen(5)

print("server is listening on port 5000, waiting for response")

#Main server loop 
while True:
    connection_socket, _ = server_socket.accept()
    clients.append(connection_socket)  
    t = Thread(target=handleClient, args=(connection_socket,))
    t.start()
    # server_socket.close()
    t.start()