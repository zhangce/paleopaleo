#! /usr/bin/env python

class Sentence:
    sentid = None
    words = None

    def __init__(self):
        self.words = []
        self.sentid = None

    def __repr__(self):
        _words = []
        for w in self.words:
            _words.append(w.word)
        return " ".join(_words)
    
    def push_word(self, word):
        if self.sentid== None:
            self.sentid = word.sentid
            self.words.append(word)
            return True
        else:
            if self.sentid == word.sentid:
                self.words.append(word)
                return True
            else:
                return False

    def get_word_dep_path(self, idx1, idx2):
        
        path1 = []
        path2 = []

        c = idx1
        i = len(self.words) + 10
        while i > 0:
            i = i -1
            try:
                if c == -1: break
                path1.append(c)
                c = self.words[c].deppar
            except:
                break

        c = idx2
        i = len(self.words) + 10
        while i > 0:
            i = i -1
            try:
                if c == -1: break
                path2.append(c)
                c = self.words[c].deppar
            except:
                break

        parent = None
        for i in range(0, max(len(path1), len(path2))):
            tovisit = 0 - i - 1
            if i >= len(path1) or i >= len(path2):
                break
            if path1[tovisit] != path2[tovisit]:
                break
            parent = path1[tovisit]
        #print parent

        first_word_to_parent = []
        c = idx1   
        i = len(self.words) + 10
        while i > 0:
            i = i -1
            try:
                if c == -1: break
                if c == parent: break
                if c == idx1: 
                    first_word_to_parent.append(self.words[c].deppath)
                else:
                    if self.words[c].ner != 'O':
                        first_word_to_parent.append(self.words[c].deppath + "|" + self.words[c].ner)
                    else:
                        first_word_to_parent.append(self.words[c].deppath + "|" + self.words[c].lemma)
                c = self.words[c].deppar
            except:
                break

        second_word_to_parent = []
        c = idx2
        i = len(self.words) + 10
        while i > 0:
            i = i -1
            try:
                if c == -1: break
                if c == parent: break
                if c == idx2:
                    second_word_to_parent.append(self.words[c].deppath)
                else:
                    if self.words[c].ner != 'O':
                        second_word_to_parent.append(self.words[c].deppath + "|" + self.words[c].ner)
                    else:
                        second_word_to_parent.append(self.words[c].deppath + "|" + self.words[c].lemma)
                c = self.words[c].deppar   
            except:
                break

        #print first_word_to_parent
        #print second_word_to_parent

        return "-".join(first_word_to_parent) + "@" + "-".join(second_word_to_parent)

    def dep_path(self, entity1, entity2):
    
        begin1 = entity1.words[0].insent_id
        end1 = entity1.words[-1].insent_id
        begin2 = entity2.words[0].insent_id
        end2 = entity2.words[-1].insent_id
    
        paths = []
        for idx1 in range(begin1, end1+1):
            for idx2 in range(begin2, end2+1):
                paths.append(self.get_word_dep_path(idx1, idx2))

        path = ""
        ll = 100000000
        for p in paths:
            if len(p) < ll:
                path = p
                ll = len(p)
        return path


    def wordseq_feature(self, entity1, entity2):
        
        begin1 = entity1.words[0].insent_id
        end1 = entity1.words[-1].insent_id
        begin2 = entity2.words[0].insent_id
        end2 = entity2.words[-1].insent_id

        start = end1 + 1
        finish = begin2 - 1
        prefix = ""

        if end2 <= begin1:
            start = end2 + 1
            finish = begin1 - 1
            prefix = "INV:"
        
        ss = []
        for w in range(start, finish + 1):
            if self.words[w].ner == 'O':
                ss.append(self.words[w].word)
            else:
                ss.append(self.words[w].ner)

        return prefix + "_".join(ss)

    def wordseq_feature2(self, begin1, end1, begin2, end2):
        
        start = end1 + 1
        finish = begin2 - 1
        prefix = ""

        if end2 <= begin1:
            start = end2 + 1
            finish = begin1 - 1
            prefix = "INV:"
        
        ss = []
        for w in range(start, finish + 1):
            if self.words[w].ner == 'O':
                ss.append(self.words[w].word)
            else:
                ss.append(self.words[w].ner)

        return prefix + "_".join(ss)







