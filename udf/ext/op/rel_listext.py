#! /usr/bin/env python

from helper.easierlife import *

from ext.doc.Relation import *

class ListRelationExtraction:
    
    def __init__(self):
        donothing = None
    
    def loadDict(self):
        donothing = None
    
    def extract(self, doc):
        
        ranks = {"subspecies":1,"species":2,"subgenus":3,"genus":4,"subtribe":5,"tribe":6,"subfamily":7,"family":8,"group":9,"superfamily":10,"infraorder":11,"suborder":12,"order":13,"superorder":14,"infraclass":15,"subclass":16,"class":17,"superclass":18,"subphylum":19,"phylum":20,"superphylum":21,"subkingdom":22,"kingdom":23,"superkingdom":24}
        for r in ranks.keys():
            ranks[r+"!"] = ranks[r]
        
        flag_start_context = False
        
        lastsent = None
        last_sent_entities = []
        
        lastsent_withgenus = None
        lastsent_withgenus_entities = []
        
        after_appendix = False
        seen_table_after_appendix = False
        
        contextentities = {"ROCK":None, "INTERVAL":None, "LOCATION":None}
        
        ents = {}
        for sentid in doc.entities:
            
            if len(doc.sents[sentid].words) < 3 and 'appendix' in doc.sents[sentid].words[0].word.lower():
                after_appendix = True
            
            if after_appendix != True: continue
            
            if doc.sents[sentid].words[0].word.lower() == 'table' or doc.sents[sentid].words[0].word.lower().startswith('reference'):
                seen_table_after_appendix = True
            
            if seen_table_after_appendix == True: continue
            
            for e in doc.entities[sentid]:
                if 'species' in e.type or 'genus' in e.type:
                    ents[e.entity.lower()] = 1

        if len(ents) < 30:
            return
        
        after_appendix = False
        seen_table_after_appendix = False
        
        for sentid in doc.entities:
        
            if len(doc.sents[sentid].words) < 3 and 'appendix' in doc.sents[sentid].words[0].word.lower():
                after_appendix = True

            if after_appendix != True: continue

            if doc.sents[sentid].words[0].word.lower() == 'table' or doc.sents[sentid].words[0].word.lower().startswith('reference') or doc.sents[sentid].words[0].word.lower().startswith('literature'):
                seen_table_after_appendix = True

            if seen_table_after_appendix == True: continue

            for e in doc.entities[sentid]:
                contextentities[e.type] = e
                    
            for e in doc.entities[sentid]:
                                
                if 'species' in e.type or 'genus' in e.type:
                    
                    if contextentities['ROCK'] != None and contextentities['INTERVAL'] != None and contextentities['LOCATION'] != None:
                        
                        #doc.relationtriples.append([e, contextentities['ROCK'], contextentities['LOCATION'], contextentities['INTERVAL']])
                        
                        doc.push_relation(Relation('LOCATION', e,  contextentities['LOCATION'], '[APPENDIX LIST]'))
                        doc.push_relation(Relation('FORMATION', e,  contextentities['ROCK'], '[APPENDIX LIST]'))
                        doc.push_relation(Relation('TEMPORAL', e,  contextentities['INTERVAL'], '[APPENDIX LIST]'))
                    










