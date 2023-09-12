import paramiko
from naoqi import ALProxy

# Your Nao's IP address and port
nao_ip = "ricenao.local"
nao_port = 9559

# Create a proxy to ALAudioPlayer
audio_player = ALProxy("ALAudioPlayer", nao_ip, nao_port)

# Path of the local file on your PC
local_file_path = "/home/jerin/robotics/Thesis/audio.wav"

# Path of the file on the robot
file_path_on_robot = "/home/nao/intercultural_pedagogy/audio.wav"

# Use paramiko for scp
transport = paramiko.Transport((nao_ip, 22))
transport.connect(username='nao', password='ricelab')

sftp = paramiko.SFTPClient.from_transport(transport)

while True:
    # Continuously upload and play audio files
    sftp.put(local_file_path, file_path_on_robot)
    
    # Load a local audio file on the robot
    file_id = audio_player.loadFile(file_path_on_robot)

    # Play the loaded file
    audio_player.play(file_id)

sftp.close()
transport.close()
