import time

from pids.nissan import *
from pids.parsed import *

# use 'loop' to run with emulator
#port_name = 'loop'
port_name = 'COM10'
baudrate = 115200

fast_mode = False
monitor_Vbat = True

pids_list = []
pids_list = pids_list + nissan_pids

init_list = [
	[0x7E0, '10C0']
]

selected_pids = [
#	'Acc Pedal S1',
	'Acc Pedal S2',
	'Mass Air Flow',
#	'MAF B1',
#	'MAF B2',
	'Inj Pulse B1',
	'Inj Pulse B2',
#	'Fuel Base',
	'RPM',
	'Ign Adv',
	'Engine Load',
#	'Ign Adv Adj',
#	'TPS S1 (B1)',
#	'TPS S2 (B1)',
#	'A/F Ratio',
#	'A/F Adj (B1)',
#	'A/F Adj (B2)',
#	'TPS S1 (B2)',
#	'TPS S2 (B2)',
	'A/F S1 (B1)',
	'A/F S1 (B2)',
#	'STFT B1',
#	'STFT B2',
#	'A/F S1 HTR(B1)',
#	'A/F S1 HTR(B2)',
#	'LTFT B1',
#	'LTFT B2',
#	'Car Speed',
	'INT/V TIM B1',
	'INT/V TIM B2',
	'EXH/V TIM B1',
	'EXH/V TIM B2',
	'INT/V SOL(B1)',
	'INT/V SOL(B2)',
	'VTC DTY EX B1',
	'VTC DTY EX B2',
#	'Engine Load',
	'H02S2 (B1)',
	'H02S2 (B2)',
#	'Current DTC',
#	'Coolant T',
#	'Intake Air T',
#	'VVT Oil T',
#	'CO ADJUSTMENT',
#	'SRT STATUS',
	'BAT CUR SEN',
]

gauges = [
	['RPM', 0, 3000],
	['Acc Pedal S1', 0.7, 4.2],
	['Acc Pedal S2', 0.7, 4.2],
	['TPS S1 (B1)', 0.5, 2.0],
	['TPS S2 (B1)', 0.5, 2.0],
	['TPS S1 (B2)', 0.5, 2.0],
	['TPS S2 (B2)', 0.5, 2.0],
	['Mass Air Flow', 0, 40],
	['A/F S1 (B1)', 0, 5.0],
	['A/F S1 (B2)', 0, 5.0],
	['MAF B1', 0, 5.0],
	['MAF B2', 0, 5.0],
	['Engine Load', 0, 100],
	['H02S2 (B1)', 0, 1.0],
	['H02S2 (B2)', 0, 1.0],
	['STFT B1', -30, 30],
	['STFT B2', -30, 30],
	['LTFT B1', -30, 30],
	['LTFT B2', -30, 30],
	['Car Speed', 0, 120],
	['Inj Pulse B1', 0, 10],
	['Inj Pulse B2', 0, 10],
	['A/F S1 HTR(B1)', 0, 100],
	['A/F S1 HTR(B2)', 0, 100],
	['BAT CUR SEN', 0, 5.0],
]

# update interval
interval = 0

# debug log
dbg_logfile = 'logs/debug_' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.txt'

# data log
data_logfile = 'logs/data_' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.csv'
