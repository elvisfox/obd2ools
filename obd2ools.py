#!/usr/bin/env python3

import serial
import io
import threading
import time
import os
import sys
import utils.save_pids

from utils.serio import *
from elm327emu.elm327emu import *
from elm327reader.elm327reader import *

from config import *

# ANSI support for Windows
if os.name == 'nt':
	import colorama
	colorama.init()

# open logfiles
f_dbg = None
f_log = None

if dbg_logfile:
	f_dbg = open(dbg_logfile, 'w')

if data_logfile:
	f_log = open(data_logfile, 'w')

ser = None
th_elm = None

if port_name == 'loop':
	r_stream = IOLoop(0.1)
	w_stream = IOLoop(0.1)

	sio_elm = SerIO(w_stream, r_stream, b'\r')
	sio_rdr = SerIO(r_stream, w_stream, b'>')

	# run elm327 thread
	th_elm = elm327emu(sio_elm, f_dbg)
	th_elm.pids_list = pids_list
	th_elm.start()
else:
	ser = serial.Serial(port_name, timeout=0.2, baudrate=baudrate)
	ser.read(1000)
	sio_rdr = SerIO(ser, ser, b'>')

# init reader
th_rdr = elm327reader(sio_rdr, f_log, f_dbg)
th_rdr.import_pids(pids_list, selected_pids)
th_rdr.init_list = init_list
th_rdr.readout_interval = interval
th_rdr.fast_mode = fast_mode
th_rdr.gauges = gauges

# run reader thread, or execute specific command
if len(sys.argv) >= 2 and sys.argv[1] == 'scan':
	scanned_pids = th_rdr.scan_pids(parsed_pids)
	utils.save_pids.generate('scanned', scanned_pids)
else:
	th_rdr.start()

# loop until ctrl+c
try:
	while th_rdr.is_alive():
		time.sleep(0.05)
except KeyboardInterrupt:
    pass

print('\nexiting...\n')

# shutdown threads
th_rdr.stop()
try:
	th_rdr.join()
except:
	pass

if th_elm:
	th_elm.stop()
	th_elm.join()

# close files
if ser:
	ser.close()
if f_dbg:
	f_dbg.close()
if f_log:
	f_log.close()
