#! /usr/bin/env python

from helper.easierlife import *

import re

from ext.doc.Table import *
from ext.doc.Relation import *

class TableCaptionRelationExtractor:
    
    def __init__(self):
        donothing = None
    
    def loadDict(self):
        donothing = None
    
    def extract(self, doc):
        
        for table in doc.tables:

            exted = False
            
            #print table
            capentities = []
            for sent in table.caption:
                for e in doc.entities[sent.sentid]:
                    capentities.append(e)

            contententities = []
            for sent in table.content:
                for e in doc.entities[sent.sentid]:
                    contententities.append(e)
                
            for capentity in capentities:
                for contententity in contententities:
                    if 'class' in contententity.type or 'clade' in contententity.type or 'order' in contententity.type or 'family' in contententity.type or 'genus' in contententity.type or 'species' in contententity.type:
                        if capentity.type == 'LOCATION':
                            doc.push_relation(Relation('LOCATION', contententity, capentity, '[TABLE CAPTION]'))
                            exted = True
                        if capentity.type == 'ROCK':
                            doc.push_relation(Relation('FORMATION', contententity, capentity, '[TABLE CAPTION]'))
                            exted = True
                        if capentity.type == 'INTERVAL':
                            doc.push_relation(Relation('TEMPORAL', contententity, capentity, '[TABLE CAPTION]'))
                            exted = True




