#! /usr/bin/env python

from helper.easierlife import *

from ext.Util import *

from ext.doc.Sentence import *
from ext.doc.Word import *
from ext.doc.Box import *
import ext.Util as Util
import math

import copy

import re

RE_CLEAN_OCR1 = re.compile('[a-zA-Z]*(0+)[a-zA-Z]')
RE_CLEAN_OCR2 = re.compile('[a-zA-Z]*(1+)[a-zA-Z]')
RE_CLEAN_OCR3 = re.compile('^([0-9]*)([A-Z])')
RE_NOT_A_TO_Z = re.compile('^[A-Z]')

def clean_ocr(word):

    a = word
        
    for m in re.finditer(RE_CLEAN_OCR1, word):
        a = a.replace(m.group(1), 'o'*len(m.group(1)))
    for m in re.finditer(RE_CLEAN_OCR2, word):
        a = a.replace(m.group(1), 'I'*len(m.group(1)))
    for m in re.finditer(RE_CLEAN_OCR3, word):
        a = a.replace(m.group(1)+m.group(2), m.group(2))
    
    a = a.replace('lndia', 'India')
    a = a.replace('Tulf', 'Tuff')
    a = a.replace('Kahuilaru', 'Kahuitara')
    a = a.replace('?l', 'fil')
    a = a.replace('NTTE', 'NITE')
    a = a.replace('I-I', 'H')
    a = a.replace('i?i', 'ifi') 
    
    return a


class Document:
    docid = None

    sents = None
    
    tables = None

    entities = None

    relations = None
    
    titleentities = None
    
    title = None
    
    _tmp_sent = None
    
    ent_author_map = None

    fonts = None

    fontshash = None

    def __init__(self, _docid):
        self.docid = _docid
        self.sents = []
        self.sents.append(Sentence())
    
        self.entities = {}
        self.relations = []
        
        self.titleentities = []
    
        self.tables = []
        
        self.ent_author_map = {}
    
        self.title = ""

        self.fonts = {}
        self.fontshash = {}

    
    def parse_doc(self, filepath):

        try:
             for l in open(filepath + "/fonts.text"):
                (type, page, l, t, r, b, content) = l.rstrip('\n').split('\t')
                box = Box("p%sl%st%sr%sb%s"%(page, l, t, r, b))
                page = int(page)
                if page not in self.fonts: self.fonts[page] = []
                self.fonts[page].append({"type":type, "box":box, "content":content})
                self.fontshash[box.__repr__()] = {"type":type, "box":box, "content":content}
        except:
            donothing = True
        		
        ranks = {"subspecies":1,"species":2,"subgenus":3,"genus":4,"subtribe":5,"tribe":6,"subfamily":7,"family":8,"group":9,"superfamily":10,"infraorder":11,"suborder":12,"order":13,"superorder":14,"infraclass":15,"subclass":16,"class":17,"superclass":18,"subphylum":19,"phylum":20,"superphylum":21,"subkingdom":22,"kingdom":23,"superkingdom":24}
        for r in ranks.keys():
            ranks[r+"!"] = ranks[r]
        
        lastbox = None

        newsentidct = 1
        
        lastsentid = None
                
        reallastbox = None
        
        insentid_ct = 0
        
        try:
            for l in open(filepath + "/title.text"):
                self.title = l.rstrip()
        except:
            self.title = ""

        try:
            for l in open(filepath + "/input.text"):
                ss = l.rstrip().split('\t')
                if len(ss) < 3: continue
                (insent_id, word, pos, ner, lemma, deppath, deppar, sentid, box) = ss
                
                box = Box(box)
                word = clean_ocr(word)
                lemma = clean_ocr(lemma)
            
                if lastsentid == None:
                    insentid_ct = 0
                    lastbox = box
                    reallastbox = box
                    lastsentid = sentid
                    newsentid = "SENT_%d" % newsentidct
                else:
                    if lastsentid != sentid:
                        insentid_ct = 0
                        lastbox = box
                        reallastbox = box
                        lastsentid = sentid
                        newsentidct = newsentidct + 1
                        newsentid = "SENT_%d" % newsentidct
                    else:
                        if box.left > lastbox.left and box.top > lastbox.bottom and box.top > reallastbox.bottom and re.search(RE_NOT_A_TO_Z, word) and word.lower() in ranks:
                            #print sentid, word, box.top, lastbox.bottom
                            lastbox = box
                            reallastbox = box
                            lastsentid = sentid
                            newsentidct = newsentidct + 1
                            insentid_ct = 0
                            newsentid = "SENT_%d" % newsentidct
                        else:
                            reallastbox = box
                            lastsentid = sentid
                            newsentid = "SENT_%d" % newsentidct

                insentid_ct = insentid_ct + 1
        
                self.push_word(Word("%d"%insentid_ct, word, pos, ner, lemma, deppath, deppar, newsentid, box))
        except:
            donothing = False

    def push_word(self, word):

        font = ""
        centered = False
        followed = False
        left_margin = 1000000
        altword = None

        if word.box.page in self.fonts:

            for b2 in self.fonts[word.box.page]:
                if word.box.overlap(b2["box"]) == True:

                    if b2["type"] == "SPECFONT":
                        font = "SPECFONT"
                    if b2["type"] == 'CENTERED':
                        centered = True
                    if b2["type"] == 'FOLLOWED':
                        followed = True
                    if b2["type"] == "CENTERED" or b2["type"] == "FOLLOWED":
                        left_margin = min(left_margin, math.fabs(b2["box"].left - word.box.left))
                    if b2["type"] == "JUSTWORD":
                        altword = b2["content"]

        word.font = font 
        word.centered = centered
        word.followed = followed
        word.left_margin = left_margin
        word.altword = altword

        if self.sents[-1].push_word(word) == False:
            self.sents.append(Sentence())
            self.sents[-1].push_word(word)
        if word.sentid not in self.entities:
            self.entities[word.sentid] = []
    
    def push_entity(self, entity):
                
        self.entities[entity.sentid].append(entity)
        for w in entity.words:
            w.ner = "#" + entity.type + "#"

    def push_relation(self, relation):
        self.relations.append(relation)
    
    def push_table(self, table):
        self.tables.append(table)

    def get_sentrepr(self, sentid):
        return self.sents[sentid].__repr__()

    def cleanup_entities(self):
        for sentid in self.entities:
            
            toremove = []
            for e1 in self.entities[sentid]:
                for e2 in self.entities[sentid]:
                    if e1 == e2: continue
                    if e1.type == e2.type: continue
                    if e1.words == e2.words:
                        if e1.type != 'LOCATION' and e1.type != 'INTERVAL' and e1.type != 'ROCK':
                            toremove.append(e1)
                    if e1.phrase in e2.phrase:
                        if e1.type == 'LOCATION' and e2.type == 'ROCK':
                            toremove.append(e1)
                        if e2.phrase not in e1.phrase and e1.type in ['genus', 'subgenus', 'subgenus!'] and e2.type.startswith('subgen'):
                            toremove.append(e1)
        
            newlist = []
            for e in self.entities[sentid]:
                if e in toremove: continue
                newlist.append(e)
            self.entities[sentid] = newlist

    def assign_ids(self):

        eid_ct = 0
        for sentid in self.entities:
            for e in self.entities[sentid]:
                eid_ct = eid_ct + 1
                eid = "DOC_" + self.docid + "_ENT_%d" % eid_ct
                e.eid = eid

                if 'INTERVAL' not in e.type and 'ROCK' not in e.type and 'LOCATION' not in e.type:
                    if e.entity in self.ent_author_map:
                        e.author_year = self.ent_author_map[e.entity]["author"] + "\t" + self.ent_author_map[e.entity]["year"]

        rid_ct = 0
        for rel in self.relations:
            rid_ct = rid_ct + 1
            rid = "DOC_" + self.docid + "_REL_%d" % rid_ct
            rel.rid = rid


    def get_entities_candidates(self, fo):

        for sentid in self.entities:
            for e in self.entities[sentid]:
                fo.write(json.dumps({"docid":self.docid, "type":e.type, "eid":e.eid, "entity":e.entity, "features":""}))
                fo.write('\n')
                    
    def get_relation_candidates(self, superviser, fo):
    
        for rel in self.relations:
    
            ans = superviser.teach_me(self.docid, rel.type, rel.entity1, rel.entity2)
    
            fo.write(json.dumps({"is_correct":ans,"docid":self.docid, "type":rel.type, "eid1":rel.entity1.eid, "eid2":rel.entity2.eid, "entity1":rel.entity1.entity.decode('ascii', 'ignore'), "entity2":rel.entity2.entity.decode('ascii', 'ignore'), "features":rel.type + "-" + rel.prov}))
            fo.write('\n')







