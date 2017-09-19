import time

from pids.nissan import *
from pids.parsed import *

# use 'loop' to run with emulator
port_name = 'loop'
#port_name = 'COM10'
baudrate = 115200

fast_mode = False

pids_list = []
pids_list = pids_list + nissan_pids

init_list = [
	[0x7E0, '10C0']
]

selected_pids = [
	'Acc Pedal S2',
	'Mass Air Flow',
	'Inj Pulse B1',
	'Inj Pulse B2',
	'Fuel Base',
	'RPM',
	'A/F S1 (B1)',
	'A/F S1 (B2)',
	'Engine Load',
	'H02S2 (B1)',
	'H02S2 (B2)',
]

gauges = [
	['RPM', 0, 4000],
	['Acc Pedal S2', 0.7, 4.2],
	['TPS S1', 0, 5.0],
	['A/F S1 (B1)', 0, 5.0],
	['A/F S1 (B2)', 0, 5.0],
	['Engine Load', 0, 100],
	['H02S2 (B1)', 0, 1.0],
	['H02S2 (B2)', 0, 1.0],
]

# update interval
interval = 0

# debug log
dbg_logfile = 'logs/debug_' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.txt'

# data log
data_logfile = 'logs/data_' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.csv'
