#! /usr/bin/env python

from ext.Util import *

class Relation:
    type = None
    entity1 = None
    entity2 = None
    prov = None

    rid = None

    def __init__(self, _type, _entity1, _entity2, _prov):
        self.type = _type
        self.entity1 = _entity1
        self.entity2 = _entity2
        self.prov = _prov

        self.rid = ""
