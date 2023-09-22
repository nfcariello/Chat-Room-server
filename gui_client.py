import socket
import select
import sys
import tkinter as tk
from tkinter import scrolledtext, Button, Entry, Label, messagebox

from threading import Thread


def send_message(event=None):
    message = entry.get()
    if message:
        server.send(message.encode())
        entry.delete(0, tk.END)
        append_to_chat(f"<You> {message}")


def receive_message():
    while True:
        sockets_list = [server]
        read_sockets, _, _ = select.select(sockets_list, [], [], 1)
        for socks in read_sockets:
            if socks == server:
                message = socks.recv(2048)
                append_to_chat(message.decode())


def append_to_chat(message):
    chat_text.configure(state='normal')
    chat_text.insert(tk.END, message + "\n")
    chat_text.configure(state='disabled')
    chat_text.see(tk.END)


def join_chatroom():
    ip = ip_entry.get()
    port = port_entry.get()
    name = name_entry.get()

    try:
        port = int(port)
        server.connect((ip, port))
        server.send(name.encode())

        ip_label.grid_remove()  # Hide the labels
        ip_entry.grid_remove()  # Hide the IP entry
        port_label.grid_remove()  # Hide the port labels
        port_entry.grid_remove()  # Hide the port entry
        name_label.grid_remove()  # Hide the name label
        name_entry.grid_remove()  # Hide the name entry
        join_button.grid_remove()  # Hide the join button

        chat_text.grid(row=0, column=0, columnspan=2,
                       sticky='nsew')  # Constrain chat_text to top, expand both horizontally and vertically
        entry_frame.grid(row=1, column=0, columnspan=2,
                         sticky='ew')  # Constrain entry_frame to the bottom, expand both horizontally
        entry.grid(row=0, column=0, sticky='ew')  # Constrain entry to the left, expand horizontally
        send_button.grid(row=0, column=1, sticky='ew')  # Constrain send_button to the right, expand horizontally
        entry.configure(state='normal')
        send_button.configure(state='normal')

        root.grid_rowconfigure(0, weight=1)  # Allow chat_text to expand vertically
        root.grid_rowconfigure(1, weight=0)  # Constrain entry_frame vertically
        root.grid_columnconfigure(0, weight=1)  # Allow entry to expand horizontally
        root.grid_columnconfigure(1, weight=0)  # Constrain send_button horizontally

    except ValueError:
        messagebox.showerror("Error", "Port must be an integer.")
    except ConnectionRefusedError:
        messagebox.showerror("Error", "Connection refused. Check IP and port.")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Create a simple Tkinter GUI
root = tk.Tk()
root.title("Chat Client")

ip_label = Label(root, text="Enter IP Address:")
ip_label.grid(row=0, column=0, sticky='w')

ip_entry = Entry(root, width=40)
ip_entry.grid(row=0, column=1, sticky='ew')

port_label = Label(root, text="Enter Port (default 5000):")
port_label.grid(row=1, column=0, sticky='w')

# Set default value for port_entry
port_entry = Entry(root, width=40)
port_entry.insert(0, "5000")  # Default value
port_entry.grid(row=1, column=1, sticky='ew')

name_label = Label(root, text="Enter your name:")
name_label.grid(row=2, column=0, sticky='w')

name_entry = Entry(root, width=40)
name_entry.grid(row=2, column=1, sticky='ew')

join_button = Button(root, text="Join Chatroom", command=join_chatroom)
join_button.grid(row=3, column=0, columnspan=2, sticky='ew')

chat_text = scrolledtext.ScrolledText(root, state='disabled', width=40, height=10)

# Create a frame for the text entry and button
entry_frame = tk.Frame(root)

entry = Entry(entry_frame, width=40, state='normal')  # Enable the text entry
entry.bind("<Return>", send_message)  # Bind Enter key to send_message function
send_button = Button(entry_frame, text="Send", command=send_message, state='normal')  # Enable the Send button

# Start a thread to continuously receive and display messages
receive_thread = Thread(target=receive_message)
receive_thread.daemon = True
receive_thread.start()

# Configure row and column weights for resizing
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=0)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)  # Allow send_button to expand horizontally

root.mainloop()
