#! /usr/bin/env python

from helper.easierlife import *

from ext.op.superviser_occurrences import *

superviser = OccurrencesSuperviser()
superviser.loadDict()

#superviser.extract()

for row in get_inputs():

	docid = row["documents.docid"]
	doc = deserialize(row["documents.document"])

	doc.get_relation_candidates(superviser, {'ROCK'}, {'LOCATION'})
