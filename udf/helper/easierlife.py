#! /usr/bin/env python

import fileinput
import json
import math

#from helper.ocr import *

from cls.Box import *
from cls.Word import *
from cls.Sentence import *
from cls.Entity import *

import zlib

import sys

import os

import cPickle as pickle

import itertools

import os

BASE_FOLDER, throwaway = os.path.split(os.path.realpath(__file__))
BASE_FOLDER = BASE_FOLDER + "/../../"

def is_fossil_entity(ent):
	if 'class' in ent.type or 'clade' in ent.type or 'subgenus' in ent.type or 'order' in ent.type or 'family' in ent.type or 'genus' in ent.type or 'species' in ent.type:
		return True
	else:
		return False

def myjoin(d, array, mapfunc):
	rs = []
	for a in array:
		if mapfunc(a) not in ['?']: rs.append(mapfunc(a))
	return d.join(rs)

def my_par_join(d, array):
    rss = []
    for a in array:
        if a.altword != a.word and a.altword != None:
            rss.append([a.word, a.altword])
        else:
            rss.append([a.word])

    for i in itertools.product(*rss):
        rs = []
        for a in i:
            if a not in ['?', '']:
                rs.append(a)
        yield d.join(rs)

def log(str):
	sys.stderr.write(str.__repr__() + "\n")

def serialize(obj):
	#return zlib.compress(pickle.dumps(obj))
	return pickle.dumps(obj)

def deserialize(obj):
	#return pickle.loads(str(unicode(obj)))
	return pickle.loads(obj.encode("utf-8"))

def get_inputs():
	for line in fileinput.input():
		yield json.loads(line)

def dump_input(OUTFILE):
	fo = open(OUTFILE, 'w')
	for line in fileinput.input():
		fo.write(line)
	fo.close()
