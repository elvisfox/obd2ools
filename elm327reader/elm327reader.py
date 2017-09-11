import io
import threading

class elm327reader(threading.Thread):

    def __init__(self, stream):
        super().__init__()
        self.should_live = 1
        self.sio = stream
    
    def run(self):
        while self.should_live == 1:
        	pass

    def stop(self):
        self.should_live = 0
