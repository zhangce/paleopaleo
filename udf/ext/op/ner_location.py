#! /usr/bin/env python

from helper.easierlife import *

import re

from ext.Util import *
from ext.doc.Entity import *

import math


class LocationEntityExtractor:

    locs = None
    pars = None
    ranks = None
    id2ents = None
    id2pop = None
    
    BADLOCATIONNAME = {
        "north":1,
        "south":1,
	    "east":1,
        "west":1,
        "north":1,
        "central":1,
        "hill":1,
        "hills":1,
        "lake":1,
        "mount":1,
        "springs":1,
        "white":1,
        "basin":1,
        "pushkin":1,
        "lima":1,
        "island":1,
        "ocean":1,
        "southwest":1,
        "southeast":1,
        "northwest":1,
        "northeast":1,
        "valley":1,
        "academia":1,
        "national":1,
        "museum":1,
        "cross":1,
        "united":1,
        "reservoir":1,
        "limestone":1,
        "creek":1,
				"middle":1        
    }
    
    def __init__(self):
        self.dict_context = {}
        self.dict_single = {}
    
    def loadDict(self, docdir):
    
        import os
        words = {}
        pprev = ""
        prev = ""
        for folder in os.listdir(docdir):
            
            import os.path
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


        locs = {}
        pars = {}
        ranks = {}
        id2ents = {}
        id2pop = {}
        progress = 0

        import zipfile
        import os

        for _file in os.listdir(BASE_FOLDER + '/dicts'):
            if not _file.startswith('geonames'): continue
            for l in open(BASE_FOLDER + '/dicts/' + _file):
                if progress % 100000 == 0:
                    log(progress)
                    #break
                progress = progress + 1
                (id, ent, rank, names, parents) = l.rstrip('\n').split('\t')
                rank = rank
                names = names.split(',')
                parents = parents.split(',')

                names.append(ent.split('|')[0])

                added = False
                for name in names:
                    name = name.lower()
                    #if not (name in words):
                    #    continue
                    #print name
                    if name not in locs: locs[name] = {}
                    locs[name][id] = "1"
                    added = True
                #id2pop[id] = len(names)
                    
                if added == True:
                    id2pop[id] = len(names)
                    for p in parents:
                        pars[id + "|" + p] = "1"

                    id2ents[id] = ent

                    ranks[id] = rank

        #print "DONE"
        
        self.locs = locs
        self.pars = pars
        self.ranks = ranks
        self.id2ents = id2ents
        self.id2pop = id2pop

    def extract(self, doc):
        
        MAXPHRASELEN = 3

        obvious_locs = {}
        candidates = {}

        started = False
        ended = False

        for sent in doc.sents:

            for start in range(0, len(sent.words)):
                for end in range(start + 1, min(len(sent.words) + 1, start + 1 + MAXPHRASELEN)):
                    phrase = myjoin(" ", sent.words[start:end], lambda (w) : w.word)
                    ner = myjoin(" ", sent.words[start:end], lambda (w) : w.ner)

                    if not re.search('^[A-Z]', phrase): continue
                    if not re.search('^(LOCATION\s*)+$', ner) and phrase.lower() not in ['iowa']: continue

                    nearest_number = -1
                    for i in range(end, len(sent.words)):
                        if re.search('^[0-9][0-9][0-9][0-9]$', sent.words[i].word):
                            nearest_number = i
                            break
                    if nearest_number != -1 and (nearest_number - end) < 8: continue
                    
                    nearest_number = -1
                    for i in range(end, len(sent.words)):
                        if re.search('^and$', sent.words[i].word.lower()):
                            nearest_number = i
                            break
                        if re.search('^et$', sent.words[i].word.lower()):
                            nearest_number = i
                            break
                    if nearest_number != -1 and (nearest_number - end) < 3: continue

                    if phrase.lower() in self.locs and phrase.lower() not in self.BADLOCATIONNAME:
                        if len(self.locs[phrase.lower()]) == 1:
                            obvious_locs[phrase.lower()] = {self.locs[phrase.lower()].keys()[0]:{1:1}}             
                        if phrase.lower() not in candidates:
                            candidates[phrase.lower()] = {}
                        candidates[phrase.lower()][sent.sentid] = [start, end]

        for phrase1 in candidates:
            for phrase2 in candidates:
                for s1 in candidates[phrase1]:
                    if s1 in candidates[phrase2]:
                        s2 = s1
                        if s1 == s2 :
                            dis = candidates[phrase2][s2][0] - candidates[phrase1][s1][1]

                            if dis >= 0 and dis <= 5:
                                for id1 in self.locs[phrase1]:
                                    for id2 in self.locs[phrase2]:
                                        if id1 + "|" + id2 in self.pars:
                                            if phrase1 not in obvious_locs: obvious_locs[phrase1] = {}
                                            if id1 not in obvious_locs[phrase1]: obvious_locs[phrase1][id1] = {}
                                            obvious_locs[phrase1][id1][2] = 1

        for phrase1 in candidates:
            if phrase1 not in obvious_locs:
                for id1 in self.locs[phrase1]:
                    if self.ranks[id1] == "1":
                        if phrase1 not in obvious_locs: obvious_locs[phrase1] = {}
                        if id1 not in obvious_locs[phrase1]: obvious_locs[phrase1][id1] = {}
                        obvious_locs[phrase1][id1][3] = 1

        for phrase1 in candidates:
            if phrase1 not in obvious_locs:
                for id1 in self.locs[phrase1]:
                    if self.ranks[id1] == "2":
                        if phrase1 not in obvious_locs: obvious_locs[phrase1] = {}
                        if id1 not in obvious_locs[phrase1]: obvious_locs[phrase1][id1] = {}
                        obvious_locs[phrase1][id1][4] = 1


        for phrase1 in candidates:
            for phrase2 in candidates:
                for s1 in candidates[phrase1]:
                    if s1 in candidates[phrase2]:
                        s2 = s1
                        if s1 == s2:
                            if math.fabs(s1 - s2) < 10000 :
                                for id1 in self.locs[phrase1]:
                                    for id2 in self.locs[phrase2]:
                                        if id1 + "|" + id2 in self.pars:
                                            if phrase1 not in obvious_locs: obvious_locs[phrase1] = {}
                                            if id1 not in obvious_locs[phrase1]: obvious_locs[phrase1][id1] = {}
                                            obvious_locs[phrase1][id1][6] = 1

                            if math.fabs(s1 - s2) < 5 :
                                for id1 in self.locs[phrase1]:
                                    for id2 in self.locs[phrase2]:
                                        if id1 + "|" + id2 in self.pars:
                                            if phrase1 not in obvious_locs: obvious_locs[phrase1] = {}
                                            if id1 not in obvious_locs[phrase1]: obvious_locs[phrase1][id1] = {}
                                            obvious_locs[phrase1][id1][5] = 1

        locmapping = {}
        for phrase in obvious_locs:
            mpid = -1
            maxpop = -1
            for id in obvious_locs[phrase]:
                ll = len(obvious_locs[phrase][id])
                if ll > maxpop:
                    maxpop = ll
                    mpid = id
            locmapping[phrase] = mpid

        for phrase in obvious_locs:

            if phrase in locmapping:
                continue

            mpid = -1
            maxpop = -1
            for id in obvious_locs[phrase]:
                if self.id2pop[id] > maxpop:
                    maxpop = self.id2pop[id]
                    mpid = id

            locmapping[phrase] = mpid

        title = doc.title.replace(',', ' ')
        title = re.sub('\s+', ' ', title)
        titlewords = title.lower().split(' ')
        
        log("~~~~~~~~~~" + titlewords.__repr__())

        history = {}
        for start in range(0, len(titlewords)):
            for end in reversed(range(start + 1, min(len(titlewords)+1, start + 1 + MAXPHRASELEN))):
                phrase = " ".join(titlewords[start:end])

                if start in history: continue

                if phrase.lower() in locmapping:
                    doc.titleentities.append(Entity("LOCATION", self.id2ents[locmapping[phrase.lower()]] , []))
                    for i in range(start, end):
                        history[i] = 1

        badnames = {}
        started = False
        ended = False
        for sent in doc.sents:
            for start in range(0, len(sent.words)):
                for end in reversed(range(start + 1, min(len(sent.words)+1, start + 1 + MAXPHRASELEN))):

                    if start in history: continue

                    phrase = myjoin(" ", sent.words[start:end], lambda (w) : w.word)
                    ner = myjoin(" ", sent.words[start:end], lambda (w) : w.ner)

                    if not re.search('^[A-Z]', phrase): continue
                    if not re.search('^(LOCATION\s*)+$', ner) and phrase.lower() not in ['iowa']: continue

                    if phrase.lower() in locmapping and 'river' not in phrase.lower():
                        nearest_number = -1
                        for i in range(end, len(sent.words)):
                            if re.search('^[0-9][0-9][0-9][0-9]$', sent.words[i].word):
                                nearest_number = i
                                break
                        if nearest_number != -1 and (nearest_number - end) < 3: badnames[phrase.lower()] = 1
                    
                        nearest_number = -1
                        for i in range(end, len(sent.words)):
                            if re.search('^et$', sent.words[i].word.lower()):
                                nearest_number = i
                                break
                        if nearest_number != -1 and (nearest_number - end) < 3: badnames[phrase.lower()] = 2

        log(badnames)

        started = False
        ended = False
        for sent in doc.sents:

            history = {}
            for start in range(0, len(sent.words)):
                for end in reversed(range(start + 1, min(len(sent.words)+1, start + 1 + MAXPHRASELEN))):

                    if start in history: continue

                    phrase = myjoin(" ", sent.words[start:end], lambda (w) : w.word)
                    ner = myjoin(" ", sent.words[start:end], lambda (w) : w.ner)

                    if not re.search('^[A-Z]', phrase): continue
                    if not re.search('^(LOCATION\s*)+$', ner) and phrase.lower() not in ['iowa']: continue

                    nearest_number = -1
                    for i in range(end, len(sent.words)):
                        if re.search('^[0-9][0-9][0-9][0-9]$', sent.words[i].word):
                            nearest_number = i
                            break
                    if nearest_number != -1 and (nearest_number - end) < 8: continue
                    
                    nearest_number = -1
                    for i in range(end, len(sent.words)):
                        if re.search('^et$', sent.words[i].word.lower()):
                            nearest_number = i
                            break
                    if nearest_number != -1 and (nearest_number - end) < 3: continue

                                            
                    if phrase.lower() in locmapping and phrase.lower() not in badnames:
                        log("LOCATION      " + phrase.lower() + "--->" + self.id2ents[locmapping[phrase.lower()]])
                        entity = Entity("LOCATION", self.id2ents[locmapping[phrase.lower()]], sent.words[start:end])
                        doc.push_entity(entity)
                        for i in range(start, end):
                            history[i] = 1


