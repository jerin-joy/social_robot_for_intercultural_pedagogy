from naoqi import ALProxy
import socket
from conversation_log import ConversationLogger

logger = ConversationLogger('conversation.log')

# Implementing a socket server.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
server_socket.bind(('localhost', 12345))
server_socket.listen(1)
client_socket, client_address = server_socket.accept()

while True:
    print("Waiting for a connection")
    client_socket, client_address = server_socket.accept()
    # print("Accepted connection from {}".format(client_address))

    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        # Split the received data into sentence and language code
        sentence, language_code = data.split('|')
        logger.log_message('Robot', sentence)
        print("Received sentence: {}".format(sentence))
        print("Received language code: {}".format(language_code))

        text = 'received'
        client_socket.sendall(text.encode())

    client_socket.close()
    
server_socket.close()

# To kill the port already in use:  kill -9 $(lsof -t -i:12345)
