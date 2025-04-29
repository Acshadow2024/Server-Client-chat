# 🧠 Python Chat Application – Server & Client

This project is a basic **chat system** implemented in Python using sockets and threading. It supports multiple clients, basic user authentication (register/login), and real-time messaging.

---

## 🚀 Features

- ✅ Multi-client support using `select` (server side)
- 🔐 Simple user authentication (register / login)
- 💬 Real-time message broadcasting
- 💻 Console-based interface for both server and clients
- 🧵 Threaded client-side message handling

---

## 🧩 Project Structure

| File | Description |
|------|-------------|
| `server_project.py` | The server script that handles connections, authentication, and message broadcasting |
| `client_project.py` | The client script that connects to the server, authenticates, and allows sending/receiving messages |

---

## ⚙️ How to Run

### ▶️ Start the Server

```bash
python server_project.py
