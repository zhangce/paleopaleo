#! /usr/bin/env python

from helper.easierlife import *

from ext.op.superviser_occurrences import *

superviser = OccurrencesSuperviser()
superviser.loadDict()

#superviser.extract()

ranks = {"subspecies":1,"species":2,"subgenus":3,"genus":4,"subtribe":5,"tribe":6,"subfamily":7,"family":8,"group":9,"superfamily":10,"infraorder":11,"suborder":12,"order":13,"superorder":14,"infraclass":15,"subclass":16,"class":17,"superclass":18,"subphylum":19,"phylum":20,"superphylum":21,"subkingdom":22,"kingdom":23,"superkingdom":24}
for r in ranks.keys():
	ranks[r+"!"] = ranks[r]

for row in get_inputs():

	docid = row["documents.docid"]
	doc = deserialize(row["documents.document"])

	doc.get_relation_candidates(superviser, ranks, {'ROCK'})

