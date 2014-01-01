#! /usr/bin/env python

from helper.easierlife import *

import re
from ext.doc.Relation import *
import math
class TitleRelationExtractor:
    
	def __init__(self):
			donothing = None
    
	def loadDict(self):
			donothing = None
    
	def extract(self, doc):
		fossils = []
		log("Extracting from ttitles")
		ranks = {"subspecies":1,"species":2,"subgenus":3,"genus":4,"subtribe":5,"tribe":6,"subfamily":7,"family":8,"group":9,"superfamily":10,"infraorder":11,"suborder":12,"order":13,"superorder":14,"infraclass":15,"subclass":16,"class":17,"superclass":18,"subphylum":19,"phylum":20,"superphylum":21,"subkingdom":22,"kingdom":23,"superkingdom":24}
		for sent in doc.entities:
			for e1 in doc.entities[sent]:
				if e1.type not in ['FORMATION', 'LOCATION', 'ROCK', 'INTERVAL']:
					if e1.entity not in fossils:
						fossils.append(e1.entity)
		for rel in doc.relations:
			if rel.type in ['FORMATION']:	
				if rel.entity1 in fossils:
					fossils.remove()
		remove_fossils = []
		for sent in doc.entities:
			for e1 in doc.entities[sent]:
				if e1.type in ranks and e1.entity in fossils:
					for sent2 in doc.entities:
						if math.fabs(sent - sent2)<6:
							for e2 in doc.entities[sent2]:
								if e2.type=='ROCK':
									doc.push_relation(Relation("FORMATION",e1, e2, "[NEARENOUGH]"))
									remove_fossils.append(e1.entity)
									
		for title_en in doc.titleentities:
				if title_en.type =='ROCK':
					for sent in doc.entities:
						for e1 in doc.entities[sent]:
							if e1.type in ranks and e1.entity in fossils and e1.entity not in remove_fossils:
								doc.push_relation(Relation("FORMATION",e1, title_en, "[TITLE CONTEXT]"))


