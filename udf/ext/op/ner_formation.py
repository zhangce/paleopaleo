#! /usr/bin/env python

from helper.easierlife import *

import re

from ext.Util import *
from ext.doc.Entity import *

class FormationEntityExtractor:
		 
	dict_intervals = None
	stop_words = None
    
	BADFORMATIONNAME = {
        "lower":1,
        "upper":1,
        "middle":1
    }
    
	def __init__(self):
		self.dict_intervals = {}
		self.stop_words = []
    
	def loadDict(self):
		donothing = None
		dicts = {}
		for l in open(BASE_FOLDER + '/dicts/intervals.tsv', 'r'):
			(begin, end, name) = l.rstrip().split('\t')
			dicts[name.lower()] = name + '|' + begin + '|' + end
			va = name.lower().replace('late ', 'upper ').replace('early ', 'lower')
			if va != name.lower():
				dicts[va] = name + '|' + begin + '|' + end
        
		self.dict_intervals = dicts
		for l in open(BASE_FOLDER + '/dicts/english.stop', 'r'):
			self.stop_words.append(l.strip())

                
	def extract(self, doc):
		MAXPHRASELEN = 5
		rocktypes = {"formation":1, "group":1, "member":1, "shale":1, "slate":1, "marble":1, "formations":1, "groups":1, "members":1, "shales":1, "facies":1, "slates":1, "marbles":1, "limestone":1, 'tuff':1, 'beds':1, 'bed':1, "face":1}
		good_names = {}
		for sent in doc.sents:
			history = {}
			for start in range(0, len(sent.words)):
				for end in reversed(range(start + 1, min(len(sent.words), start + 1 + MAXPHRASELEN))):
						if start in history or end in history: continue
						phrase = myjoin(" ", sent.words[start:end], lambda (w) : w.word)
						ner = myjoin(" ", sent.words[start:end], lambda (w) : w.ner)
						lemma = myjoin(" ", sent.words[start:end], lambda (w) : w.lemma)
						lemma = lemma.replace('Sandstones', 'Sandstone')
						isvalid = True
						for r in rocktypes:
							if phrase.lower().startswith(r):
										isvalid = False
						if isvalid == False:
											continue
       
						if (re.search('^([A-Z][a-zA-Z][a-zA-Z]+\s*|de\s*)*$', phrase) and start>0) or re.search('^([A-Z][a-zA-Z][a-zA-Z][a-zA-Z]+\s*|de\s*)*$', phrase) or re.search('^[A-Z][a-z] ([A-Z][a-zA-Z][a-zA-Z][a-zA-Z]+\s*)*$', phrase):
												word ='' 
												if ' ' in phrase:
													word = phrase.lower()[:phrase.index(' ')]
												else:
													word = phrase.lower()
												if len(word.strip())<=4 and word.lower() in self.stop_words:continue
												#print word	
												for lastword in rocktypes:
														if phrase.lower().endswith(' ' + lastword) and phrase.lower() != lastword:
																contains = False
																for interval in self.dict_intervals:
																	if interval.lower() in phrase.lower():
																		contains = True
																for badname in self.BADFORMATIONNAME:
																		if badname + " " in phrase.lower():
																			contains = True
          
																if contains == False:
																	good_names[phrase.lower()] = phrase.lower()
																	good_names[phrase[0:phrase.rindex(' ')].lower()] = phrase.lower()
																	name = phrase.lower()
																	#print phrase[0:phrase.rindex(' ')]
																	if phrase.lower().endswith('bed') or phrase.lower().endswith('beds') or phrase.lower().endswith('tuff') or (phrase.lower() + " " + lastword).lower().endswith('limestone'):
																		name = name + ' ' + 'formation'
																	if not (lemma.lower().endswith(' facies') or lemma.lower().endswith(' face')): 
																		entity = Entity("ROCK", lemma.lower(), sent.words[start:end])
																		doc.push_entity(entity)
																		#print str(entity.sentid) + " : " + "FORMATION : " + entity.entity
																	for i in range(start, end): history[i] = 1
		for sent in doc.sents:
			history = {}
			for start in range(0, len(sent.words)):
				for end in reversed(range(start + 1, min(len(sent.words), start + 1 + MAXPHRASELEN))):
					if start in history or end in history: continue
					phrase = myjoin(" ", sent.words[start:end], lambda (w) : w.word)
					ner = myjoin(" ", sent.words[start:end], lambda (w) : w.ner)
					lemma = myjoin(" ", sent.words[start:end], lambda (w) : w.lemma)

					lemma = lemma.replace('Sandstones', 'Sandstone')
					isvalid = True
					for r in rocktypes:
						if phrase.lower().startswith(r):
							isvalid = False
					if isvalid == False:continue   
					if re.search('^([A-Z][a-zA-Z][a-zA-Z][a-zA-Z]+\s*|de\s*)*$', phrase):
						exted = False
						for lastword in rocktypes:
							if phrase.lower().endswith(" " + lastword) and phrase.lower() != lastword:
								contains = False
								for interval in self.dict_intervals:
									if interval.lower() in phrase.lower():
										contains = True
								for badname in self.BADFORMATIONNAME:
									if badname + " " in phrase.lower():
										contains = True

								if contains == False:
									exted = True
		for sent in doc.sents:
			for start in range(0, len(sent.words)):
				for end in reversed(range(start + 1, min(len(sent.words), start + 1 + MAXPHRASELEN))):
					phrase = myjoin(" ", sent.words[start:end], lambda (w) : w.word)
					lemma = myjoin(" ", sent.words[start:end], lambda (w) : w.lemma)
					lemma = lemma.replace('Sandstones', 'Sandstone')
					if phrase.lower() in good_names:
						c= True
						if sent.sentid in doc.entities:	
							for ent in doc.entities[sent.sentid]:
								if ent.phrase.strip().lower()==phrase.strip().lower() or phrase.strip().lower() in ent.phrase.strip().lower():
									c = False
						if c:
							entity = Entity("ROCK", good_names[phrase.lower()], sent.words[start:end], good_names[phrase.lower()])
							doc.push_entity(entity)

