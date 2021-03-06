import io
import threading
import time
import datetime

class elm327reader(threading.Thread):

    def command_fast(self, cmd):

        t = time.time()
        # send a command
        self.sio.write(cmd+'\r')
        #self.sio.flush()

        if self.dbg:
            self.dbg.write('fast: ' + cmd + '\n')
            self.dbg.flush()

        self.dbg.write('  sent in ' + format(time.time() - t, '0.3f') + ' sec\n')

        resp = '\r'
        while resp == '\r':
            resp = self.sio.readline(b'\r')
            self.dbg.write('  readline: ' + resp + ' (' + format(time.time() - t, '0.3f') + ' sec)\n')
            try:
                if resp[0] == '>':
                    resp = resp[1:]
            except:
                pass

        # leave only part until \r
        resp = resp.split('\r')[0]

        # check for > at the beginning
        

        if self.dbg:
            self.dbg.write('  resp: ' + resp + '\n')
            self.dbg.flush()

        return resp

    def command(self, cmd, wait=0):
        # send a command
        self.sio.write(cmd+'\r')
        #self.sio.flush()

        if self.dbg:
            self.dbg.write('cmd: ' + cmd + '\n')
            self.dbg.flush()

        if wait > 0:
            time.sleep(wait)

        resp = self.sio.readline()

        # leave only part until \r
        resp = resp.split('\r')[0]

        # check for > at the beginning

        if self.dbg:
            self.dbg.write('  got: ' + resp + '\n')
            self.dbg.flush()

        return resp

    def reset(self):
        self.protocol = 0
        self.header = 0

    def init(self):

        resp = self.command('ATZ', 1.2)          # Reset
        #if resp != 'ELM327 v1.5':
        #    return False
        #time.sleep(1.5)

        resp = self.command('ATE0')         # Echo Off
        #if resp != 'OK':
        #    return False

        resp = self.command('ATL0')         # Linefeeds Off
        #if resp != 'OK':
        #    return False 

        resp = self.command('ATI')          # Reset
        if resp != 'ELM327 v1.5':
            return False

        resp = self.command('ATS0')         # Spaces off
        if resp != 'OK':
            return False

        resp = self.command('ATH0')         # Headers off
        if resp != 'OK':
            return False

        resp = self.command('ATM0')         # Memory off
        if resp != 'OK':
            return False

        if not self.set_protocol(6):
            return False

        resp = self.command('ATST10')       # Timeout 4*25 ms
        if resp != 'OK':
            return False

        resp = self.command('ATAT0')        # Adaptive Timing Auto 1
        if resp != 'OK':
            return False

        resp = self.read_pid(0x806, '0100')
        if resp == None:
            return False

        for pid in self.init_list:
            if self.read_pid(pid[0], pid[1]) == None:
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

        cmd = 'AT SH ' + format(header, '03X')

        if self.fast_mode:
            resp = self.command_fast(cmd)
        else:
            resp = self.command(cmd)

        if resp != 'OK':
            return False

        self.header = header
        return True

    def read_pid(self, header, pid):
        if not self.set_header(header):
            return None

        # measure time
        t = time.time()

        # request pid
        if self.fast_mode:
            resp = self.command_fast(pid+' 1')
        else:
            resp = self.command(pid+' 1')

        # debug output - time
        self.dbg.write('  spent ' + format(time.time() - t, '0.3f') + ' sec\n')

        # split response into address and data
        ln = len(pid)
        addr = resp[:ln]
        data = resp[ln:]

        # Check address
        exp_addr = format(int(pid[:1], 16) | 4, 'X') + pid[1:]
        if addr != exp_addr:
            return None

        try:
            result = int(data, 16)
        except:
            result = 0

        return result

    def read_Vbat(self):
        # measure time
        t = time.time()

        if self.fast_mode:
            resp = self.command_fast('AT RV')
        else:
            resp = self.command('AT RV')

        # debug output - time
        self.dbg.write('  spent ' + format(time.time() - t, '0.3f') + ' sec\n')

        return resp

    def __init__(self, stream, log_stream=None, debug_stream=None):
        super().__init__()
        self.should_live = 1
        self.sio = stream
        self.log = log_stream
        self.dbg = debug_stream
        self.pids_list = []
        self.init_list = []
        self.gauges = []
        self.fast_mode = False
        self.readout_interval = 1
        self.init_time = time.time()
        self.monitor_Vbat = False
        self.reset()
    
    def run(self):
        # init
        if not self.init():
            self.should_live = 0;

        # log header
        if self.log:
            self.log.write('time')
            if self.monitor_Vbat:
                self.log.write(',Vbat')
            for pid in self.pids_list:
                self.log.write(',' + 'Time [s]' + ',' + pid[3] + ' [' + pid[4] + ']')
            self.log.write('\n')
            self.log.flush()

        # main loop
        while self.should_live == 1:

            # get current time with milliseconds
            stamp = format(time.time() - self.init_time, '0.3f')  #datetime.datetime.utcnow().strftime('%H:%M:%S.%f')[:-3]

            for pid in self.pids_list:
                data = self.read_pid(pid[0], pid[1])

                if data == None:
                    pid[8] = None
                    continue

                # store value under pid[7]
                pid[8] = pid[6](data, *pid[7])
                pid[9] = time.time() - self.init_time

            # read battery voltage if requested
            if self.monitor_Vbat:
                vbat = self.read_Vbat()

            #clear screen
            print('\x1b[2J\x1b[H')
            print('\tTime:\t\t' + stamp + ' s')

            if self.log:
                self.log.write(stamp)

            # print battery voltage
            if self.monitor_Vbat:
                print('\tBattery:\t' + vbat)
                self.log.write(',' + vbat)

            for pid in self.pids_list:
                try:
                    if pid[8] != None:
                        val = format(pid[8], pid[5])
                    else:
                        val = '--'
                    print('\t' + pid[3] + ':\t' + ('\t' if len(pid[3])<7 else '') + val + ' ' + pid[4])
                    if self.log:
                        self.log.write(',' + format(pid[9], '0.3f') + ',' + val)

                    # some shit
                    for g in self.gauges:
                        if pid[3] == g[0]:
                            num = int(max(min((pid[8] - g[1]) * 60 // (g[2] - g[1]), 60), 0))
                            print('    [' + '#' * num + ' ' * (60-num) + ']')
                except:
                    pass

            if self.log:
                self.log.write('\n')
                self.log.flush()

            if self.readout_interval:
                time.sleep(self.readout_interval)

        # protocol close
        self.command('ATPC')

    def scan_pids(self, pids_list):
        # init
        if not self.init():
            return
        # prepare empty list
        sc_pids = list()
        # readout pids from the list
        for pid in pids_list:
            if not self.set_header(pid[0]):
                return None

            # request pid
            if self.fast_mode:
                resp = self.command_fast(pid[1]+' 1')
            else:
                resp = self.command(pid[1]+' 1')

            # print response
            print(pid[3] + ' - ' + resp)

            ln = len(pid[1])
            addr = resp[:ln]
            data = resp[ln:]

            # Check address
            exp_addr = format(int(pid[1][:1], 16) | 4, 'X') + pid[1][1:]
            if addr == exp_addr:
                pid[2] = data
                sc_pids.append(pid)

        return sc_pids

    def stop(self):
        self.should_live = 0

    def import_pids(self, pids_list, selected_pids):
        for pid_name in selected_pids:
            for pid in pids_list:
                if pid[3] == pid_name:
                    cpy = list(pid)
                    cpy.append(0)
                    cpy.append(0)
                    self.pids_list.append(cpy)

