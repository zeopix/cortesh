import os

class Logger:
    def log(self, message):
        #check if exists if not create it
        if not os.path.exists('../logs'):
            os.makedirs('../logs')
        with open('../logs/log.txt', 'a') as f:
            f.write(message + '\n')
        pass