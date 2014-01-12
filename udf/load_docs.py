#! /usr/bin/env pypy

import codecs

from helper.easierlife import *

from multiprocessing import *

INPUT_FOLDER = BASE_FOLDER + "/input"

from ext.doc.Document import *

from ext.op.tab_tablefromtext import *

from ext.op.ner_location import *
from ext.op.ner_fossil import *
from ext.op.ner_interval import *
from ext.op.ner_formation import *

from ext.op.rel_samesent import *
from ext.op.rel_title import *
from ext.op.rel_tablecaption import *
from ext.op.rel_jointformation import *
from ext.op.rel_sectionheader import *
from ext.op.rel_listext import *

from ext.op.superviser_occurrences import *


locationext = LocationEntityExtractor()
locationext.loadDict(INPUT_FOLDER)

fossilext = FossilEntityExtractor()
fossilext.loadDict(INPUT_FOLDER)

intervalext = IntervalEntityExtractor()
intervalext.loadDict()

formationext = FormationEntityExtractor()
formationext.loadDict()

samesentrel = SameSentRelationExtractor()
samesentrel.loadDict()

tableexttext = TableExtractorFromText()
tableexttext.loadDict()

tablecaprel = TableCaptionRelationExtractor()
tablecaprel.loadDict()

title_rel = TitleRelationExtractor()

sectionrel = SectionHeaderRealtionExtraction()
sectionrel.loadDict()

listrel = ListRelationExtraction()
listrel.loadDict()

jointrel = JointFormationRelationExtractor()
jointrel.loadDict()

superviser = OccurrencesSuperviser()
superviser.loadDict()


class Task:
	l = None
	docid = None

	def __init__(self):
		self.l = ""
		self.docid = ""

lock = Lock()

def initializer(*args):
	global lock
	lock = args[0]

def process(task):

	DOCID = task.docid

	global INPUT_FOLDER
	DOCDIR = INPUT_FOLDER

	doc = Document(DOCID)
	doc.parse_doc(DOCDIR + "/" + DOCID)

	global locationext
	global fossilext
	global intervalext
	global formationext
	global samesentrel
	global tableexttext
	global tablecaprel
	global jointrel
	global sectionrel

	global superviser

	try:

		locationext.extract(doc)

		fossilext.extract(doc)

		intervalext.extract(doc)

		formationext.extract(doc)

		doc.cleanup_entities()

		samesentrel.extract(doc)

		tableexttext.extract(doc)

		tablecaprel.extract(doc)

		sectionrel.extract(doc)

		listrel.extract(doc)

		jointrel.extract(doc)

		title_rel.extract(doc)

		doc.assign_ids()

		fo = codecs.open(BASE_FOLDER + "/tmp/" + DOCID + ".ent", 'w', 'utf-8')
		doc.get_entities_candidates(fo)
		fo.close()

		fo = codecs.open(BASE_FOLDER + "/tmp/" + DOCID + ".rel", 'w', 'utf-8')
		doc.get_relation_candidates(superviser, fo)
		fo.close()

	except:
		donothing = True

	#lock.acquire()
	#print json.dumps({"docid":DOCID, "document":serialize(doc)})
	#sys.stdout.flush()
	#lock.release()

	#return doc

log("START PROCESSING!")

def do():
	tasks = []
	#ct = 0
	for docid in os.listdir(INPUT_FOLDER):
		if docid.startswith('.'): continue

		#if '26937' not in docid: continue

		task = Task()
		task.docid = docid
		tasks.append(task)

		#if task.docid != "11173.2": continue
		#print task.docid
		#process(task)
		#print "done"

		#ct = ct + 1
		#if ct > 1:
		#	break

		#tasks.append(task)

	pool = Pool(8, initializer, (lock,))
	pool.map(process, tasks)

#import cProfile
#cProfile.run('do()')

do()

#for doc in pool.map(process, tasks):
#print json.dumps({"docid":doc.docid, "document":serialize(doc)})









