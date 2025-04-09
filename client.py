import tkinter as tk
import threading
import socket
import queue

class App:
    def __init__(self, master):
        self.master = master
        master.title("Socket Reader")

        self.chat_display = tk.Text(master, height=10, width=40, state='disabled')
        self.chat_display.pack()

        self.input_box = tk.Entry(master, width=40)
        self.input_box.pack()
        self.input_box.bind("<Return>", self.send_message)

        self.data_queue = queue.Queue()
        self.running = True

        self.socket_thread = threading.Thread(target=self.read_socket)
        self.socket_thread.daemon = True  # Allow program to exit even if thread is running
        self.socket_thread.start()

        self.update_gui()

    def read_socket(self):
        host = '127.0.0.1'  # Or "localhost"
        port = 5000         # Replace with your port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        while self.running:
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                self.data_queue.put(data.decode())
            except:
                break

    def update_gui(self):
        try:
            while True:
                data = self.data_queue.get_nowait()
                self.chat_display.configure(state='normal')
                self.chat_display.insert(tk.END, data + '\n')
                self.chat_display.configure(state='disabled')
                self.chat_display.see(tk.END)
        except queue.Empty:
            pass
        if self.running:
            self.master.after(100, self.update_gui) # Check every 100 ms


    def send_message(self, event=None):
        message = self.input_box.get()
        if message:
            try:
                self.sock.send(message.encode())
            except:
                pass
            self.input_box.delete(0, tk.END)

    def close(self):
        self.running = False
        try:
            self.sock.close()
        except:
            pass
        self.master.destroy()

root = tk.Tk()
app = App(root)
root.protocol("WM_DELETE_WINDOW", app.close) # Handle window close event
root.mainloop()