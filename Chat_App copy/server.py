import socket
import threading
import datetime

HOST = '127.0.0.1'
PORT = 1234
LISTENER_LIMIT = 5
active_clients = [] # List of all users currently connected

def add_message_to_file(message):
    with open("conversation.txt", "a") as file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"{timestamp}: {message}\n")

# Function to listen for incoming client messages
def listen_for_messages(client, username):

    while 1:
        message = client.recv(2048).decode('utf-8')
        if message != '':
            final_msg = username + ':' + message
            add_message_to_file(final_msg)
            send_messages_to_all(final_msg)
        else:
            print(f"The message sent from client {username} is empty")

# Function to send message to a single client
def send_message_to_client(client, message):

    client.sendall(message.encode())

# Function to send any new message to all clients currently connected to server
def send_messages_to_all(message):

    for user in active_clients:
        send_message_to_client(user[1], message)


# Function to handle client
def client_handler(client):
    
    # Server will listen for client message containing username
    # Contain the username
    while 1:
        username = client.recv(2048).decode('utf-8')
        if username != '':
            active_clients.append((username, client))
            prompt_message = "SERVER:" + f"{username} was added to the chat"
            send_messages_to_all(prompt_message)
            break
        else:
            print("Client username is empty")
            
    threading.Thread(target=listen_for_messages, args=(client, username, )).start()

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((HOST, PORT))
        print(f"Running server on {HOST} {PORT}")
    except:
        print(f"Unable to bind to host {HOST} and port {PORT}")
    
    server.listen(LISTENER_LIMIT)

    while 1:
        client, address = server.accept()
        print(f"Successfully connected to client {address[0]} {address[1]}")

        threading.Thread(target=client_handler, args=(client, )).start()

if __name__ == '__main__':
    main()