import socket
import threading

while True:
    server_ip = input("Enter your IP address: \n")
    try:
        c = socket.socket()
        c.connect((server_ip, 1337))
        print(f"Successfully connected to {server_ip}:1337")
        break
    except Exception:
        print(f"Failed to connect to {server_ip}:1337")
        print("Please try again.\n")
logged_in_user = ""

def login_user():
    while True:
        try:
            message = c.recv(4096).decode()
            if not message:
                print("Something went wrong... disconnected from server")
                break

            print(f"Server says: {message.strip()}")

            msg_lower = message.lower().strip()

            if "do you have an account?" in msg_lower:
                response = input()
                c.send(response.encode())
                continue

            elif "create your username" in msg_lower or "enter your username" in msg_lower:
                username = input()
                c.send(username.encode())
                continue

            elif "create your password" in msg_lower or "enter your password" in msg_lower:
                password = input()
                c.send(password.encode())
                continue

            elif "registration successful" in msg_lower or "login successful" in msg_lower:
                print("You are now connected to the chat! You can start sending messages.")
                return username

        except Exception:
            print(f"Something went wrong... closing connection")
            return None

def send_message_loop():
    while True:
        message = input("Send your message: \n")
        if message.lower() == "exit":
            c.close()
            break
        c.send(f"{message}".encode())

def receive_message_loop():
    while True:
        try:
            message = c.recv(4096).decode()
            print(message)
        except:
            print("Error while handling socket message")
            c.close()
            break

logged_in_user = login_user()

if logged_in_user:
    threading.Thread(target=send_message_loop).start()
    threading.Thread(target=receive_message_loop).start()


