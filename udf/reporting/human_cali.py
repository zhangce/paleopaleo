#! /usr/bin/env python

#from helper.easierlife import *

BASE_FOLDER = "/Users/czhang/Desktop/paleodeepdive.language/examples/paleo/"

import os

def norm(s):
	a = s.replace('<i>', '').replace('</i>', '')
	a = a.replace(',', '|')
	return a.lower()

relmap = {
	"FORMINT"           : "FORMATIONINTERVAL",
	"FORMLOC"           : "FORMATIONLOCATION",
	"FOSSFORM"          : "FORMATION",
	"belongs to"        : "TAXONOMY",
	"subjective synonym": "TAXONOMY2"
}

for l in open(BASE_FOLDER + "/dicts/paleo_feedbacks.tsv"):
	try:
		(user, time, signature) = l.rstrip().split('\t')
		if signature.startswith('EXT'):
			(ext, value, docid, rel, e1, e2) = signature.split('|')
			print relmap[rel], "\t", norm(e1), norm(e2)
	except:
		continue

