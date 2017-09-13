#!/usr/bin/env python3

import serial
import io
import threading
import time

from utils.serio import *
from elm327emu.elm327emu import *
from elm327reader.elm327reader import *

r_stream = IOLoop(0.1)
w_stream = IOLoop(0.1)

sio_elm = SerIO(w_stream, r_stream, b'\r')
sio_rdr = SerIO(r_stream, w_stream, b'>')

class StoppableThread(threading.Thread):

	def __init__(self):
		super(StoppableThread, self).__init__()
		self.should_live = 1
	
	def run(self):
		while self.should_live == 1:
			time.sleep(0.01)

	def stop(self):
		self.should_live = 0


# run elm327 thread
th_elm = elm327emu(sio_elm)
th_elm.start()

# run reader thread
th_rdr = elm327reader(sio_rdr)
th_rdr.start()

# loop until ctrl+c
try:
	while th_elm.is_alive() and th_rdr.is_alive():
		time.sleep(0.05)
except KeyboardInterrupt:
    pass

print('\nexiting...\n')

# shutdown threads
th_elm.stop()
th_rdr.stop()
