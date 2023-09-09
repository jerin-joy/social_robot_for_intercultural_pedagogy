from naoqi import ALProxy
import socket

# Implementing a socket server.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
server_socket.bind(('localhost', 12345))
server_socket.listen(1)
client_socket, client_address = server_socket.accept()

# tts = ALProxy("ALTextToSpeech", "ricenao.local", 9559)
# taskId = tts.post.say("Checking the response after speaking")
# while tts.isRunning(taskId):
#     pass
# # The robot has finished speaking, you can execute the next step in your code here
# print("The robot has done speaking")


while True:
    print("Waiting for a connection")
    client_socket, client_address = server_socket.accept()
    # print(f"Accepted connection from {client_address}")

    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        print(data)

        text = 'received'
        client_socket.sendall(text.encode())

    client_socket.close()
    
server_socket.close()

# while True:
#     data = client_socket.recv(1024)
#     if not data:
#         break
#     print (data)

#     text = 'received'
#     client_socket.sendall(text)


# client_socket.close()
# server_socket.close()


# To kill the port already in use:  kill -9 $(lsof -t -i:12345)
