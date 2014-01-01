#! /usr/bin/env python

class Table:

    caption = None
    content = None

    def __init__(self):
        self.caption = []
        self.content = []

    def __repr__(self):
        rs = ""
        rs = rs + '+-----TABLE-----' + '\n'
        for sent in self.caption:
            rs = rs + '|[CAPTION] ' + sent.__repr__() + '\n'
        for sent in self.content:
            rs = rs + '|[CONTENT] ' + sent.__repr__() + '\n'
        rs = rs + '+-----ENDTB-----' + '\n'
        return rs
