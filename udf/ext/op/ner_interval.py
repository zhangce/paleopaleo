#! /usr/bin/env python

from helper.easierlife import *

import re

from ext.Util import *
from ext.doc.Entity import *

class IntervalEntityExtractor:

		dict_intervals = None
		
		def __init__(self):
				self.dict_intervals = {}
		
		def loadDict(self):
		
				dicts = {}
				for l in open(BASE_FOLDER + '/dicts/intervals.tsv', 'r'):
						(begin, end, name) = l.rstrip().split('\t')
						dicts[name.lower()] = name + '|' + begin + '|' + end
				
						va = name.lower().replace('late ', 'upper ').replace('early ', 'lower')
						if va != name.lower():
								dicts[va] = name + '|' + begin + '|' + end
		
				self.dict_intervals = dicts
								
		def extract(self, doc):
				
				MAXPHRASELEN = 3

				obvious_fossil_name = {}

				title = doc.title.replace(',', ' ')
				title = title.replace('(', ' ')
				title = title.replace(')', ' ')
				title = re.sub('\s+', ' ', title)
				titlewords = title.lower().split(' ')
				
				log(titlewords)

				history = {}
				for start in range(0, len(titlewords)):
						for end in reversed(range(start + 1, min(len(titlewords)+1, start + 1 + MAXPHRASELEN))):
								phrase = " ".join(titlewords[start:end])

								if start in history: continue

								if phrase.lower() in self.dict_intervals:
										doc.titleentities.append(Entity("INTERVAL", self.dict_intervals[phrase.lower()], []))
										#log("INTERVAL : "+ phrase.lower())
										for i in range(start, end):
												history[i] = 1
				
				for sent in doc.sents:
						history = {}
						for start in range(0, len(sent.words)):
								for end in reversed(range(start + 1, min(len(sent.words), start + 1 + MAXPHRASELEN))):
												
										if start in history or end in history: continue
												
										phrase = myjoin(" ", sent.words[start:end], lambda (w) : w.word)
										ner = myjoin(" ", sent.words[start:end], lambda (w) : w.ner)
												
										if phrase.lower() in self.dict_intervals:
												entity = Entity("INTERVAL", self.dict_intervals[phrase.lower()], sent.words[start:end])
												doc.push_entity(entity)
												for i in range(start, end):
													history[i]=1
												#log(str(entity.sentid) + " : " + "INTERVAL : " + entity.entity)
										if '-' in phrase:
												for part in phrase.split('-'):
														if part.lower() in self.dict_intervals:
																entity = Entity("INTERVAL", self.dict_intervals[part.lower()], sent.words[start:end])
																doc.push_entity(entity)
																for i in range(start, end):
																	history[i]=1
	






