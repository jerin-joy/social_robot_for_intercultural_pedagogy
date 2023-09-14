from naoqi import ALProxy
import paramiko
import socket

# Your Nao's IP address and port
nao_ip = "ricenao.local"
nao_port = 9559

# Create a proxy to ALAudioPlayer
audio_player = ALProxy("ALAudioPlayer", nao_ip, nao_port)

# Path of the local file on your PC
local_file_path = "/home/jerin/robotics/Thesis/audio.wav"

# Path of the file on the robot
file_path_on_robot = "/home/nao/intercultural_pedagogy/audio.wav"

# Implementing a socket server.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
server_socket.bind(('localhost', 12345))
server_socket.listen(1)

while True:
    print("Waiting for a connection")
    client_socket, client_address = server_socket.accept()

    while True:
        data = client_socket.recv(1024)
        if not data:
            break

        # Split the received data into sentence and language code
        sentence, language_code = data.split('|')
        print("Received sentence: {}".format(sentence))
        print("Received language code: {}".format(language_code))

        # Use paramiko for scp
        transport = paramiko.Transport((nao_ip, 22))
        transport.connect(username='nao', password='ricelab')

        sftp = paramiko.SFTPClient.from_transport(transport)

        # Upload and play audio files
        sftp.put(local_file_path, file_path_on_robot)

        # Load a local audio file on the robot
        file_id = audio_player.loadFile(file_path_on_robot)

        # Play the loaded file
        audio_player.play(file_id)

        sftp.close()
        transport.close()

        text = 'finished'
        client_socket.sendall(text.encode())

    client_socket.close()
    
server_socket.close()
