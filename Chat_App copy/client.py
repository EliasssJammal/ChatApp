import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox
import datetime

HOST = '127.0.0.1'
PORT = 1234

DARK_BLUE = '#162447'
LIGHT_BLUE = '#1F4068'
LIGHT_GREY = '#DDDDDD'
WHITE = 'white'
FONT = ("Helvetica", 14)
SMALL_FONT = ("Helvetica", 12)
BUTTON_FONT = ("Helvetica", 13)

# Create a socket object for client-server communication
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Function to add a message to the conversation file
def add_message_to_file(message):
    with open("conversation.txt", "a") as file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp}: {message}\n")

# Function to add a message to the GUI message box and conversation file
def add_message(message):
    message_box.config(state=tk.NORMAL) 
    message_box.insert(tk.END, message + '\n', 'user_message')
    message_box.config(state=tk.DISABLED)
    add_message_to_file(message)

# Function to establish connection to the server
def connect():
    try:
        client.connect((HOST, PORT))
        print(f"Successfully connected to server")
        add_message("[SERVER] Successfully connected to the server")
    except:
        messagebox.showerror("Unable to connect to server", f"Unable to connect to server {HOST} {PORT}")
    # Get the username from the entry field
    username = username_textbox.get()
    if username != '':
        client.sendall(username.encode())
    else:
        messagebox.showerror("Invalid username", "Username cannot be empty")
    # Start a thread to listen for messages from the server
    threading.Thread(target=listen_for_messages_from_server, args=(client, )).start()
    # Disable username entry and join button after connecting
    username_textbox.config(state=tk.DISABLED)
    username_button.config(state=tk.DISABLED)    
# Function to send a message to the server
def send_message():
    message = message_textbox.get()
    if message != '':
        client.sendall(message.encode())
        message_textbox.delete(0, len(message))
    else:
        messagebox.showerror("Empty message", "Message cannot be empty")
# Create main chat window
root = tk.Tk()
root.geometry("600x600") # Dimensions of chat window by pixels
root.title("Client Messenger")
root.resizable(False, False)
root.config(bg=DARK_BLUE)

# Create frames for top, middle, and bottom sections of chat window
top_frame = tk.Frame(root, bg=DARK_BLUE)
top_frame.pack(fill=tk.X)

middle_frame = tk.Frame(root, bg=LIGHT_BLUE)
middle_frame.pack(expand=True, fill=tk.BOTH)

bottom_frame = tk.Frame(root, bg=DARK_BLUE)
bottom_frame.pack(fill=tk.X)

# Create GUI elements for username entry and join button
username_label = tk.Label(top_frame, text="Enter username:", font=FONT, bg=DARK_BLUE, fg=LIGHT_GREY)
username_label.grid(row=0, column=0, padx=(10, 5), pady=10)

username_textbox = tk.Entry(top_frame, font=FONT, bg=LIGHT_GREY, fg=DARK_BLUE)
username_textbox.grid(row=0, column=1, padx=5, pady=10)

username_button = tk.Button(top_frame, text="Join", font=BUTTON_FONT, bg=LIGHT_GREY, fg=DARK_BLUE, command=connect)
username_button.grid(row=0, column=2, padx=(5, 10), pady=10)

# Create GUI elements for message entry and send button
message_textbox = tk.Entry(bottom_frame, font=FONT, bg=LIGHT_GREY, fg=DARK_BLUE)
message_textbox.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.X, expand=True)

message_button = tk.Button(bottom_frame, text="Send", font=BUTTON_FONT, bg=LIGHT_GREY, fg=DARK_BLUE, command=send_message)
message_button.pack(side=tk.RIGHT, padx=10, pady=10)

# Create a scrolled text box for displaying messages
message_box = scrolledtext.ScrolledText(middle_frame, font=SMALL_FONT, bg=LIGHT_BLUE, fg=WHITE)
message_box.tag_configure('user_message', foreground='white')
message_box.pack(fill=tk.BOTH, padx=10, pady=10, expand=True)
message_box.config(state=tk.DISABLED)

# Function to continuously listen for messages from the server
def listen_for_messages_from_server(client):

    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            username = message.split(":")[0]
            content = message.split(":")[1]
            add_message(f"[{username}] {content}")
        else:
            messagebox.showerror("Error", "Message received from client is empty")

def main():
    root.mainloop()

if __name__ == '__main__':
    main()
