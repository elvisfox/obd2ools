import io
import threading
import time
import datetime

class elm327reader(threading.Thread):

    def command(self, cmd):
        # send a command
        self.sio.write(cmd+'\r')
        #self.sio.flush()

        if self.dbg:
            self.dbg.write('cmd: ' + cmd + '\n')
            self.dbg.flush()

        resp = self.sio.readline()

        # leave only part until \r
        resp = resp.split('\r')[0]

        if self.dbg:
            self.dbg.write('  got: ' + resp + '\n')
            self.dbg.flush()

        return resp

    def reset(self):
        self.protocol = 0
        self.header = 0

    def init(self):
        resp = self.command('ATE0')         # Echo Off
        #if resp != 'OK':
        #    return False

        resp = self.command('ATL0')         # Linefeeds Off
        #if resp != 'OK':
        #    return False 

        resp = self.command('ATZ')          # Reset
        if resp != 'ELM327 v1.5':
            return False

        resp = self.command('ATH0')         # Headers off
        if resp != 'OK':
            return False

        resp = self.command('ATM0')         # Memory off
        if resp != 'OK':
            return False

        resp = self.command('ATST62')       # Timeout 4*62 ms
        if resp != 'OK':
            return False

        resp = self.command('ATAT1')        # Adaptive Timing Auto 1
        if resp != 'OK':
            return False

        if not self.set_protocol(6):
            return False

        resp = self.read_pid(0x07E806, '0100')
        if resp == None:
            return False

        return True

    def set_protocol(self, protocol):
        resp = self.command('ATSP' + format(protocol, 'd'))
        if resp != 'OK':
            return False

        self.protocol = protocol
        return True

    def set_header(self, header):
        if self.header == header:
            return True

        resp = self.command('AT SH ' + format(header & 0x000FFF, '03X'))
        if resp != 'OK':
            return False

        self.header = header
        return True

    def read_pid(self, header, pid):
        if not self.set_header(header):
            return None

        # request pid
        resp = self.command(pid)

        # split response into address and data
        ln = len(pid)
        addr = resp[:ln]
        data = resp[ln:]

        # Check address
        exp_addr = format(int(pid[:1], 16) | 4, 'X') + pid[1:]
        if addr != exp_addr:
            return None

        return int(data, 16)

    def __init__(self, stream, log_stream=None, debug_stream=None):
        super().__init__()
        self.should_live = 1
        self.sio = stream
        self.log = log_stream
        self.dbg = debug_stream
        self.pids_list = []
        self.readout_interval = 1
        self.reset()
    
    def run(self):
        # init
        if not self.init():
            self.should_live = 0;

        # log header
        if self.log:
            self.log.write('time')
            for pid in self.pids_list:
                self.log.write(',' + pid[3] + ' [' + pid[4] + ']')
            self.log.write('\n')
            self.log.flush()

        # main loop
        while self.should_live == 1:

            # get current time with milliseconds
            stamp = datetime.datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]

            for pid in self.pids_list:
                data = self.read_pid(pid[0], pid[1])

                if data == None:
                    continue

                # store value under pid[7]
                pid[8] = pid[6](data, *pid[7])

            #clear screen
            print('\x1b[2J\x1b[H')
            print('\tTime:\t\t' + stamp)

            if self.log:
                self.log.write(stamp)

            for pid in self.pids_list:
                try:
                    val = format(pid[8], pid[5])
                    print('\t' + pid[3] + ':\t' + ('\t' if len(pid[3])<7 else '') + val + ' ' + pid[4])
                    if self.log:
                        self.log.write(',' + val)
                except:
                    pass

            if self.log:
                self.log.write('\n')
                self.log.flush()

            time.sleep(self.readout_interval)

        # protocol close
        self.command('ATPC')

    def stop(self):
        self.should_live = 0

    def import_pids(self, pids_list, selected_pids):
        for pid in pids_list:
            if pid[3] in selected_pids:
                cpy = list(pid)
                cpy.append(0)
                self.pids_list.append(cpy)

