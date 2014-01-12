#! /usr/bin/env python

from helper.easierlife import *


class OccurrencesSuperviser:
    
    kb_fossil_formation = None
    kb_formation_temporal = None
    kb_formation_location = None
    kb_formation_country = None

    kb_country_code = None

    kb_taxonomy = None

    ranks = None

    def __init__(self):
        donothing = None
    
    def loadDict(self):
        
        self.kb_fossil_formation = {}
        self.kb_formation_temporal = {}
        self.kb_formation_location = {}
        self.kb_formation_country = {}
        self.kb_country_code = {}
        self.kb_taxonomy = {}

        self.ranks = {"subspecies":1,"species":2,"subgenus":3,"genus":4,"subtribe":5,"tribe":6,"subfamily":7,"family":8,"group":9,"superfamily":10,"infraorder":11,"suborder":12,"order":13,"superorder":14,"infraclass":15,"subclass":16,"class":17,"superclass":18,"subphylum":19,"phylum":20,"superphylum":21,"subkingdom":22,"kingdom":23,"superkingdom":24}
        for r in self.ranks.keys():
            self.ranks[r+"!"] = self.ranks[r]

        for l in open(BASE_FOLDER + "/dicts/macrostrat_supervision.tsv"):
            (name1, n1, n2, n3, n4) = l.split('\t')
            name1 = name1.replace(' Fm', '').replace(' Mbr', '').replace(' Gp', '')
            n1 = float(n1)
            n2 = float(n2)
            n3 = float(n3)
            n4 = float(n4.rstrip())

            #log(name1)
            #log(n1)
            #log(n2)
            #log(n3)
            #log(n4)

            for rock in [name1.lower(), name1.lower() + " formation", name1.lower() + " member"]:
                if rock not in self.kb_formation_temporal:
                    self.kb_formation_temporal[rock] = {}
                self.kb_formation_temporal[rock][(min(n1, n2, n3, n4), max(n1, n2, n3, n4))] = 1


        for l in open(BASE_FOLDER + '/dicts/paleodb_taxonomy.tsv'):
            (refid, rel, tax1, tax2) = l.rstrip().split('\t')
            if 'belongs to' not in rel and 'ive synonym' not in rel: continue
            tax1 = tax1.lower()
            tax2 = tax2.lower()

            if 'belongs to' in rel: rel = 'TAXONOMY'
            if 'ive synonym' in rel: rel = 'TAXONOMY2'

            if tax1 not in self.kb_taxonomy:
                self.kb_taxonomy[tax1] = {}
            self.kb_taxonomy[tax1][tax2] = rel

        for l in open(BASE_FOLDER + "/dicts/countrycode.tsv"):
            (abbrv, fullname) = l.rstrip().split('\t')
            self.kb_country_code[abbrv.lower()] = fullname.lower()

        for l in open(BASE_FOLDER + '/dicts/supervision_occurrences.tsv'):
            (reference_no, genus, species, formation, member, group, country, n1, n2, n3, n4) = l.split('\t')
            n1 = float(n1)
            n2 = float(n2)
            n3 = float(n3)
            n4 = float(n4.rstrip())

            formation = formation.lower() + " formation"
            member = member.lower() + " member"
            group = group.lower() + " group"

            country = country.lower()

            for fossil in [genus.lower(), genus.lower() + ' ' + species.lower()]:
                for rock in [formation, member, group]:
                    if fossil not in self.kb_fossil_formation:
                        self.kb_fossil_formation[fossil] = {}
                    if rock not in self.kb_fossil_formation[fossil]:
                        self.kb_fossil_formation[fossil][rock] = {}
                    self.kb_fossil_formation[fossil][rock][reference_no] = 1

            for rock in [formation.lower()]:
                if rock not in self.kb_formation_country:
                    self.kb_formation_temporal[rock] = {}
                    self.kb_formation_location[rock] = {}
                    self.kb_formation_country[rock] = {}
                #self.kb_formation_location[rock][]
                self.kb_formation_country[rock][country] = {}
                self.kb_formation_temporal[rock][(min(n1, n2, n3, n4), max(n1, n2, n3, n4))] = 1

    def teach_me(self, docid, relname, e1, e2):
        
        dd = docid.split('.')[0]

        if relname == 'FORMATION':

            ans = None

            if e2.type != 'ROCK':
                #log(e1.entity + "F---F" + e2.entity)
                ans = False     

            
            if e1.entity in self.kb_fossil_formation:

                if e2.entity in self.kb_fossil_formation[e1.entity]:
                    #log(e1.entity + "F+++F" + e2.entity)
                    ans = True

            #if ans == None: ans = False 
            return ans

        elif relname == 'FORMATIONLOCATION':

            ans = None

            if e1.type != 'ROCK' or e2.type != 'LOCATION':
                #log(e1.entity + "L---L" + e2.entity)
                ans = False  

            if e1.entity in self.kb_formation_country:

                if e2.entity.split('|')[1].lower() in self.kb_country_code:
                    country = self.kb_country_code[e2.entity.split('|')[1].lower()]
                    #log(e1.entity + " L----" + country)
                    #log(self.kb_formation_country[e1.entity])
                    if country in self.kb_formation_country[e1.entity]:
                        #log(e1.entity + "L+++L" + e2.entity)
                        ans = True
                    else:
                        #log(e1.entity + "L---L" + e2.entity)
                        ans = False
            #if ans == None: ans = False
            return ans

        elif relname == 'FORMATIONTEMPORAL':

            ans = None

            if e1.type != 'ROCK' or e2.type != 'INTERVAL':
                #log(e1.entity + "T---T" + e2.entity)
                ans = False
                return ans

            if e1.entity in self.kb_formation_temporal:
                (name, large, small) = e2.entity.split('|')
                large = float(large)
                small = float(small)

                overlapped = False
                for (a,b) in self.kb_formation_temporal[e1.entity]:
                    if max(b,large) - min(a,small) >= b-a + large-small + 10:
                        donothing = True
                    else:
                        overlapped = True

                if overlapped == True:
                    #log(e1.entity + "T+++T" + e2.entity)
                    ans = True
                else:
                    #log(self.kb_formation_temporal[e1.entity])
                    #log(e1.entity + "T~~~T" + e2.entity)
                    ans = False

            #if ans == None: ans = False
            return ans
        elif relname.startswith('TAXONOMY'):
            ans = None

            if e1.entity==e2.entity:
                return ans

            if e1.type not in self.ranks or e2.type not in self.ranks:
                ans = False

            if e1.entity in self.kb_taxonomy:
                if e2.entity in self.kb_taxonomy[e1.entity]:
                    if self.kb_taxonomy[e1.entity][e2.entity] == relname:
                        ans = True
                    else:
                        ans = False
                else:
                    has_same_rel = False
                    for ee in self.kb_taxonomy[e1.entity]:
                        if self.kb_taxonomy[e1.entity][ee] == relname:
                            has_same_rel = True
                    if has_same_rel == True:
                        ans = False
            return ans

        #print self.kb_fossil_formation
        #print self.kb_formation_temporal
        #print self.kb_formation_location






