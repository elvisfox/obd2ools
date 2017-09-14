import io
import threading

use_protocol = 6

class elm327emu(threading.Thread):

    def reset(self):
        # OBD state defaults
        self.protocol = use_protocol
        self.headers_on = 1
        self.header = 0x806
        self.timeout = 0

    def __init__(self, stream, debug_stream=None):
        super().__init__()
        self.should_live = 1
        self.sio = stream
        self.dbg = debug_stream
        self.reset()
        self.pids_list = []
    
    def run(self):
        while self.should_live == 1:
            # get command from the port
            cmd = self.sio.readline()

            if len(cmd) == 0:
                continue

            # print command
            if self.dbg:
                self.dbg.write('recv: ' + cmd + '\n')
                self.dbg.flush()

            # default answer is empty
            ans = ''

            # process AT commands
            if cmd[:2] == 'AT':
                # remove AT and \r
                sub = cmd[2:-1]
                #print(sub)

                if sub == 'Z':
                    self.reset()
                    ans = 'ELM327 v1.5'
                elif sub == 'I':
                    ans = 'ELM327 v1.5'
                elif sub == '@1':
                    ans = 'OBDII to RS232 Interpreter'
                elif sub in ['L0', 'M0', 'E0', 'AT1', 'AT0', 'AT2', 'S0', 'PC']:
                    ans = 'OK'
                elif sub == 'DPN':          # respond protocol number
                    ans = str(self.protocol)
                elif sub[:2] == 'ST':
                    self.timeout = int(sub[2:])
                    print('  Timeout changed to '+str(self.timeout))
                    ans = 'OK'
                elif sub[:2] == 'SP':
                    self.protocol = int(sub[2:])
                    print('  Protocol changed to '+str(self.protocol))
                    ans = 'OK'
                elif sub[:1] == 'H':
                    self.headers_on = int(sub[1:])
                    print('  Headers_on changed to '+str(self.headers_on))
                    ans = 'OK'
                elif sub[:4] == ' SH ':
                    self.header = int(sub[4:], 16)
                    print('  Header changed to '+hex(self.header))
                    ans = 'OK'
                else:
                    print('  Unsupported command!')
                    ans = 'ERROR'
            elif cmd != '\r':
                # check used protocol
                if self.protocol != use_protocol:
                    ans = 'UNABLE TO CONNECT'
                else:
                    # default answer is now 'NO DATA'
                    ans = 'NO DATA'

                    # remove \r and spaces
                    sub = cmd[:-1].replace(' ', '')

                    # if odd number of digits, skip last one (expected number of responses)
                    if len(sub)%2 == 1:
                        sub = sub[:-1]

                    # process the list of pids
                    for pid in self.pids_list:
                        #print(pid[1])
                        if pid[0] == self.header and pid[1] == sub:
                            # prepare the reponse
                            ans = format(int('0x'+sub[:1], 16) | 4, 'X') + sub[1:] + pid[2]

                            # now add a header if needed
                            if self.headers_on:
                                ans = format(self.header, 'X') + ans

                            break

            # print response
            if self.dbg:
                self.dbg.write('  send: ' + ans + '\n')
                self.dbg.flush()

            # new line character
            self.sio.write(ans+'\r\r>')
            #self.sio.flush()

    def stop(self):
        self.should_live = 0
