#! /usr/bin/env python

from helper.easierlife import *

import re

from ext.Util import *
from ext.doc.Entity import *

import string


class FossilEntityExtractor(object):

	dict_fossils = None
	dict_species_lastword = None
	
	dict_english = None
	dict_locations = None
	
	def __init__(self):
		self.dict_fossils = {}
		self.dict_species_lastword = {}
		self.dict_english = {}

	def loadDict(self, docdir):

		import os
		words = {}
		pprev = ""
		prev = ""
		for folder in os.listdir(docdir):

			if not os.path.isdir(docdir + '/' +  folder):
				continue
			"""
			try:
				for l in open(docdir + '/' +  folder + '/input.text'):
					ss = l.rstrip().split('\t')
					if len(ss) > 2:
						words[ss[1].lower()] = 1
						words[prev + " " + ss[1].lower()] = 1
						words[pprev+" " + prev + " "+ss[1].lower()] = 1
						pprev = prev
						prev = ss[1].lower()
			except:
				donothing = True
			"""
			
		log("LOADED DICT")

		for l in open(BASE_FOLDER + '/dicts/words'):
			self.dict_english[l.rstrip().lower()] = 1
	
		for l in open(BASE_FOLDER + '/dicts/paleodb_taxons.tsv'):
			try:
				(rawname, rank) = l.rstrip().split('\t')
				
				ss = rawname.split(' ')
				if len(ss) == 1:
					self.dict_fossils[ss[0].lower()] = rank
				elif len(ss) == 2:
					if '(' not in rawname:
						self.dict_fossils[rawname.lower()] = rank
					else:
						for s in ss:
							if '(' in s:
								s = s.replace('(', '').replace(')', '')
							if 'species' in rank and ' ' not in s: continue
							self.dict_fossils[s.lower()] = rank
				elif len(ss) == 3:
					if '(' not in rawname:
						self.dict_fossils[name.lower()] = rank
					elif '(' in ss[1] and '(' not in ss[2] and '(' not in ss[0]:
						self.dict_fossils[(ss[0]+" "+ss[2]).lower()] = rank
						self.dict_fossils[(ss[1].replace('(', '').replace(')', '')+" "+ss[2]).lower()] = rank

				if 'species' in rank and len(ss) > 1 and len(ss[-1]) > 2:
					self.dict_species_lastword[ss[-1].lower()] = 1
			
			except:
				continue


		self.dict_locations = {}
		progress = 0
		for _file in os.listdir(BASE_FOLDER + '/dicts'):
			if not _file.startswith('geonames'): continue
			for l in open(BASE_FOLDER + '/dicts/' + _file):
				if progress % 100000 == 0:
					log(progress)
					#break
				progress = progress + 1
				(id, ent, rank, names, parents) = l.rstrip('\n').split('\t')
				rank = int(rank)
				names = names.split(',')
				parents = parents.split(',')

				for name in names:
					#if name.lower() in words:
					self.dict_locations[name.lower()] = "1"

	def extract(self, doc):

		RE_CF_ATOZ = re.compile(' cf\. [A-Z]\.')
		RE_CF = re.compile(' cf\.')
		RE_SIC = re.compile(' ( sic ) ')

		RE_AFF1 = re.compile(r'\baff\b')
		RE_AFF2 = re.compile(r'\baff\.\b')
		RE_INC1 = re.compile(r'\bincertae\b')
		RE_INC2 = re.compile(r'\bindet\b')

		RE_START_ATOZ = re.compile(r'^[A-Z]')
		RE_START_ATOZSTAR_END = re.compile(r'^[A-Z]*$')


		ranks = {"subgenus":3,"genus":4,"subtribe":5,"tribe":6,"subfamily":7,"family":8,"group":9,"superfamily":10,"infraorder":11,"suborder":12,"order":13,"superorder":14,"infraclass":15,"subclass":16,"class":17,"superclass":18,"subphylum":19,"phylum":20,"superphylum":21,"subkingdom":22,"kingdom":23,"superkingdom":24}
		
		MAXPHRASELEN = 7

		obvious_fossil_name = {}
		candiate_new_fossil_name = {}
		
		started = False
		ended = False
		for sent in doc.sents:

			started = True

			history = {}
			for start in range(0, len(sent.words)):
				for end in reversed(range(start + 1, min(len(sent.words)+1, start + 1 + MAXPHRASELEN))):
					
					if start in history or end in history: continue
					#print myjoin(" ", sent.words[start:end], lambda (w) : w.word)

					if end<len(sent.words):
						n_word = sent.words[end]
						if n_word.word.lower().endswith('zone'):
							continue
					if end<len(sent.words)-1:
						n_word = sent.words[end+1]
						if n_word.word.lower().endswith('zone'):
							continue

					ner = myjoin(" ", sent.words[start:end], lambda (w) : w.ner)
					font = myjoin(" ", sent.words[start:end], lambda (w) : w.font).replace('  ', '')
	
					nc = 0
					for phrase in my_par_join(" ", sent.words[start:end]):

						nc = nc + 1

						if 'cf.' in phrase or 'sic' in phrase:

							phrase2 = re.sub(RE_CF_ATOZ, '', phrase)
		   					phrase = phrase2

			 		   		phrase2 = re.sub(RE_CF, '', phrase)
				 			phrase = phrase2

							phrase2 = re.sub(RE_SIC, '', phrase)
							phrase = phrase2

						lphrase = phrase.lower()

						if 'aff' in lphrase or 'incertae' in lphrase or 'indet' in lphrase:
							if re.search(RE_AFF1, lphrase):
		   						continue
							if re.search(RE_AFF2, lphrase):
								continue
							if re.search(RE_INC1, lphrase):
								continue
							if re.search(RE_INC2, lphrase):
								continue

						prerank = None
						for prew in range(max(0, start-1), start):
							if sent.words[prew].word.lower() in ranks:
								prerank = sent.words[prew].word.lower()
  
						ss = phrase.split(' ')
						lss = len(ss)
						
						isvalid = True
						if not re.search(RE_START_ATOZ, ss[0]): isvalid = False
						
						for i in range(1, lss):
							if re.search(RE_START_ATOZ, ss[i]) and not re.search(RE_START_ATOZSTAR_END, ss[i]):
								isvalid = False

						inpar = False
						for i in range(1, lss):
							if '(' in ss[i]:
								inpar = True
								continue
							if ')' in ss[i]:
								inpar = False
								continue
							if inpar == False and re.search(RE_START_ATOZ, ss[i]) and not re.search(RE_START_ATOZSTAR_END, ss[i]):
								isvalid = False
						if isvalid == False: continue

						if inpar == True: continue
						if len(phrase) < 5: continue
						
						if prerank == None and prerank == None and lphrase in self.dict_locations: continue
					
						if lphrase in self.dict_fossils:
						
							obvious_fossil_name[lphrase] = self.dict_fossils[lphrase]
							if prerank != None:
								entity = Entity(prerank + "!", lphrase, sent.words[start:end])
							else:
								entity = Entity(self.dict_fossils[lphrase], lphrase, sent.words[start:end])
							doc.push_entity(entity)

						elif ' ' not in lphrase and lphrase.endswith('idae') and phrase.lower not in self.dict_english:
							
			 				if prerank != None:
								obvious_fossil_name[lphrase] = prerank
								entity = Entity(prerank + "!", lphrase, sent.words[start:end])
							else:
								obvious_fossil_name[lphrase] = "family"
								entity = Entity("family" ,lphrase, sent.words[start:end])
								doc.push_entity(entity)
						else:
												
							ss = phrase.split(' ')
							ssl = lphrase.split(' ')
						
							if len(ss) == 2:

								if ssl[0] in self.dict_fossils and 'genus' in self.dict_fossils[ssl[0]]:
									if ssl[1] in self.dict_species_lastword and ssl[1] not in self.dict_english:
									
										obvious_fossil_name[lphrase] = "species"
										entity = Entity("species", lphrase, sent.words[start:end])
										doc.push_entity(entity)
									else:
										if  ("SPECFONTSPECFONT" in font or "SPECFONT SPECFONT" in font) and len(ss[1]) > 3 and ssl[1] == ss[1]:
											if len(ss[0]) > 2 and ssl[1] not in self.dict_english:
												obvious_fossil_name[lphrase] = "species"
												entity = Entity("species", lphrase, sent.words[start:end])
												doc.push_entity(entity)
											
								elif ssl[1] == ss[1] and (ssl[1] in self.dict_species_lastword or (ssl[1] not in self.dict_english and re.search('^[a-z]*$', ss[1]))):
									if ("SPECFONTSPECFONT" in font or "SPECFONT SPECFONT" in font):
										if len(ss[0]) > 2 and ss[1].lower() not in self.dict_english:
											obvious_fossil_name[lphrase] = "species"
											entity = Entity("species",   lphrase, sent.words[start:end])
											doc.push_entity(entity)
											obvious_fossil_name[ss[0].lower()] = "genus"
											entity = Entity("genus", ss[0].lower(), sent.words[start:end-1])
											doc.push_entity(entity)
						
								cleanup = []
								inpars = []
								inpar = False
								for s in ssl:
									if '(' in s:
										inpar = True
										continue
									if ')' in s:
										inpar = False
										continue
									if inpar == False:
										cleanup.append(s)
									else:
										inpars.append(s)

								if len(inpars) == 1 and inpars[0] in self.dict_fossils and 'genus' in self.dict_fossils[inpars[0]]:
									if nc == 1:
										if len(cleanup) == 1 and ss[0] != '(':
											if cleanup[0] in self.dict_fossils and 'genus' in self.dict_fossils[cleanup[0]]:
												obvious_fossil_name[" ".join(ssl)] = "subgenus!"
												entity = Entity("subgenus!", " ".join(ssl), sent.words[start:end])
												doc.push_entity(entity)
									
									if nc == 1 and len(cleanup) == 2:
										if cleanup[0] in self.dict_fossils and 'genus' in self.dict_fossils[cleanup[0]]:
											if cleanup[1] in self.dict_species_lastword and cleanup[1] not in self.dict_english:

												obvious_fossil_name[" ".join(ssl)] = "species"
												entity = Entity("species", " ".join(ssl), sent.words[start:end])
												doc.push_entity(entity)

												obvious_fossil_name[cleanup[0]] = "genus"
												entity = Entity("genus", cleanup[0], sent.words[start:end-1])
												doc.push_entity(entity)
								

		possible_shortphrase = {}
		for name in obvious_fossil_name:
			ss = name.split(' ')
			if len(ss) == 2:
				shortphrase = ss[0][0] + '. ' + ss[1]
				if shortphrase not in possible_shortphrase: possible_shortphrase[shortphrase] = {}
				possible_shortphrase[shortphrase][name] = obvious_fossil_name[name]

		last_genus = ""
		started = False
		ended = False
		for sent in doc.sents:

			if ('introduction' in sent.__repr__().lower() or 'abstract' in sent.__repr__().lower()) and (len(sent.words) < 5 or (sent.words[0].word.lower() == 'abstract' and sent.words[0].box.left < 200)):
				started = True

			if ('keywords :' in sent.__repr__().lower()):
				started = True

			if ('reference' in sent.__repr__() or 'literature cited' in sent.__repr__()) and len(sent.words) < 20:
				ended = True

			if started== False or ended == True:
				continue

			history = {}
			for start in range(0, len(sent.words)):
				for end in reversed(range(start + 1, min(len(sent.words), start + 1 + MAXPHRASELEN))):
					if start in history or end in history: continue
					if end<len(sent.words)-1:
						n_word = sent.words[end+1]
						if n_word.word.lower().endswith('zone'):
							continue
					
					phrase = myjoin(" ", sent.words[start:end], lambda (w) : w.word)
					ner = myjoin(" ", sent.words[start:end], lambda (w) : w.ner)
					font = myjoin(" ", sent.words[start:end], lambda (w) : w.font).replace('  ', '')

					ss = phrase.split(' ')
					isvalid = True
					if not re.search('^[A-Z]', ss[0]): isvalid = False
					for i in range(1, len(ss)):
						if re.search('^[A-Z]', ss[i]) and not re.search('^[A-Z]*$', ss[i]):
							isvalid = False
					if isvalid == False: continue

					if phrase.lower() in self.dict_fossils:
						if 'genus' in self.dict_fossils[phrase.lower()]:
							last_genus = phrase.lower()
				
					if sent.words[start].word.endswith('.') and len(sent.words[start].word) == 2:
						if phrase.lower() in possible_shortphrase:
														
							for longphrase in possible_shortphrase[phrase.lower()]:
								
								entity = Entity(obvious_fossil_name[longphrase], longphrase, sent.words[start:end])
								doc.push_entity(entity)
						else:
							if len(ss) == 2 and last_genus.startswith(sent.words[start].word[0].lower()):
								testname = (last_genus + ' ' + myjoin(" ", sent.words[(start+1):end], lambda (w) : w.word)).lower()
								if testname in self.dict_fossils: 
									
									entity = Entity(self.dict_fossils[testname], testname.lower(), sent.words[start:end])
									doc.push_entity(entity)


		def format(e, seq, year):

			ss = seq.lower().split(' ')
			ss2 = []
			for w in ss:
				if w == '(' or len(w) == 0: continue
				if w.endswith('.') and len(w) == 2: continue
				ss2.append(w)
			if len(ss2) == 1 or (len(ss2) == 3 and 'and' in ss2) and int(year) > 1600:
				doc.ent_author_map[e.entity] = {"author":" ".join(ss2), "year": year}
				   
		for sentid in doc.entities:

			nspec = 0
			ngenus = 0
			history = {}
			for e in doc.entities[sentid]:
				if 'species' in e.type and e.entity not in history:
					nspec = nspec + 1
				if 'genus' in e.type and e.entity not in history:
					ngenus = ngenus + 1
				history[e.entity] = 1

			for e in doc.entities[sentid]:

				sent = doc.sents[sentid]
				for k in ['nomen dubium', 'nomen nudum', 'nomen oblitum', 'nomen vanum']:
					if k in sent.__repr__():
						if 'species' in e.type and nspec == 1:
							e.spectype = k
						elif 'genus' in e.type and nspec == 0 and ngenus == 1:
							e.spectype = k
						#else:
						#	import pdb
						#	pdb.set_trace()
				
				if 'INTERVAL' not in e.type and 'ROCK' not in e.type and 'LOCATION' not in e.type:
					words = []
					year = None
					if len(e.words) > 0:
						for wid in range(e.words[-1].insent_id+1, len(doc.sents[sentid].words)):
							word = doc.sents[sentid].words[wid].word
							if re.search('^[0-9][0-9][0-9][0-9]$', word):
								year = word
								break
							if 'new species' in " ".join(word):
								break
							words.append(word)

						if 'new species' in " ".join(words):
							if e.type == 'species':
								seq = " ".join(words)
								index = string.find('new species', " ".join(words))
								if index >= 0 and index < 10:
									format(e, "NEWSPEC-REF" + doc.docid, "0000")

						if year != None and len(words) > 0:

							if e.type == 'species':
								seq = " ".join(words)
								ss = seq.split(',')
								if len(ss) == 1:
									format(e, ss[0], year)
								if len(ss) == 2 and len(ss[1]) == 0 and len(ss[0]) != 0 :
									format(e, ss[0], year)

							if e.type != 'species':
								if words[0] == ',': words.pop(0)
								if len(words) == 0: continue

								if re.search('^[a-z]*$',words[0]) or not (re.search('^[A-Z][a-z][a-z].*$',words[0]) or (re.search('^[A-Z]\.$',words[0]))):
									continue
								else:
									seq = " ".join(words)
									ss = seq.split(',')
									if len(ss) == 1:
										format(e, ss[0], year)
									if len(ss) == 2 and len(ss[1]) == 0 and len(ss[0]) != 0 :
										format(e, ss[0], year)




