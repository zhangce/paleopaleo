#! /usr/bin/env python

from helper.easierlife import *

from ext.op.superviser_occurrences import *



for row in get_inputs():

	#	log(row)

	o = {}
	for key in row:
		kk = key.split('.')[1]
		if kk != 'id' and kk != 'features':
			o[kk] = row[key]

	print json.dumps(o)


