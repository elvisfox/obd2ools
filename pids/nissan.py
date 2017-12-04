

def linear(data, gain, offset):
	return data * gain + offset

def signed(data, bits, gain):
	sd = data
	if data > (1 << (bits-1)):
		sd -= 1 << bits;
	return sd * gain

#	 0			1			2			3				4		5		6		7
#	[header, pid,		example,	short name,		units,	format,	func,	[params]],
nissan_pids = [
	[0x806,	'0100',		'00000000',	'Sprt PIDs',	'deg',	'0.3f',	linear,	[0.0, 0]	],
	[0x7E0,	'10C0',		'',			'Nissan Init',	'',		'0.0f',	linear,	[0.0, 0]	],
	[0x7e0,	'221101',	'82',		'Coolant T',	'°С',	'0.0f',	linear,	[1.0, -50]	],
	[0x7E0,	'221106',	'0000',		'Intake Air T',	'°C',	'0.0f',	linear,	[1.0, -50]	],		#  
	[0x7E0,	'22110A',	'FF',		'Ign Adv',		'°',	'0.3f',	linear,	[-1.0, 110] ],		# Ignition Timing Advance Angle, 8-bit unsigned, 0 = 110deg, 1 = -1.0deg
	[0x7E0,	'221110',	'01',		'EVAP Purge Duty', '%',	'0.3f',	linear,	[0.5, 0]	],		# EVAP Purge Duty Cycle, 1 = 0.5%
	[0x7E0,	'221111',	'2D',		'Fuel T',		'°C',	'0.3f',	linear,	[1.0, -50]	],		# Fuel Temperature, offset=0x32 (50degC), 1 = 1degC
	[0x7E0,	'221114',	'34',		'Fuel Level',	'%',	'0.0f',	linear,	[1.0, 0]	],		# ??? 
	[0x7E0,	'221117',	'3A',		'Engine Load',	'%',	'0.0f',	linear,	[1.0/2.56, 0]],		# 
	[0x7E0,	'22111A',	'1C',		'H02S2 (B1)',	'V',	'0.2f',	linear,	[0.01, 0]	],		# 
	[0x7E0,	'22111B',	'1C',		'H02S2 (B2)',	'V',	'0.2f',	linear,	[0.01, 0]	],		# 
	[0x7E0,	'22111F',	'76',		'VVT Oil T',	'°C',	'0.3f',	linear,	[1.0, -50]	],		# VVT Oil Temperature, offset=0x32 (50degC), 1 = 1degC
	[0x7E0,	'221123',	'65',		'STFT B1',		'%',	'0.0f',	linear,	[1.0, -100]	],		# A/F Ratio Adjustment (B1), offset=0x64, 1 = 1%
	[0x7E0,	'221124',	'67',		'STFT B2',		'%',	'0.0f',	linear,	[1.0, -100]	],		# A/F Ratio Adjustment (B2), offset=0x64, 1 = 1%
	[0x7E0,	'221125',	'6A',		'LTFT B1',		'%',	'0.0f',	linear,	[1.0, -100]	],		# A/F Ratio Adjustment (B1), offset=0x64, 1 = 1%
	[0x7E0,	'221126',	'6C',		'LTFT B2',		'%',	'0.0f',	linear,	[1.0, -100]	],		# A/F Ratio Adjustment (B2), offset=0x64, 1 = 1%
#	[0x7e0,	'22112D',	'00',		'Ign Adv Adj',	'°',	'0.0f',	linear,	[1.0,	0]	],
	[0x7E0,	'221134',	'84',		'A/F Ratio',	'',		'0.0f',	linear,	[1.0,	0]	],		# 
	[0x7E0,	'221135',	'7F',		'INT/V TIM B1',	'°CA',	'0.1f',	linear,	[0.5, -64]	],		# Camshaft Advance Angle (B1), 7-bit signed, 0 = 0deg, 1 = +0.5deg
#	[0x7E0,	'221137',	'04',		'Cam Adv B2',	'deg',	'0.1f',	linear,	[0.5, -128]	],		# Camshaft Advance Angle (B2), 7-bit signed, 0 = -128deg, 1 = +1.0deg
	[0x7e0,	'221138',	'00',		'INT/V SOL(B1)', '%',	'0.3f',	linear,	[1.0/2.56, 0]],
	[0x7e0,	'221139',	'00',		'INT/V SOL(B2)', '%',	'0.3f',	linear,	[1.0/2.56, 0]],
	[0x7e0,	'22114E',	'8D',		'A/F S1 HTR(B1)', '%',	'0.3f',	linear,	[1.0/2.56, 0]],
	[0x7e0,	'22114F',	'A0',		'A/F S1 HTR(B2)', '%',	'0.3f',	linear,	[1.0/2.56, 0]],
	[0x7e0,	'221163',	'81',		'INT/V TIM B2',	'°CA',	'0.3f',	linear,	[0.5, -64]	],
	[0x7e0,	'221164',	'80',		'EXH/V TIM B1',	'°CA',	'0.3f',	linear,	[0.5, -64]	],
	[0x7e0,	'221165',	'7F',		'EXH/V TIM B2',	'°CA',	'0.3f',	linear,	[0.5, -64]	],
	[0x7e0,	'221179',	'BB',		'AC EVA TEMP',	'°C',	'0.1f',	linear,	[0.33, -30]	],
	[0x7e0,	'22117A',	'63',		'AC EVA TARGET','°C',	'0.1f',	linear,	[0.33, -30]	],
 	[0x7E0,	'221201',	'0050',		'RPM',			'rpm',	'0.0f',	linear,	[12.5,	0]	],		# Engine RPM, 1 = 12.5 rpm
 	[0x7E0,	'221204',	'00E4',		'MAF B1',		'V',	'0.2f',	linear,	[0.005, 0]	],		# MAF Voltage (B1), 1 = 5mV
 	[0x7E0,	'221205',	'01D8',		'MAF B2',		'V',	'0.2f',	linear,	[0.005, 0]	],		# MAF Voltage (B2), 1 = 5mV
 	[0x7E0,	'221206',	'0129',		'Inj Pulse B1',	'ms',	'0.2f',	linear,	[0.01,	0]	],		# Injector Pulse Width (B1), 100 = 1ms
 	[0x7E0,	'221207',	'0250',		'Inj Pulse B2',	'ms',	'0.2f',	linear,	[0.01,	0]	],		# Injector Pulse Width (B2), 100 = 1ms
 	[0x7E0,	'221208',	'2062',		'Fuel Base',	'ms',	'0.3f',	linear,	[0.001, 0]	],		# Fuel Base Pulse Width, 1000 = 1ms
 	[0x7E0,	'221209',	'01DA',		'Mass Air Flow','gm/s',	'0.2f',	linear,	[0.01,	0]	],		# Mass Air Flow, 100 = 1gm/s
# 	[0x7e0,	'22120B',	'0000',		'Current DTC',	'',		'04X',	linear,	[1,		0]	],
 	[0x7E0,	'22120D',	'01DA',		'Acc Pedal S1',	'V',	'0.2f',	linear,	[0.005, 0]	],		# 
 	[0x7E0,	'22120E',	'01DA',		'Acc Pedal S2',	'V',	'0.2f',	linear,	[0.005, 0]	],		# 
 	[0x7E0,	'22120F',	'01DA',		'TPS S1 (B1)',	'V',	'0.2f',	linear,	[0.005, 0]	],		# 
 	[0x7E0,	'221210',	'01DA',		'TPS S2 (B1)',	'V',	'0.2f',	linear,	[0.005, 0]	],		# 
 	[0x7E0,	'22121A',	'01DA',		'Car Speed',	'km/h',	'0.1f',	linear,	[0.1,	0]	],		#
 	[0x7e0,	'221225',	'01B5',		'A/F S1 (B1)',	'V',	'0.2f',	linear,	[0.005, 0]	],		#
	[0x7e0,	'221226',	'01AE',		'A/F S1 (B2)',	'V',	'0.2f',	linear,	[0.005, 0]	],		#
	[0x7e0,	'22122F',	'0000',		'VTC DTY EX B1','%',	'0.3f',	linear,	[3200/32768, 0]],
	[0x7e0,	'221230',	'0000',		'VTC DTY EX B2','%',	'0.3f',	linear,	[3200/32768, 0]],
	[0x7e0,	'221246',	'01F7',		'BAT CUR SEN',	'V',	'0.3f',	linear,	[0.005, 0]	],
	[0x7e0,	'221249',	'FFEB',		'A/F Adj (B1)',	'%',	'0.1f',	signed,	[16, 0.2]	],		#
	[0x7e0,	'22124A',	'FFE7',		'A/F Adj (B2)',	'%',	'0.1f',	signed,	[16, 0.2]	],		#
	[0x7e0,	'22124B',	'006E',		'TPS S1 (B2)',	'V',	'0.2f',	linear,	[0.005,	0]	],		#
	[0x7e0,	'22124C',	'006D',		'TPS S2 (B2)',	'V',	'0.2f',	linear,	[0.005,	0]	],		#
	[0x7E0,	'22122B',	'0064',		'Cruise Tgt',	'km/h',	'0.1f',	linear,	[0.1,	0]	],		# Cruise Control Target
#	[0x7e0,	'221174',	'00',		'CO ADJUSTMENT', '%',	'0.3f',	linear,	[1.0/2.56,	0]],
	[0x7e0,	'22130C',	'4100',		'SRT STATUS',	'',		'04X',	linear,	[1,		0]	],
]
