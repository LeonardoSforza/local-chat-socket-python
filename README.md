# local-chat-socket-python
Server and Client code for a local chatting service using TCP.


This is an example of the response of the script:


client ->      HELLO-FROM <name>\n
server ->      HELLO <name>\n
 
client ->      WHO\n
server ->      WHO-OK <name1>,...,<name n>\n
  
client ->      SEND <user> <message>\n
server ->      SEND-OK\n

server ->      DELIVERY <sender> <msg>\n

Have fun :)
