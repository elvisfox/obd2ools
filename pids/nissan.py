

def linear(data, gain, offset):
	return data * gain + offset

#	 0			1			2			3				4		5		6
#	[header,	pid,		example,	short name,		units,	func,	[params]],
nissan_pids = [
	[0x07E806,	'0100',		'00000000',	'Sprt PIDs',	'deg',	linear,	[-1.0, 110]	],
	[0x07E7E0,	'22110A',	'FF',		'Ign Adv',		'deg',	linear,	[-1.0, 110] ],		# Ignition Timing Advance Angle, 8-bit unsigned, 0 = 110deg, 1 = -1.0deg
	[0x07E7E0,	'221110',	'01',		'',				'deg',	linear,	[-1.0, 110]	],		# EVAP Purge Duty Cycle, 1 = 0.5%
	[0x07E7E0,	'221111',	'2D',		'',				'deg',	linear,	[-1.0, 110]	],		# Fuel Temperature, offset=0x32 (50degC), 1 = 1degC
	[0x07E7E0,	'22111F',	'76',		'',				'deg',	linear,	[-1.0, 110]	],		# VVT Oil Temperature, offset=0x32 (50degC), 1 = 1degC
#	[0x07E7E0,	'221186',	'7F2212',	'',				'deg',	linear,	[-1.0, 110] ],		# ?? always answers 7F2212 w/o command header
	[0x07E7E0,	'221123',	'64',		'',				'deg',	linear,	[-1.0, 110]	],		# A/F Ratio Adjustment (B1), offset=0x64, 1 = 1%
	[0x07E7E0,	'221124',	'84',		'',				'deg',	linear,	[-1.0, 110]	],		# A/F Ratio Adjustment (B2), offset=0x64, 1 = 1%
	[0x07E7E0,	'221135',	'7F',		'',				'deg',	linear,	[-1.0, 110]	],		# Camshaft Advance Angle (B1), 7-bit signed, 0 = 0deg, 1 = +0.5deg
	[0x07E7E0,	'221137',	'04',		'',				'deg',	linear,	[-1.0, 110]	],		# Camshaft Advance Angle (B2), 7-bit signed, 0 = -128deg, 1 = +1.0deg
	[0x07E7E0,	'221138',	'20',		'',				'deg',	linear,	[-1.0, 110]	],		# Camshaft Valve Duty Cycle (B1), 1 = 1/2.56 %
	[0x07E7E0,	'221139',	'20',		'',				'deg',	linear,	[-1.0, 110]	],		# Camshaft Valve Duty Cycle (B2), 1 = 1/2.56 %
 	[0x07E7E0,	'221201',	'0220',		'',				'deg',	linear,	[-1.0, 110]	],		# Engine RPM, 1 = 12.5 rpm
 	[0x07E7E0,	'221204',	'00E4',		'',				'deg',	linear,	[-1.0, 110]	],		# MAF Voltage (B1), 1 = 5mV
 	[0x07E7E0,	'221205',	'01D8',		'',				'deg',	linear,	[-1.0, 110]	],		# MAF Voltage (B2), 1 = 5mV
 	[0x07E7E0,	'221206',	'0129',		'',				'deg',	linear,	[-1.0, 110]	],		# Injector Pulse Width (B1), 100 = 1ms
 	[0x07E7E0,	'221207',	'0250',		'',				'deg',	linear,	[-1.0, 110]	],		# Injector Pulse Width (B2), 100 = 1ms
 	[0x07E7E0,	'221208',	'2062',		'',				'deg',	linear,	[-1.0, 110]	],		# Fuel Base Pulse Width, 1000 = 1ms
 	[0x07E7E0,	'221209',	'01DA',		'',				'deg',	linear,	[-1.0, 110]	],		# Mass Air Flow, 100 = 1gm/s
	[0x07E7E0,	'22122B',	'0064',		'',				'deg',	linear,	[-1.0, 110]	],		# Cruise Control Target, ???
	[0x07E7E0,	'221305',	'6844',		'',				'deg',	linear,	[-1.0, 110]	],		# Brake Switch ???
	[0x07E7E0,	'221307',	'4242',		'',				'deg',	linear,	[-1.0, 110]	],		# AC Compressor ???
	[0x07E7E0,	'221313',	'0008',		'',				'deg',	linear,	[-1.0, 110]	],		# Cooling Fan Low / High ???
]
