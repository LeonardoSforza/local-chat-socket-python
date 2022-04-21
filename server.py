import socket
import threading

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

clients = {
    "echobot": {
        "name": "echobot"
    }
}

def recMsg(thing):
    msg = ""
    char = ""
    while True:
        try:
            char = thing.recv(1).decode(FORMAT)
            if not char:
                break
            elif char == "\n":
                return msg
            else:
                msg += char
        except:
            return 0

def sendTo(reciever, sender, senderName, msg):
    for name in clients:
        if name == reciever:
            connection = clients[name]["conn"]
            toReciever = "DELIVERY " + senderName + " " + msg
            connection.send(toReciever.encode(FORMAT))
            toSender = "SEND-OK\n"
            sender.send(toSender.encode(FORMAT))
            return 1
    return 0

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    firstLoop = True
    while True:
        msg = recMsg(conn)
        if msg != 0 and msg:
            if firstLoop:
                name = msg.split()[1]
                if name in clients:
                    conn.send("IN-USE\n".encode(FORMAT))
                    continue
                else:
                    if len(clients) <= 64:
                        clients[name] = {
                            "name": name,
                            "conn": conn
                        }
                        response = "HELLO " + name + "\n"
                        conn.send(response.encode(FORMAT))
                        global clientName
                        clientName = name
                    firstLoop = False
                    print(clients)
                    continue
            elif msg.split()[0] == "WHO":
                for name in clients:
                    print(name)
                response = "WHO-OK"
                for name in clients:
                    response += " " + name + ","
                response = response[:-1]
                response += "\n"
                print(response)
                conn.send(response.encode(FORMAT))
            elif msg.split()[0] == 'SEND':
                destinationClient = msg.split()[1]
                destinationMessage = msg.split()[2:]

                message = ""
                for word in destinationMessage:
                    message += word + " "
                message = message[:-1]
                destinationMessage = message + "\n"

                if destinationClient == "echobot":
                    response = "DELIVERY echobot " + destinationMessage + "\n"
                    conn.send(response.encode(FORMAT))
                else:
                    findClient = True
                    for name in clients:
                        if name == destinationClient:
                            print("We found your guy :)", destinationClient, destinationMessage)
                            resp = sendTo(destinationClient, conn, clientName, destinationMessage)
                            if resp == 1:
                                findClient = True
                                break
                        else:
                            findClient = False
                    if not findClient:
                        response = "UNKNOWN\n"
                        conn.send(response.encode(FORMAT))
        else:
            clients.pop(clientName)
            break
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")

print("[STARTING] server is starting...")
start()