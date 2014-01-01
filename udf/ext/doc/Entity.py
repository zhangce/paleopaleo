#! /usr/bin/env python

from ext.Util import *

class Entity:
    entity = None
    sentid = None
    phrase = None
    
    words = None
    type = None

    spectype = None

    eid = None

    author_year = None
    
    def __init__(self, _type, _entity, _words, ph=''):

        self.eid = ""
        self.author_year = ""
        self.entity = _entity
        self.words = _words
        if len(_words) > 0:
            self.sentid = _words[0].sentid
        if ph != '':
            self.phrase = ph
        else:
        	self.phrase = myjoin(" ", self.words, lambda (w) : w.word)
        self.type = _type

    def __repr__(self):
        return self.entity

    def overlap(self, other):
        for w1 in self.words:
            for w2 in other.words:
                if w1 == w2:
                    return True
        return False
