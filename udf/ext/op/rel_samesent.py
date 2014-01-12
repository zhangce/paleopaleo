#! /usr/bin/env python

from helper.easierlife import *

import re
from ext.doc.Relation import *
import math
import random

class SameSentRelationExtractor:
    
    def __init__(self):
        donothing = None
    
    def loadDict(self):
        donothing = None
    
    def extract(self, doc):
        
        flist = ['INV:PERSON_,_DATE_RANK', 'new_RANK_and_assign_to', ',_we_amend_the_RANK_name_into', 'INV:PERSON_,_DATE', 'INV:,_include_TAXON_in_the', 'INV:,_include', 'PERSON_,_DATE_be_transfer_into','OVERLAP', 'to_the'
                 ]
    
        features = {'INV:PERSON_,_DATE_RANK':1, 'INV:' : 1, '(':1, 'INV::' : 1, 'INV:(' : 1, 'within_the' : 1, 'INV:PERSON_,_DATE_RANK_:' : 1, 'INV:PERSON_,_DATE': 1, 'PERSON_and_PERSON_,_DATE_RANK' : 1, 'INV:,_TAXON_,' : 1, 'and_TAXON_in_the_RANK' : 1, 'in_the_RANK' : 1, 'of' : 1, 'of_the' : 1, 'INV:,_RANK' : 1, 'of_the_RANK' : 1, 'INV::_TAXON_,' : 1, 'INV:PERSON_PERSON_,_DATE_RANK' : 1, 'be_place_in_the' : 1, 'have_be_consider_to_be_a_member_of_the': 1, 'within_the_RANK' : 1, 'PERSON_,_DATE_,_in' : 1, 'as_a_RANK_of' : 1, 'DATE_,_RANK' : 1, 'INV:belong_to_the' : 1, 'INV:PERSON_PERSON_,_DATE_RANK_:' : 1, 'INV:be_divide_into_two_RANK_:' : 1}
    
        for fff in flist: features[fff] = 1
    
        features_pattern = ['INV:[A-Z]._and_(PERSON_)*,_DATE_RANK$', 'INV:[A-Z][a-zA-Z]*_,_DATE_RANK$', 'we_attribute_.*?_to_the$']
    
        ranks = {"subspecies":1,"species":2,"subgenus":3,"genus":4,"subtribe":5,"tribe":6,"subfamily":7,"family":8,"group":9,"superfamily":10,"infraorder":11,"suborder":12,"order":13,"superorder":14,"infraclass":15,"subclass":16,"class":17,"superclass":18,"subphylum":19,"phylum":20,"superphylum":21,"subkingdom":22,"kingdom":23,"superkingdom":24}
        for r in ranks.keys():
            ranks[r+"!"] = ranks[r]
        
        started = False
        ended = False
        
        QUOTE = 100
        for sent in doc.entities:
            rels ={}
            rels['FORMATIONLOCATION']={}
            rels['FORMATION']={}
            sss = doc.sents[sent]

            history = {}
            for e1 in doc.entities[sent]:
                for e2 in doc.entities[sent]:

                    if e1.overlap(e2):
                        if 'species' in e1.type and 'genus' in e2.type and e1.entity.lower().startswith(e2.entity.lower()):
                            doc.push_relation(Relation("TAXONOMY", e1, e2, "[TRIVIAL]"))
                        
                        continue

                    ws = doc.sents[sent].wordseq_feature(e1, e2)

                    ws_dep = doc.sents[sent].dep_path(e1, e2)

                    #if QUOTE > 0 and random.random() < 0.1:
                    #
                    #    QUOTE = QUOTE - 1
                    #
                    #    doc.push_relation(Relation("FORMATION", e1, e2, "[SAMESENT PROV=" + ws + "] "))
                    #    doc.push_relation(Relation("FORMATION", e1, e2, "[SAMESENT PROV=" + ws_dep + "] "))
                    #                    
                    #    doc.push_relation(Relation("FORMATIONTEMPORAL", e1, e2, "-[SAMESENT PROV=" + ws + "] "))
                    #    doc.push_relation(Relation("FORMATIONTEMPORAL", e1, e2, "-[SAMESENT PROV=" + ws_dep + "] "))
                    #
                    #    doc.push_relation(Relation("FORMATIONLOCATION", e1, e2, "[SAMESENT PROV=" + ws + "] "))
                    #    doc.push_relation(Relation("FORMATIONLOCATION", e1, e2, "[SAMESENT PROV=" + ws_dep + "] "))

                    #print ws_dep

                    #if len(ws) > 100:
                    #    ws = "LONGER-THAN-100"
                    #elif len(ws) > 50:
                    #    ws = "LONGER-THAN-50"
                    
                    if e1.type in ranks and e2.type in ranks:
                        if ranks[e1.type] < ranks[e2.type]:
                    
                            for pattern in features_pattern:
                                if re.search(pattern, ws):
                                    doc.push_relation(Relation("TAXONOMY", e1, e2, "[SAMESENT PROV=" + ws + "] "))
                                    doc.push_relation(Relation("TAXONOMY", e1, e2, "[SAMESENT PROV=" + ws_dep + "] "))
                                        
                            if ws in features:
                                doc.push_relation(Relation("TAXONOMY", e1, e2, "[SAMESENT PROV=" + ws + "] "))
                                doc.push_relation(Relation("TAXONOMY", e1, e2, "[SAMESENT PROV=" + ws_dep + "] "))

                    if ';' in ws and len(doc.sents[sent].words) > 10:
                        continue
                    
                        ## this is the negative example of formation
                    #if ('class' in e1.type or 'clade' in e1.type or 'subgenus' in e1.type or 'order' in e1.type or 'family' in e1.type or 'genus' in e1.type or 'species' in e1.type) and ('class' in e2.type or 'clade' in e2.type or 'subgenus' in e2.type or 'order' in e2.type or 'family' in e2.type or 'genus' in e2.type or 'species' in e2.type):
                    #    
                    #    if random.random() < 0.1 and (e1 != e2 and e1.entity not in e2.entity and e2.entity not in e1.entity):
                    #
                    #        doc.push_relation(Relation("FORMATION", e1, e2, "[SAMESENT PROV=" + ws + "] "))
                    #        doc.push_relation(Relation("FORMATION", e1, e2, "[SAMESENT PROV=" + ws_dep + "] "))
                    #    
                    #        #doc.push_relation(Relation("FORMATIONTEMPORAL", e1, e2, "[SAMESENT PROV=" + ws + "] "))
                    #       
                    #        #doc.push_relation(Relation("FORMATIONLOCATION", e1, e2, "[SAMESENT PROV=" + ws + "] "))
                    #        #doc.push_relation(Relation("FORMATIONLOCATION", e1, e2, "[SAMESENT PROV=" + ws_dep + "] "))

                    if ('class' in e1.type or 'clade' in e1.type or 'subgenus' in e1.type or 'order' in e1.type or 'family' in e1.type or 'genus' in e1.type or 'species' in e1.type) and e2.type == 'LOCATION':
                        doc.push_relation(Relation("LOCATION", e1, e2, "[SAMESENT PROV=" + ws + "] "))
                        doc.push_relation(Relation("LOCATION", e1, e2, "[SAMESENT PROV=" + ws_dep + "] "))

                        #doc.push_relation(Relation("FORMATION", e1, e2, "[SAMESENT PROV=" + ws + "] "))

                    if ('class' in e1.type or 'subgenus' in e1.type or 'clade' in e1.type or 'order' in e1.type or 'family' in e1.type or 'genus' in e1.type or 'species' in e1.type) and e2.type == 'ROCK':
                        
                        doc.push_relation(Relation("FORMATION",e1, e2, "[SAMESENT PROV=" + ws + "] "))
                        doc.push_relation(Relation("FORMATION",e1, e2, "[SAMESENT PROV=" + ws_dep + "] "))

                        if e2.entity not in rels['FORMATION']:
                            rels['FORMATION'][e2.entity]=(math.fabs(e1.words[0].insent_id-e2.words[0].insent_id), doc.get_sentrepr(sent), e1, e2)
                        else:
                            if math.fabs(e1.words[0].insent_id-e2.words[0].insent_id) < rels['FORMATION'][e2.entity][0]:
                                rels['FORMATION'][e2.entity]=(math.fabs(e1.words[0].insent_id-e2.words[0].insent_id), doc.get_sentrepr(sent), e1, e2)

                    #if ('class' in e1.type or 'clade' in e1.type or 'subgenus' in e1.type or 'order' in e1.type or 'family' in e1.type or 'genus' in e1.type or 'species' in e1.type) and e2.type == 'INTERVAL':
                    #    #doc.push_relation(Relation("TEMPORAL", e1, e2, "[SAMESENT]"))
                    #    doc.push_relation(Relation("FORMATION", e1, e2, "[SAMESENT PROV=" + ws + "] "))
                    #    doc.push_relation(Relation("FORMATION", e1, e2, "[SAMESENT PROV=" + ws_dep + "] "))

                    if (e1.type == 'ROCK') and e2.type == 'LOCATION':
                        
                        doc.push_relation(Relation("FORMATIONLOCATION", e1, e2, "[SAMESENT PROV=" + ws + "] "))
                        doc.push_relation(Relation("FORMATIONLOCATION", e1, e2, "[SAMESENT PROV=" + ws_dep + "] "))

                        if e1.entity not in rels['FORMATIONLOCATION']:
                            rels['FORMATIONLOCATION'][e1.entity] = (math.fabs(e1.words[0].insent_id-e2.words[0].insent_id), doc.get_sentrepr(sent), e1, e2) 
                        else:
                        	if math.fabs(e1.words[0].insent_id-e2.words[0].insent_id) < rels['FORMATIONLOCATION'][e1.entity][0]:
	                        	rels['FORMATIONLOCATION'][e1.entity]=(math.fabs(e1.words[0].insent_id-e2.words[0].insent_id), doc.get_sentrepr(sent), e1, e2)
        
                    if (e1.type == 'ROCK') and e2.type == 'INTERVAL':
                        #if ',' in ws:
                        doc.push_relation(Relation("FORMATIONTEMPORAL", e1, e2, "[SAMESENT PROV=" + ws + "] "))
                        doc.push_relation(Relation("FORMATIONTEMPORAL", e1, e2, "[SAMESENT PROV=" + ws_dep + "] "))
                        #else:
                        #    doc.push_relation(Relation("FORMATIONTEMPORAL", e1, e2, "[SAMESENT PROV=" + ws + "] " + "[SAMESENT PROV=NOTCONTAIN_COMMA] "))
                        #doc.push_relation(Relation("FORMATIONTEMPORAL", e1, e2, "[SAMESENT PROV=" + ws + "] "))

            for ent in rels['FORMATIONLOCATION']:
            	sentrepr=rels['FORMATIONLOCATION'][ent][1]
            	doc.push_relation(Relation("FORMATIONLOCATION", rels['FORMATIONLOCATION'][ent][2], rels['FORMATIONLOCATION'][ent][3], "[SAMESENT-NEAREST]"))
            for ent in rels['FORMATION']:
                sentrepr=rels['FORMATION'][ent][1]
                doc.push_relation(Relation("FORMATION",rels['FORMATION'][ent][2], rels['FORMATION'][ent][3], "[SAMESENT-NEARST]"))
	
        # extract fauna
			
        for sentid in doc.entities:
            ctcount = 0
            for e in doc.entities[sentid]:
                if 'genus' in e.type or 'species' in e.type:
                    ctcount = ctcount + 1
            if ctcount > 5 or 'fauna' in doc.sents[sentid].__repr__().lower() or 'foraminifer' in doc.sents[sentid].__repr__().lower():
                
                for sentid2 in range(sentid+1, min(max(doc.entities.keys()),sentid+6)):
                    if 'fauna' in doc.sents[sentid2].__repr__().lower() or 'foraminifer' in doc.sents[sentid2].__repr__().lower() :
                        
                        for e1 in doc.entities[sentid]:
                            for e2 in doc.entities[sentid2]:
                                if ('class' in e1.type or 'clade' in e1.type or 'order' in e1.type or 'family' in e1.type or 'genus' in e1.type or 'species' in e1.type) and e2.type == 'LOCATION':
                                    doc.push_relation(Relation("LOCATION", e1, e2, "[FAUNA SAME PARAGRAPH AFTER]"))

                                if ('class' in e1.type or 'clade' in e1.type or 'order' in e1.type or 'family' in e1.type or 'genus' in e1.type or 'species' in e1.type) and e2.type == 'ROCK':
                                    doc.push_relation(Relation("FORMATION", e1, e2, "[FAUNA SAME PARAGRAPH AFTER]"))

                                if ('class' in e1.type or 'clade' in e1.type or 'order' in e1.type or 'family' in e1.type or 'genus' in e1.type or 'species' in e1.type) and e2.type == 'INTERVAL':
                                    doc.push_relation(Relation("TEMPORAL", e1, e2, "[FAUNA SAME PARAGRAPH AFTER]"))
                                                
                        break
                    
                formations = {}
                for sentid2 in range(max(0,sentid-3), sentid):
                    for e in doc.entities[sentid2]:
                        if e.type == 'ROCK' and 'formation' in e.entity:
                            formations[e.entity] = e
            
                    if 'fauna' in doc.sents[sentid2].__repr__().lower() or 'foraminifer' in doc.sents[sentid2].__repr__().lower() :
                        for e1 in doc.entities[sentid]:
                            for e2 in doc.entities[sentid2]:
                                if ('class' in e1.type or 'clade' in e1.type or 'order' in e1.type or 'family' in e1.type or 'genus' in e1.type or 'species' in e1.type) and e2.type == 'INTERVAL':
                                    doc.push_relation(Relation("TEMPORAL", e1, e2, "[FAUNA SAME PARAGRAPH PREV]"))

                if len(formations) == 1:
                    for k in formations.keys():
                        e2 = formations[k]
                        for e1 in doc.entities[sentid]:
                            if ('class' in e1.type or 'clade' in e1.type or 'order' in e1.type or 'family' in e1.type or 'genus' in e1.type or 'species' in e1.type) and e2.type == 'ROCK':
                                doc.push_relation(Relation("FORMATION", e1, e2, "[FAUNA SAME PARAGRAPH PREV]"))

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
                        if ('class' in e1.type or 'clade' in e1.type or 'order' in e1.type or 'family' in e1.type or 'genus' in e1.type or 'species' in e1.type) and e2.type == 'ROCK':
                            doc.push_relation(Relation("FORMATION", e1, e2, "[SINGLE FORMATION PER DOC]"))




