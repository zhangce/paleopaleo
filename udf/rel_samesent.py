#! /usr/bin/env python

from helper.easierlife import *
from cls.Document import *


def get_rel(docid, e1, e2, rel, feature):
	rs = {"docid":docid, "e1":serialize(e1), "e2":serialize(e2), "rel":rel, "feature":feature}
	return rs

def extract1(doc):
		
	for sent in doc.entities:

		rels ={}
		rels['FORMATIONLOCATION']={}
		rels['FORMATION']={}
		
		sss = doc.sents[sent]

		hist = {}
		
		for e1 in doc.entities[sent]:
			for e2 in doc.entities[sent]:
				if e1 == e2: continue

				if e2 + "|" + e1 in hist: continue
				hist[e1+"|"+e2] = 1

				if 'species' in e1.type and 'genus' in e2.type and e1.entity.lower().startswith(e2.entity.lower()):
					rs = get_rel(doc.docid, e1, e2, "belongs to", "belongs_to-TRIVIAL")
					print json.dumps(rs)
					
				ws = doc.sents[sent].wordseq_feature(e1, e2)
				if len(ws) > 100:
					ws = "LONGER_THAN_100"
				else:
					ws = "LONGER_THAN_50"

				has_semicomma = False
				if ';' in doc.sents[sent].wordseq_feature(e1, e2) and len(doc.sents[sent].words) > 10:
					has_semicomma = True

				has_comma = False
				if ',' in doc.sents[sent].wordseq_feature(e1, e2):
					has_comma = True

				if (e1.type == 'ROCK') and e2.type == 'INTERVAL' and ',' not in doc.sents[sent].wordseq_feature(e1, e2):
					rs = get_rel(doc.docid, e1, e2, "FORMATIONTEMPORAL", "FORMATIONTEMPORAL-TRIVIAL-HASCOMMA=%r-HASSEMICOMMA=%r" % (has_comma, has_semicomma))
					print json.dumps(rs)

					rs = get_rel(doc.docid, e1, e2, "FORMATIONTEMPORAL", "FORMATIONTEMPORAL-TRIVIAL-HASCOMMA=%r-HASSEMICOMMA=%r-ws=%s" % (has_comma, has_semicomma, ws))
					print json.dumps(rs)

				if is_fossil_entity(e1) and e2.type == 'ROCK':

					rs = get_rel(doc.docid, e1, e2, "FORMATION", "FORMATION-TRIVIAL-HASCOMMA=%r-HASSEMICOMMA=%r" % (has_comma, has_semicomma))
					print json.dumps(rs)

					rs = get_rel(doc.docid, e1, e2, "FORMATION", "FORMATION-TRIVIAL-HASCOMMA=%r-HASSEMICOMMA=%r-ws=%s" % (has_comma, has_semicomma, ws))
					print json.dumps(rs)

					if has_comma==False and has_semicomma == False:

						if e2.entity not in rels['FORMATION'] and has_comma==False and has_semicomma == False:
							rels['FORMATION'][e2.entity]=(math.fabs(e1.words[0].insent_id-e2.words[0].insent_id), "", e1, e2)
						else:
							if math.fabs(e1.words[0].insent_id-e2.words[0].insent_id) < rels['FORMATION'][e2.entity][0]:
								rels['FORMATION'][e2.entity]=(math.fabs(e1.words[0].insent_id-e2.words[0].insent_id), "", e1, e2)

				if (e1.type == 'ROCK') and e2.type == 'LOCATION':

					rs = get_rel(doc.docid, e1, e2, "FORMATIONLOCATION", "FORMATIONLOCATION-TRIVIAL-HASCOMMA=%r-HASSEMICOMMA=%r" % (has_comma, has_semicomma))
					print json.dumps(rs)

					rs = get_rel(doc.docid, e1, e2, "FORMATIONLOCATION", "FORMATIONLOCATION-TRIVIAL-HASCOMMA=%r-HASSEMICOMMA=%r-ws=%s" % (has_comma, has_semicomma, ws))
					print json.dumps(rs)
					
					if has_comma==False and has_semicomma == False:

						if e1.entity not in rels['FORMATIONLOCATION']:
							rels['FORMATIONLOCATION'][e1.entity] = (math.fabs(e1.words[0].insent_id-e2.words[0].insent_id), "", e1, e2) 
						else:
							if math.fabs(e1.words[0].insent_id-e2.words[0].insent_id) < rels['FORMATIONLOCATION'][e1.entity][0]:
								rels['FORMATIONLOCATION'][e1.entity]=(math.fabs(e1.words[0].insent_id-e2.words[0].insent_id), "", e1, e2)
	
		for ent in rels['FORMATIONLOCATION']:
			rs = get_rel(doc.docid, rels['FORMATIONLOCATION'][ent][2], rels['FORMATIONLOCATION'][ent][3], "FORMATIONLOCATION", "FORMATIONLOCATION-NEAREST")
			print json.dumps(rs)
		for ent in rels['FORMATION']:
			rs = get_rel(doc.docid, rels['FORMATION'][ent][2], rels['FORMATION'][ent][3], "FORMATION", "FORMATION-NEAREST")
			print json.dumps(rs)

	for sentid in doc.entities:
		ctcount = 0
		for e in doc.entities[sentid]:
			if 'genus' in e.type or 'species' in e.type:
				ctcount = ctcount + 1
		if ctcount > 5 or 'fauna' in doc.sents[sentid].__repr__().lower() or 'foraminifer' in doc.sents[sentid].__repr__().lower():
			for sentid2 in range(sentid+1, sentid+6):
				if sentid2 in doc.sents and ('fauna' in doc.sents[sentid2].__repr__().lower() or 'foraminifer' in doc.sents[sentid2].__repr__().lower()) :					
					for e1 in doc.entities[sentid]:
						for e2 in doc.entities[sentid2]:
							if is_fossil_entity(e1) and e2.type == 'ROCK':
								rs = get_rel(doc.docid, e1, e2, "FORMATION", "FORMATION-FAUNA1")	
								print json.dumps(rs)										
					break
				
			formations = {}
			for sentid2 in range(max(0,sentid-3), sentid):
				if sentid2 not in doc.entities: continue
				for e in doc.entities[sentid2]:
					if e.type == 'ROCK' and 'formation' in e.entity:
						formations[e.entity] = e
		
			if len(formations) == 1:
				for k in formations.keys():
					e2 = formations[k]
					for e1 in doc.entities[sentid]:
						if is_fossil_entity(e1) and e2.type == 'ROCK':
							rs = get_rel(doc.docid, e1, e2, "FORMATION", "FORMATION-FAUNA2")	
							print json.dumps(rs)


	# single formation per document
	formations = {}
	for sentid in doc.entities:
		for e in doc.entities[sentid]:
			if e.type == 'ROCK':
				formations[e.entity] = e
					
	if len(formations) == 1:
		(e2,) = formations.values()
		
		for sentid in doc.entities:
			ctcount = 0
			for e in doc.entities[sentid]:
				if 'genus' in e.type or 'species' in e.type:
					ctcount = ctcount + 1
			if ctcount > 1:
				for e1 in doc.entities[sentid]:
					if is_fossil_entity(e1) and e2.type == 'ROCK':
						rs = get_rel(doc.docid, e1, e2, "FORMATION", "FORMATION-SINGLE-FORMATION-PER-DOC")
						print json.dumps(rs)


def main():
	'''
	@summary: Extract fossil candidates, each of which has a set of features
	'''

	#dump_input('/tmp/testinput')
	#return 0

	for sent in get_inputs():
		sents = []

		docid = sent["sentences.docid"]
		sentids = sent[".sentids"]
		words = sent[".words"]
		entities = sent[".entities"]
		
		doc = Document(docid, sentids, words, entities)

		extract1(doc)
		
main()

