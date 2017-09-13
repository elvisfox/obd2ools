import io
import threading
import time

class elm327reader(threading.Thread):

    def command(self, cmd):
        # send a command
        self.sio.write(cmd+'\r')
        #self.sio.flush()

        time.sleep(0.05)

        resp = self.sio.readline()

        # leave only part until \r
        resp = resp.split('\r')[0]

        print('got: '+resp+'\n')

        return resp

    def reset(self):
        resp = self.command('ATE0')
        if resp != 'OK':
            return False

        resp = self.command('ATZ')
        if resp != 'ELM327 v1.5':
            return False

        resp = self.command('ATH0')
        if resp != 'OK':
            return False

        resp = self.command('ATM0')
        if resp != 'OK':
            return False

        resp = self.command('ATL0')
        if resp != 'OK':
            return False

        return True

    def __init__(self, stream):
        super().__init__()
        self.should_live = 1
        self.sio = stream
    
    def run(self):
        # init
        if not self.reset():
            self.should_live = 0;
        # main loop
        while self.should_live == 1:
            pass
        # protocol close
        self.command('ATPC')

    def stop(self):
        self.should_live = 0
