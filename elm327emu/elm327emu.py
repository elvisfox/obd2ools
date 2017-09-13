import io
import threading

# PIDS list (vendor specific for Nissan/Infiniti)
pids_list = [	[0x07E806,	'0100',		'00000000'	],
				[0x07E7E0,	'22110A',	'FF'		],		# Ignition Timing Advance Angle, 8-bit unsigned, 0 = 110deg, 1 = -1.0deg
				[0x07E7E0,	'221110',	'01'		],		# EVAP Purge Duty Cycle, 1 = 0.5%
				[0x07E7E0,	'221111',	'2D'		],		# Fuel Temperature, offset=0x32 (50degC), 1 = 1degC
				[0x07E7E0,	'22111F',	'76'		],		# VVT Oil Temperature, offset=0x32 (50degC), 1 = 1degC
			#	[0x07E7E0,	'221186',	'7F2212'	],		# ?? always answers 7F2212 w/o command header
				[0x07E7E0,	'221123',	'64'		],		# A/F Ratio Adjustment (B1), offset=0x64, 1 = 1%
				[0x07E7E0,	'221124',	'84'		],		# A/F Ratio Adjustment (B2), offset=0x64, 1 = 1%
				[0x07E7E0,	'221135',	'7F'		],		# Camshaft Advance Angle (B1), 7-bit signed, 0 = 0deg, 1 = +0.5deg
				[0x07E7E0,	'221137',	'04'		],		# Camshaft Advance Angle (B2), 7-bit signed, 0 = -128deg, 1 = +1.0deg
				[0x07E7E0,	'221138',	'20'		],		# Camshaft Valve Duty Cycle (B1), 1 = 1/2.56 %
				[0x07E7E0,	'221139',	'20'		],		# Camshaft Valve Duty Cycle (B2), 1 = 1/2.56 %
			 	[0x07E7E0,	'221201',	'0220'		],		# Engine RPM, 1 = 12.5 rpm
			 	[0x07E7E0,	'221204',	'00E4'		],		# MAF Voltage (B1), 1 = 5mV
			 	[0x07E7E0,	'221205',	'01D8'		],		# MAF Voltage (B2), 1 = 5mV
			 	[0x07E7E0,	'221206',	'0129'		],		# Injector Pulse Width (B1), 100 = 1ms
			 	[0x07E7E0,	'221207',	'0250'		],		# Injector Pulse Width (B2), 100 = 1ms
			 	[0x07E7E0,	'221208',	'2062'		],		# Fuel Base Pulse Width, 1000 = 1ms
			 	[0x07E7E0,	'221209',	'01DA'		],		# Mass Air Flow, 100 = 1gm/s
				[0x07E7E0,	'22122B',	'0064'		],		# Cruise Control Target, ???
				[0x07E7E0,	'221305',	'6844'		],		# Brake Switch ???
				[0x07E7E0,	'221307',	'4242'		],		# AC Compressor ???
				[0x07E7E0,	'221313',	'0008'		],		# Cooling Fan Low / High ???
			]

use_protocol = 6

class elm327emu(threading.Thread):

    def reset(self):
        # OBD state defaults
        self.protocol = use_protocol
        self.headers_on = 1
        self.header = 0x07E806
        self.timeout = 0

    def __init__(self, stream):
        super().__init__()
        self.should_live = 1
        self.sio = stream
        self.reset()
    
    def run(self):
        while self.should_live == 1:
            # get command from the port
            cmd = self.sio.readline()

            if len(cmd) == 0:
                continue

            # print command
            print('recv: '+cmd)

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
                    ans = str(protocol)
                elif sub[:2] == 'ST':
                    timeout = int(sub[2:])
                    print('  Timeout changed to '+str(timeout))
                    ans = 'OK'
                elif sub[:2] == 'SP':
                    protocol = int(sub[2:])
                    print('  Protocol changed to '+str(protocol))
                    ans = 'OK'
                elif sub[:1] == 'H':
                    headers_on = int(sub[1:])
                    print('  Headers_on changed to '+str(headers_on))
                    ans = 'OK'
                elif sub[:4] == ' SH ':
                    header = (header & 0xFFF000) | (int('0x'+sub[4:], 16) & 0x000FFF)
                    print('  Header changed to '+hex(header))
                    ans = 'OK'
                else:
                    print('  Unsupported command!')
                    ans = 'ERROR'
            elif cmd != '\r':
                # check used protocol
                if protocol != use_protocol:
                    ans = 'UNABLE TO CONNECT'
                else:
                    # default answer is now 'NO DATA'
                    ans = 'NO DATA'

                    # remove \r
                    sub = cmd[:-1]

                    # process the list of pids
                    for pid in pids_list:
                        if pid[0] == header and pid[1] == sub:
                            # prepare the reponse
                            ans = format(int('0x'+sub[:1], 16) | 4, 'X') + sub[1:] + pid[2]

                            # now add a header if needed
                            if headers_on:
                                ans = format(header, 'X') + ans

                            break

            # print response
            print('  send: '+ans)

            # new line character
            self.sio.write(ans+'\r\r>')
            #self.sio.flush()

    def stop(self):
        self.should_live = 0
