import time

from pids.nissan import *


pids_list = []
pids_list = pids_list + nissan_pids

selected_pids = [
	'RPM',
	'STFT B1',
	'STFT B2',
	'MAF B1',
	'MAF B2',
	'Mass Air Flow',
	'Inj Pulse B1',
	'Inj Pulse B2',
]

# update interval
interval = 0.2

# debug log
dbg_logfile = 'logs/debug_' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.txt'

# data log
data_logfile = 'logs/data_' + time.strftime('%Y-%m-%d_%H-%M-%S') + '.csv'
