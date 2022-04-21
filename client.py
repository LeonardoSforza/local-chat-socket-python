import socket
import threading

FORMAT = 'utf-8'
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

client = None


print(ADDR)

def recMsg():
    msg = ""
    char = ""
    while True:
        char = client.recv(1).decode(FORMAT)
        if not char:
            break
        elif char == "\n":
            return msg
        else:
            msg += char

def sendRules(text):
    if text == "!quit":
        return 0
    elif text == "!who":
        send("WHO\n")
    elif text[0] == "@":
        user = text.split()[0][1:]
        messageList = text.split()[1:]
        message = ""
        for word in messageList:
            message += word + " " 
        send("SEND " + user + " " + message + "\n")
    return 1

def send(msg):
    message = msg.encode()
    client.send(message)

def sendRespo(text):
    message = text.encode()
    client.send(message)
    serverResponse = recMsg()
    return serverResponse

def getName():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    
    name = input("Pls Enter you name: ")
    name = "HELLO-FROM " + name + "\n"
    answer = sendRespo(name)
    if answer.split()[0] == "IN-USE":
        print("The name you have entered is already taken")
        client.close()
        getName()
    elif answer.split()[0] == "BUSY":
        print("The server is full try again next time :(")
        client.close()
        getName()
    else:
        print('You have been connected to the server:) You can always quit by typing !quit. Send Messages and see "!who" is on the sever')

def getFromClient():
    while client.fileno() != -1:
        command = input("")
        if command:
            ans = sendRules(command)
            if ans == 0:
                client.shutdown(socket.SHUT_RDWR)
                client.close()
                listenForMessages.join()
                print('You have been disconnected from the server. See you next time :)')
                break

def listenServer():
    while True:
        try:
            data = recMsg()
            if data:
                dataWords = data.split()
                if dataWords[0] == 'WHO-OK':
                    dataWords = dataWords[1:]
                    print('Here is everyone on the server:')
                    output = ""
                    for word in dataWords:
                        output += word + " "
                    print(output)
                elif dataWords[0] == 'SEND-OK':
                    print('Your message has been sent :)')
                elif dataWords[0] == 'UNKNOWN':
                    print('That was not correct. Check for spelling mistakes or try a different user :)')
                elif dataWords[0] == 'DELIVERY':
                    print(f'You have recieved a message from {dataWords[1]}:')
                    dataWords = dataWords[2:]
                    output = ""
                    for word in dataWords:
                        output += word + " "
                    print(f"\t{output}")
                else:
                    print(data)
        except:
            break

def startChat():
    listenForMessages.start()
    getFromClient()

listenForMessages = threading.Thread(target=listenServer)
getName()
startChat()
