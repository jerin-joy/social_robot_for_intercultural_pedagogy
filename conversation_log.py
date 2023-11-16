import datetime

class ConversationLogger:
    def __init__(self, filename):
        self.filename = filename

    def log_message(self, sender, message):
        with open(self.filename, 'a') as file:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write("{} - {}: {}\n".format(timestamp, sender, message))
