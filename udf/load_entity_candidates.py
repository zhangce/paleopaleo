#! /usr/bin/env python

from helper.easierlife import *

import codecs

#fo = codecs.open("/tmp/tmpoutput.tsv", 'w', 'utf-8')

for row in get_inputs():

	docid = row["documents.docid"]
	doc = deserialize(row["documents.document"])

	doc.get_entities_candidates()
	
#fo.close()