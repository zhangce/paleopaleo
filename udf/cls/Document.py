
from helper.easierlife import *

class Document:

	docid = None
	
	sents = None
	entities = None

	def __init__(self, docid, sentids, words, entities):
		self.docid = docid
		self.sents = {}
		self.entities = {}

		for i in range(0, len(sentids)):
			sent = Sentence()
			sent.sentid = sentids[i]
			sent.words = deserialize(words[i])
			self.sents[sentids[i]] = sent

		for i in range(0, len(entities)):
			ent = deserialize(entities[i])
			if ent.sentid not in self.entities:
				self.entities[ent.sentid] = []
			self.entities[ent.sentid].append(ent)