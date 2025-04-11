import tkinter as tk
import threading
import socket
import queue
from tkinter import simpledialog

class App:
    """
    Group chat application wiht TKinter GUI,
    connects to a TCP server to send and receive messages.
    """
    def __init__(self, master):
        """
        Initialize chat client GUI, gets username input and starts GUI update loop.
        """
        self.username = simpledialog.askstring("Username", "Please enter your name:")
        if not self.username:
            self.username = 'Anonymous'
        self.master = master
        master.title(f"Socket Reader: {self.username}")

        #Chat display
        self.chat_display = tk.Text(master, height=10, width=40, state='disabled')
        self.chat_display.pack()

        #Text box for user to type message
        self.input_box = tk.Entry(master, width=40)
        self.input_box.pack()
        self.input_box.bind("<Return>", self.send_message)

        #Store incoming messages
        self.data_queue = queue.Queue()
        self.running = True

        self.socket_thread = threading.Thread(target=self.read_socket)
        self.socket_thread.daemon = True  # Allow program to exit even if thread is running
        self.socket_thread.start()

        self.update_gui()

    def read_socket(self):
        """
        Connect to server and listen for messages,
        add received messages to the queue.
        """
        host = '127.0.0.1'  # Or "localhost"
        port = 5000         # Replace with your port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))
        self.sock.send(self.username.encode())

        while self.running:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                decoded = data.decode()

                #Handle server shutdown message

                if decoded == "__SERVER_SHUTDOWN__":
                    self.data_queue.put("Server has shut down. Exiting...")
                    self.running = False
                    break
                else:
                    print(f"[RECEIVED]: {decoded}") 
                    self.data_queue.put(decoded)

            except:
                break

    def update_gui(self):
        """
        Check queueu for new messages/displays them.
        """
        try:
            while True:
                data = self.data_queue.get_nowait()
                self.chat_display.configure(state='normal')
                self.chat_display.insert(tk.END, data + '\n')

                #Close app if shutdown message was received
                if self.running == False:
                    self.master.after(2000, self.close)
                
                self.chat_display.configure(state='disabled')
                self.chat_display.see(tk.END)

        except queue.Empty:
            pass
        if self.running:
            self.master.after(100, self.update_gui) # Check every 100 ms


    def send_message(self, event=None):
        """
        Sends message to server.
        """
        message = self.input_box.get()
        if message:
            full_message = f"{self.username}: {message}"
            try:
                self.sock.send(full_message.encode())
            except:
                pass

            self.input_box.delete(0, tk.END)
            

    def close(self):
        """
        Called wehn user closes window manually plus exiting message.
        """
        exiting_message = tk.Toplevel(self.master)
        exiting_message.title("Exiting Chat")
        tk.Label(exiting_message, text="Exiting Chat...").pack(padx=10, pady=10)
        exiting_message.geometry("200x100")
        self.master.after(3000, lambda: self.close_chat(exiting_message))

    def close_chat(self, exiting_message):
        """
        Close socket and destroy GUI
        """
        exiting_message.destroy()
        self.running = False
        try:
            self.sock.close()
        except:
            pass
        self.master.destroy()

#Program entry point
root = tk.Tk()
app = App(root)
root.protocol("WM_DELETE_WINDOW", app.close) # Handle window close event
root.mainloop()


