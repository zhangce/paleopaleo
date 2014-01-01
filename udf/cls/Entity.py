

from helper.easierlife import *

def myjoin(d, array, mapfunc):
    rs = []
    for a in array:
        if mapfunc(a) not in ['?']: rs.append(mapfunc(a))
    return d.join(rs)

class Entity:
    entity = None
    sentid = None
    phrase = None
    
    words = None
    type = None

    spectype = None

    features = None
    
    def __init__(self, _type, _entity, _words, ph=''):
        self.entity = _entity
        self.words = _words
        if len(_words) > 0:
            self.sentid = _words[0].sentid
        if ph != '':
            self.phrase = ph
        else:
        	self.phrase = myjoin(" ", self.words, lambda (w) : w.word)
        self.type = _type

        self.features = {}

    def __repr__(self):
        return self.entity

    def overlap(self, other):
        for w1 in self.words:
            for w2 in other.words:
                if w1 == w2:
                    return True
        return False
