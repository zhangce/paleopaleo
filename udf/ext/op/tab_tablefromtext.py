#! /usr/bin/env python

from helper.easierlife import *

import re

from ext.doc.Table import *
from ext.doc.Relation import *

class TableExtractorFromText:
    
    def __init__(self):
        donothing = None
    
    def loadDict(self):
        donothing = None
    
    def extract(self, doc):
        
        # detect caption
        history = {}
        for sentid in range(0, len(doc.sents)):
            
            if sentid in history: continue
            
            sent = doc.sents[sentid]
            nword = len(sent.words)
            
            if re.search('^(Table|TABLE) [0-9]* \.', sent.__repr__()) or (re.search('^(Table|TABLE) [0-9IVl]*', sent.__repr__()) and not sent.__repr__().endswith('.')) or (re.search('^(Table|TABLE) [0-9IVl]*$', sent.__repr__())):
                table = Table()
                table.caption.append(sent)
                remainid = sentid

                for remainid in range(remainid+1, len(doc.sents)):
                    remainsent = doc.sents[remainid]
                    
                    if remainsent.__repr__().endswith('.') or remainsent.__repr__().endswith('?'):
                        if re.search('[a-zA-Z]', remainsent.__repr__()):
                            
                            if not (len(remainsent.words)>=2 and remainsent.words[-2].word in ['sp', 'indet', 'cf', 'u/ia', 'continued'] or re.search('[^a-zA-Z]', remainsent.words[-2].word.lower()) or  len(remainsent.words[-2].word) == 1 and re.search('A-Z', remainsent.words[-2].word)):
                                table.caption.append(remainsent)
                                history[remainid] = 1
                            else:
                                if len(doc.sents[remainid-1].words) > 0 and doc.sents[remainid-1].words[-1].word == "?":
                                    table.caption.append(remainsent)
                                    history[remainid] = 1
                                else:
                                    remainid = remainid - 1
                                    break
                    else:
                        remainid = remainid - 1
                        break

                for remainid in range(remainid+1, len(doc.sents)):
                    remainsent = doc.sents[remainid]
                    if remainsent.__repr__().endswith('.'):
                        if re.search('[a-zA-Z]', remainsent.__repr__()):
                            if not (len(remainsent.words) < 3 or len(remainsent.words[-2].word.lower()) <= 3 or remainsent.words[-2].word.lower() in ['spp', 'sp', 'indet', 'cf', 'u/ia', 'continued'] or re.search('[^a-zA-Z]', remainsent.words[-2].word.lower())  or (len(remainsent.words[-2].word) == 1)):
                                
                                nextsent = remainid + 1
                                if nextsent >= len(doc.sents): break
                                
                                if len(doc.sents[nextsent].__repr__()) >= 3 and doc.sents[nextsent].__repr__().endswith('.') and re.search('[A-Za-z]', doc.sents[nextsent].__repr__()):
                                    break
                                
                    history[remainid] = 1
                    table.content.append(remainsent)
        
                doc.push_table(table)
    
