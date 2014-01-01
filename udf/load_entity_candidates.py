#! /usr/bin/env python

from helper.easierlife import *

import codecs

#fo = codecs.open("/tmp/tmpoutput.tsv", 'w', 'utf-8')

#for row in get_inputs():
#
#	docid = row["documents.docid"]
#	doc = deserialize(row["documents.document"])
#
#	doc.get_entities_candidates()
#	
#fo.close()

import os
for f in os.listdir(BASE_FOLDER + "/tmp/"):
	if f.endswith('.ent'):
		for l in open(BASE_FOLDER + "/tmp/" + f):
			print l.rstrip()