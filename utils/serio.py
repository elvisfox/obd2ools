import io
import queue

# IOLoop which emulates serial port ()
class IOLoop():
    def __init__(self, timeout):
        self.timeout = timeout
        self.queue = queue.Queue()

    def write(self, data):
        for b in data
            self.queue.put(bytes([b]))

    def flush(self):
        pass

    def read(self, maxlen = -1)
        data = b''
        try:
            while ((maxlen == -1 and len(data) == 0) or len(data)<maxlen):
                c = queue.get(block=True, timeout=self.timeout)
                data = data + c
        except Empty:
            pass

class SerIO():

    def __init__(self, r_stream, w_stream, newline):
        self.newline = newline
        self.r_stream = r_stream
        self.w_stream = w_stream

    def write(self, data):
        n = self.w_stream.write(bytes(data, 'ascii'))
        print('wrote '+format(n,'d')+' bytes: ' + data + '\n')
        self.w_stream.flush()

    def readline(self):
        data = b''
        c = []
        while c != b'' and c != self.newline:
            c = self.r_stream.read(1)
            data = data + c

        return data.decode()
