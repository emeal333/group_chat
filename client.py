import tkinter as tk
import threading
import socket
import queue
from tkinter import simpledialog
import time

class App:
    def __init__(self, master):
        self.username = simpledialog.askstring("Username", "Please enter your name:")
        if not self.username:
            self.username = 'Anonymous'
        self.master = master
        master.title(f"Socket Reader: {self.username}")

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
            self.last_message = None
            try:
                data = self.sock.recv(1024)
                if not data:
                    break
                decoded = data.decode()
                print(f"[RECEIVED]: {decoded}") 
                self.data_queue.put(decoded)

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
            print("Sending message")
            full_message = f"{self.username}: {message}"
            try:
                self.sock.send(full_message.encode())
            except:
                pass

            # self.chat_display.configure(state='normal')
            # self.chat_display.insert(tk.END, full_message + '\n')
            # self.chat_display.configure(state='disabled')
            # self.chat_display.see(tk.END)

            self.input_box.delete(0, tk.END)
            

    def close(self):
        exiting_message = tk.Toplevel(self.master)
        exiting_message.title("Exiting Chat")
        tk.Label(exiting_message, text="Exiting Chat...").pack(padx=10, pady=10)
        exiting_message.geometry("200x100")
        print("Exiting message displayed maybe?")
        self.master.after(3000, lambda: self.close_chat(exiting_message))

    def close_chat(self, exiting_message):
        exiting_message.destroy()
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