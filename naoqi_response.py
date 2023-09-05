from naoqi import ALProxy
tts = ALProxy("ALTextToSpeech", "ricenao.local", 9559)
taskId = tts.post.say("Checking the response after speaking")
while tts.isRunning(taskId):
    pass
# The robot has finished speaking, you can execute the next step in your code here
print("The robot has done speaking")