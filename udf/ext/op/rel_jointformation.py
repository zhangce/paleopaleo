#! /usr/bin/env python

from helper.easierlife import *

from ext.doc.Relation import *
import math

class JointFormationRelationExtractor:
    
    def __init__(self):
        donothing = None
    
    def loadDict(self):
        donothing = None
    
    def extract(self, doc):
                
        formationloc = {}
        for rel in doc.relations:
            if rel.type == 'FORMATIONLOCATION':
                if rel.entity1.entity.lower() not in formationloc:
                    formationloc[rel.entity1.entity.lower()] = {}
                formationloc[rel.entity1.entity.lower()][rel.entity2.entity.lower()] = 1
    
        formationtemp = {}
        for rel in doc.relations:
            if rel.type == 'FORMATIONTEMPORAL':
                if rel.entity1.entity.lower() not in formationtemp:
                    formationtemp[rel.entity1.entity.lower()] = {}
                formationtemp[rel.entity1.entity.lower()][rel.entity2.entity.lower()] = 1
    
        a = """
        for rel1 in doc.relations:
            for rel2 in doc.relations:
                if rel2.type == 'FORMATIONLOCATION' and len(formationloc[rel2.entity1.entity.lower()]) == 1:
                    if rel1.type == "FORMATION" and rel2.type == 'FORMATIONLOCATION':
                        if rel1.entity2.entity == rel2.entity1.entity:
                            doc.push_relation(Relation("LOCATION", rel1.entity1, rel2.entity2, ("%d" % math.fabs(rel2.entity1.words[0].sentid - rel1.entity1.words[0].sentid)) +  " [JOINT(SAME FORMATION)] " + "[" + rel1.prov + "] " + "[" + rel2.prov + "] "))
                
                if rel1.type == "FORMATION" and rel2.type == 'FORMATIONTEMPORAL' and len(formationtemp[rel2.entity1.entity.lower()]) <= 3:
                    if rel1.entity2.entity == rel2.entity1.entity:
                        doc.push_relation(Relation("TEMPORAL", rel1.entity1, rel2.entity2, ("%d" % math.fabs(rel2.entity1.words[0].sentid - rel1.entity1.words[0].sentid)) +  " [JOINT(SAME FORMATION)] " + "[" + rel1.prov + "] " + "[" + rel2.prov + "] "))
        """

        expands = {}
        e2e = {}
        # we want to expand temporal interval to finer grained intervals
        for sent1 in doc.entities:
            for e1 in doc.entities[sent1]:
                e2e[e1.entity] = e1
                for e2 in doc.entities[sent1]:
                    if e1.type == 'INTERVAL' and e2.type == 'INTERVAL':
                        (a,large1,small1) = e1.entity.split('|')
                        (a,large2,small2) = e2.entity.split('|')
                        large1 = float(large1)
                        large2 = float(large2)
                        small1 = float(small1)
                        small2 = float(small2)
    
                        if small2 >= small1 and large2 <= large1 and e1.entity != e2.entity:
                            if e1.entity not in expands: expands[e1.entity] = {}
                            if e2.entity not in expands[e1.entity]:
                                expands[e1.entity][e2.entity] = 0
                            expands[e1.entity][e2.entity] = expands[e1.entity][e2.entity] + 1
                        
        final_expands = {}
        for e1 in expands:
            for e2 in expands[e1]:
                if expands[e1][e2] > 1 or (len(expands[e1]) == 1):
                    if e1 not in final_expands:
                        final_expands[e1] = {}
                    final_expands[e1][e2] = expands[e1][e2]
                       
        a = """     
        history = {}
        for rel in doc.relations:
            if rel.type == 'TEMPORAL' and rel.entity1.entity not in history:
                history[rel.entity1.entity] = 1
                if rel.entity2.entity in final_expands and len(final_expands[rel.entity2.entity]) <= 2:
                    for en2 in final_expands[rel.entity2.entity]:
                        entity2 = e2e[en2]
                        doc.push_relation(Relation("TEMPORAL", rel.entity1, entity2, " [JOINT(INTERVAL EXPANSION)] " + rel.entity2.entity + " --> " + en2))
        """

        allfossils = {}
        allfossilsreldomain = {}
        allformations = {}
        allformationsdomain = {}
        for rel in doc.relations:
            if rel.type == 'TAXONOMY' or rel.type == 'TAXONOMY2': continue
            if rel.entity1.type != 'INTERVAL' and rel.entity1.type != 'ROCK' and rel.entity1.type != 'LOCATION':
                allfossils[rel.entity1.entity] = rel.entity1
                if rel.entity1.entity not in allfossilsreldomain: allfossilsreldomain[rel.entity1.entity] = {}
                allfossilsreldomain[rel.entity1.entity][rel.type] = 1
            if rel.entity2.type == 'ROCK':
                allformations[rel.entity2.entity] = rel.entity2
                if rel.entity2.entity not in allformationsdomain: allformationsdomain[rel.entity2.entity] = {}
                allformationsdomain[rel.entity2.entity][rel.type] = 1
            if rel.entity1.type == 'ROCK' and rel.type == 'FORMATIONLOCATION':
                if rel.entity1.entity not in allformationsdomain: allformationsdomain[rel.entity1.entity] = {}
                allformationsdomain[rel.entity1.entity][rel.type] = 1
                    
        for eee in allfossils:
            if 'LOCATION' not in allfossilsreldomain[eee]:
                for e in doc.titleentities:
		    if e.type =="LOCATION":
                        doc.push_relation(Relation("LOCATION", allfossils[eee], e, " [TITLE CONTEXT] " + doc.title))

        for eee in allformations:
            if 'FORMATIONLOCATION' not in allformationsdomain[eee]:
                for e in doc.titleentities:
		    if e.type == "LOCATION":
                        #print "FORMATIONLOCATION", allformations[eee], e
                        doc.push_relation(Relation("FORMATIONLOCATION", allformations[eee], e, " [TITLE CONTEXT]"))
            if 'FORMATIONTEMPORAL' not in allformationsdomain[eee]:
                for e in doc.titleentities:
		    if e.type == "INTERVAL":
                        #print "FORMATIONTEMPORAL", allformations[eee], e
                        doc.push_relation(Relation("FORMATIONTEMPORAL", allformations[eee], e, " [TITLE CONTEXT]"))

                        
                        




                  
