#! /usr/bin/env python

from helper.easierlife import *

import re
from ext.doc.Relation import *

class SectionHeaderRealtionExtraction:
    
    taxgt = None
    
    def __init__(self):
        self.taxgt = {}
        donothing = None
    
    def loadDict(self):
        self.taxgt = {}

        for l in open(BASE_FOLDER + '/dicts/paleodb_taxonomy.tsv'):
            (refid, rel, tax1, tax2) = l.rstrip().split('\t')
            if 'belongs to' not in rel and 'ive synonym' not in rel: continue
            self.taxgt[(tax1+"|"+tax2).lower()] = rel
        
        donothing = None
    
    def extract_belongs(self, doc):

        ranks = {"subspecies":1,"species":2,"subgenus":3,"genus":4,"subtribe":5,"tribe":6,"subfamily":7,"family":8,"group":9,"superfamily":10,"infraorder":11,"suborder":12,"order":13,"superorder":14,"infraclass":15,"subclass":16,"class":17,"superclass":18,"subphylum":19,"phylum":20,"superphylum":21,"subkingdom":22,"kingdom":23,"superkingdom":24}
        for r in ranks.keys():
            ranks[r+"!"] = ranks[r]

        flag_start_context = False
        
        lastsent = None
        last_sent_entities = []
        
        lastsent_withgenus = None
        lastsent_withgenus_entities = []
        
        exts = {}
        log("Extracting belongs to...")
        
        syn_to_identify_not_all_cap = {}
        syn_to_identify_all_cap = {}
        
        history = {}
        goodsents = []
        for sentid in doc.entities:
            
            sent = doc.sents[sentid]

            isnextgood = False
            nextsentid = sentid + 1
            if nextsentid < len(doc.sents):
                nextsent = doc.sents[nextsentid]
                if nextsent.words[0].centered == True and (nextsent.__repr__().startswith('Fig')):
                    isnextgood = True
            flag_start_context = True

            if flag_start_context == True:
                                            
                firstentity_index = 10000
                firstentity = None
                for e in doc.entities[sentid]:
                    if e.words[0].insent_id < firstentity_index and e.type in ranks:
                        firstentity_index = e.words[0].insent_id
                        firstentity = e
                if firstentity != None:

                    allleft = True
                    for w in sent.words:
                        if w == firstentity.words[0]: break
                        if w.box.left >= firstentity.words[0].box.right and w.centered == False:
                            allleft = False
                    if (firstentity.words[0].centered == True or isnextgood == True) and len(sent.words) < 20 and allleft == True:

                        goodsents.append({"sentid":sentid, "isgood":True})
                    else:
                        goodsents.append({"sentid":sentid, "isgood":False})
                else:
                    goodsents.append({"sentid":sentid, "isgood":False})
        
        for i in range(0, len(goodsents)):
            sentid = goodsents[i]["sentid"]
            isgood = goodsents[i]["isgood"]

            if isgood == True:

                for e1 in doc.entities[sentid]:
                    for e2 in doc.entities[sentid]:
                        if e1.type in ranks and e2.type in ranks:
                            if ranks[e1.type] < ranks[e2.type] and 'species' not in e1.type and e1.type in doc.sents[sentid].__repr__().lower() and e2.type in doc.sents[sentid].__repr__().lower() :
                                doc.push_relation(Relation("TAXONOMY", e1, e2, "[SYSTEMATIC PALEONTOLOGY SECTION HEADER TYPE 1]"))

                for j in range(i+1, len(goodsents)):
                    sentid2 = goodsents[j]["sentid"]
                    isgood2 = goodsents[j]["isgood"]

 

                    if isgood2 == True:
                        for e1 in doc.entities[sentid2]:
                            for e2 in doc.entities[sentid]:
                                if e1.type in ranks and e2.type in ranks:
                                    if ranks[e1.type] < ranks[e2.type] and 'species' not in e1.type:
                                    #if e2.entity == 'anthracomarti':
                                    #    import pdb
                                    #    pdb.set_trace()

                                        #log('#####' + e1.entity + '-->' + e2.entity)
                                        doc.push_relation(Relation("TAXONOMY", e1, e2, "[SYSTEMATIC PALEONTOLOGY SECTION HEADER TYPE 2]"))
                                        
                        break
                    else:
                        if doc.sents[sentid2].words[0].centered == True:
                            break


    
    def extract(self, doc):

        self.extract_belongs(doc)
        
        ranks = {"subspecies":1,"species":2,"subgenus":3,"genus":4,"subtribe":5,"tribe":6,"subfamily":7,"family":8,"group":9,"superfamily":10,"infraorder":11,"suborder":12,"order":13,"superorder":14,"infraclass":15,"subclass":16,"class":17,"superclass":18,"subphylum":19,"phylum":20,"superphylum":21,"subkingdom":22,"kingdom":23,"superkingdom":24}
        for r in ranks.keys():
            ranks[r+"!"] = ranks[r]
        
        flag_start_context = False
        
        lastsent = None
        last_sent_entities = []
        
        lastsent_withgenus = None
        lastsent_withgenus_entities = []
        
        exts = {}
        
        syn_to_identify_not_all_cap = {}
        syn_to_identify_all_cap = {}
				# using a dictionary
        history = {}

        """
        for sentid1 in doc.entities:
            for e1 in doc.entities[sentid1]:
                #if e1.entity in history: continue
                history[e1.entity] = 1
                for sentid2 in doc.entities:
                    for e2 in doc.entities[sentid2]:
       
                        if e1.entity + "|" + e2.entity in self.taxgt and 'species' in e1.type and 'species' in e2.type:
                            if e1.entity + "|" + e2.entity not in history:
                                history[e1.entity + "|" + e2.entity] = 1
                            else:
                                brokenup = True
                                continue
                            rel = self.taxgt[e1.entity + "|" + e2.entity]

                            if 'belongs' in rel:
                                doc.push_relation(Relation("TAXONOMY", e1, e2, "[LOOKUP]" ))
                            if 'synonym' in rel:
                                doc.push_relation(Relation("TAXONOMY2", e1, e2, "[LOOKUP]" ))
        
                        if e1.entity + "|" + e2.entity in self.taxgt:
                            rel = self.taxgt[e1.entity + "|" + e2.entity]
                            if 'belongs' in rel:
                                doc.push_relation(Relation("TAXONOMY", e1, e2, "[LOOKUP]" ))
        """
        
        history = {}
        for sentid in doc.entities:
            
            sent = doc.sents[sentid]

            isnextgood = False
            nextsentid = sentid + 1
            if nextsentid < len(doc.sents):
                nextsent = doc.sents[nextsentid]
                if nextsent.words[0].centered == True and (nextsent.__repr__().startswith('Fig')):
                    isnextgood = True

            flag_start_context = True


            if flag_start_context == True:
                                            
                firstentity_index = 10000
                firstentity = None
                for e in doc.entities[sentid]:
                    if e.words[0].insent_id < firstentity_index and 'species' in e.type:
                        firstentity_index = e.words[0].insent_id
                        firstentity = e

                if firstentity == None:
                    for e in doc.entities[sentid]:
                        if e.words[0].insent_id < firstentity_index and 'genus' in e.type and 'Genus' in sent.words[0].word:
                            firstentity_index = e.words[0].insent_id
                            firstentity = e
                
                if firstentity != None:

                    if (firstentity.words[0].centered == True or isnextgood == True) and (firstentity.words[0].left_margin < 100 or 'genus' in firstentity.type) and len(sent.words) < 20:
                        #print sent

                        for sentid2 in doc.entities:
                            if sentid2 <= sentid: continue
                            if sentid2 >= sentid + 100: continue

                            if firstentity.entity == ''.lower():
                                import pdb
                                pdb.set_trace()

                            sent2 = doc.sents[sentid2]

                            exists_center = False
                            for w in sent2.words:
                                if w.centered == True:
                                    exists_center = True
                            if exists_center == True and sentid2-sentid >= 5:
                                break

                            if sent2.words[0].word in ['Discussion', 'Material', 'Remarks', 'Matericzl', 'Remczrks', 'Type', 'Revised', 'Included', 'Diagnosis', 'Referred', '']:
                                break

                            firstentity_index2 = 10000
                            firstentity2 = None
                            doesbreak = False
                            hh = {}
                            for e in doc.entities[sentid2]:
                                if e.entity in hh:
                                    continue
                                hh[e.entity] = 1

                                if ('species' in e.type and 'species' in firstentity.type) or ('genus' in e.type and 'genus' in firstentity.type and e.words[0].left_margin < 40):
                                    firstentity_index2 = e.words[0].insent_id
                                    firstentity2 = e

                                    if firstentity2.words[0].centered == True:
                                        doesbreak = True
                                        break

                                    if firstentity2.words[0].centered == False and firstentity2.words[0].followed == True and (firstentity2.words[0].left_margin < 100 or firstentity_index2 < 3):

                                        allleft = True
                                        for w in sent2.words:
                                            if w == firstentity2.words[0]: break
                                            if w.box.left >= firstentity2.words[0].box.right and w.followed == False:
                                                allleft = False
 
                                        if allleft == True and firstentity2.words[0].box.page - firstentity.words[0].box.page <= 1 :
                                            #print "   ", firstentity2.words[0].left_margin, sent2
                                            if firstentity2.entity != firstentity.entity:
                                                doc.push_relation(Relation("TAXONOMY2", firstentity2, firstentity, "[SYSTEMATIC PALEONTOLOGY SECTION HEADER TYPE 1]"))
                            if doesbreak == True:
                                break

