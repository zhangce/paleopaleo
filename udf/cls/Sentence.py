
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







