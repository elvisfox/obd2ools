import time

from pids.nissan import *

# use 'loop' to run with emulator
port_name = 'loop'
#port_name = 'COM10'
baudrate = 115200

fast_mode = True

pids_list = []
pids_list = pids_list + nissan_pids

init_list = [
	[0x7E0, '10C0']
]

selected_pids = [
	'RPM',
	'STFT B1',
	'STFT B2',
	'LTFT B1',
	'LTFT B2',
#	'MAF B1',
#	'MAF B2',
	'Mass Air Flow',
	'Inj Pulse B1',
	'Inj Pulse B2',
	'Fuel Base',
	'A/F Ratio',
	'Vacuum',
	'MAP',
#	'Intake Air T',
#	'Intake Mf P',
#	'Fuel T',
#	'Fuel Level',
#	'H02 B1 S1',
#	'H02 B2 S1',
#	'H02 B1 S2',
#	'H02 B2 S2',
#	'VVT Oil T',
#	'TPS 1',
#	'TPS 2',
#	'Fuel Pressure',
	'Acc Pedal S1',
#	'Acc Pedal S2',
	'TPS S1',
	'TPS S2',
#	'Car Speed',
]

# update interval
interval = 0.01

# debug log
dbg_logfile = 'logs/debug_' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.txt'

# data log
data_logfile = 'logs/data_' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.csv'
