import socket
import select

s = socket.socket()
s.bind(("0.0.0.0", 1337))
s.listen()
print("Server waiting for connections...")

sockets_list = [s]
clients = {}
registered_users = {}

def verify_user(client_socket):
    client_socket.send("Do you have an account? (yes/no): ".encode())
    print("Sent: Do you have an account?")
    response = client_socket.recv(1024).decode().strip().lower()
    print(f"User responded: {response}")

    if response == "no":
        client_socket.send("Create your username: ".encode())
        print("Sent: Create your username")
        username = client_socket.recv(1024).decode().strip()
        print(f"User chose username: {username}")

        if username in registered_users:
            client_socket.send("Username already exists. Try logging to the chat".encode())
            client_socket.close()
            return False

        client_socket.send("Create your password: ".encode())
        print("Sent: Create your password")
        password = client_socket.recv(1024).decode().strip()
        print(f"User created password: {password}")
        registered_users[username] = password
        clients[client_socket] = username
        client_socket.send(f"Registration successful! Welcome, {username}!".encode())
        print(f"Registration successful for {username}")
        print(registered_users)
        return True

    elif response == "yes":
        client_socket.send("Enter your username: ".encode())
        print("Sent: Enter your username")
        username = client_socket.recv(1024).decode().strip()
        print(f"User entered username: {username}")
        client_socket.send("Enter your password: ".encode())
        print("Sent: Enter your password")
        password = client_socket.recv(1024).decode().strip()
        print(f"User entered password")

        if username in registered_users and registered_users[username] == password:
            client_socket.send(f"Login successful! Welcome back, {username}".encode())
            clients[client_socket] = username
            print(f"Login successful for {username}")
            return True

        client_socket.send("Your details are incorrect... connection closed.".encode())
        print("Sent: Your details are incorrect... connection closed.")
        client_socket.close()
        return False

    else:
        client_socket.send("Invalid response. Connection closed.\n".encode())
        print("Sent: Invalid response. Connection closed.")
        client_socket.close()
        return False

while True:
    search_sockets, _, _ = select.select(sockets_list, [], [])
    for received_socket in search_sockets:
        if received_socket == s:
            cs, info = s.accept()
            sockets_list.append(cs)
            print(f"A new connection from {info}")
            print(sockets_list)

            if not verify_user(cs):
                sockets_list.remove(cs)
        else:
            try:
                message = received_socket.recv(4096)
                if message:
                    username = clients.get(received_socket, "Unknown")
                    print(f"{username}: {message.decode().strip()}")
                    for client in sockets_list:
                        if client != received_socket:
                            try:
                                client.send(f"{username}: {message.decode()}".encode())
                            except:
                                pass
                                continue
            except:
                username = clients.get(received_socket, "Unknown")
                print(f"{username} disconnected")
                for client in sockets_list:
                    if client != s and client != received_socket:
                        try:
                            client.send(f"{username} has left the chat.".encode())
                        except:
                            print("There was an error send disconnect message")
                            continue
                sockets_list.remove(received_socket)
                clients.pop(received_socket, None)
                received_socket.close()
                continue