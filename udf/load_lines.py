#! /usr/bin/env python

from helper.easierlife import *

INPUT_FOLDER = BASE_FOLDER + "/input"

log("START PROCESSING!")

def get_boxes(docid, folder):
    boxes = {}
    boxfeatures = {}

    #print docid, folder
    # first, load all lines:
    for f in os.listdir(folder):
        m = re.search("cuneiform-page-(.*?).html", f)
        if m:
            pageid = int(m.group(1))
            if pageid not in boxes: boxes[pageid] = []
            for l in open(folder + "/" + f):
                m = re.search("<span class='ocr_line' id='.*?' title=\"bbox (.*?) (.*?) (.*?) (.*?)\">", l)
                if m:
                    sig = "p%dl%st%sr%sb%s" % (pageid, m.group(1), m.group(2), m.group(3), m.group(4))
                    if 'l0t0r0b0' in sig: continue
                    b = Box(sig)
                    b.docid = docid
                    b.type = "TEXT"
                    boxes[pageid].append(b)

    for l in open(folder + "/input.text"):
        try:
            # 2 Society NNP O   Society _   0   SENT_1  [p1l398t81r574b129],
            (wid, word, pos, ner, lemma, a, dep, c, d) = l.rstrip().split('\t')
            for bbbb in d[1:-2].split(', '):
                b = Box(bbbb)
                if b.page in boxes:
                    uniqboxes = {}
                    for bb in boxes[b.page]:
                        if bb.overlap(b):
                            uniqboxes[bb] = 1
                for bb in uniqboxes:
                    if bb not in boxfeatures:
                        boxfeatures[bb] = []
                    boxfeatures[bb].append([word, a, pos])
        except: continue

    for f in os.listdir(folder):
        m = re.search('page-(.*?).png_lines.png.txt', f)
        if m:
            pid = m.group(1)
            for y in open(folder + "/" + f.rstrip()):

                pid = int(pid)
                y = int(y)

                if pid not in boxes: boxes[pid] = []
                sig  = "p%dl%dt%dr%db%d" % (pid, 0, y, 3000, y+1)
                b = Box(sig)
                b.docid = docid
                b.type = "LINE"
                boxes[pid].append(b)

    return boxes

def generate_varaibles(docid, boxes):
    prevpage = 0
    for pid in boxes:
        while pid != prevpage:
            prevpage = prevpage + 1
            b = Box("p0l0t0r0b0")
            b.docid = docid
            b.type = "NEWPAGE"
            #print docid, b.type, b
            print json.dumps({"docid":docid, "type":b.type, "box":serialize(b), "is_intable":None, "boxstr":b.__repr__()})
        for b in sorted(boxes[pid], key=lambda x: x.top):

            # lets generate some training data for 14
            if docid == "14":
                if pid == 7:
                    print json.dumps({"docid":docid, "type":b.type, "box":serialize(b), "is_intable":True, "boxstr":b.__repr__()})
                elif pid == 2 or pid == 3 or pid == 4 or pid == 5:
                    print json.dumps({"docid":docid, "type":b.type, "box":serialize(b), "is_intable":False, "boxstr":b.__repr__()})
                elif b.__repr__() in ['p6l81t3266r1411b3331', 'p8l12t452r2148b522', 'p8l79t1634r837b1700', 'p8l87t2928r2153b3000', 'p8l12t452r2148b522','p8l12t538r2140b608','p8l14t620r2148b690','p8l6t704r2140b778','p8l8t788r2118b858','p8l12t872r2146b942','p8l12t956r2146b1026','p8l14t1040r2148b1112','p8l13t1125r2145b1196','p8l10t1208r2144b1280','p8l12t1294r2145b1364','p8l13t1379r883b1446','p8l12t1567r2149b1636','p8l79t1634r837b1700']:
                    print json.dumps({"docid":docid, "type":b.type, "box":serialize(b), "is_intable":False, "boxstr":b.__repr__()})
                else:
                    print json.dumps({"docid":docid, "type":b.type, "box":serialize(b), "is_intable":None, "boxstr":b.__repr__()})
            elif docid == "551.2":
                if pid > 30:
                    print json.dumps({"docid":docid, "type":b.type, "box":serialize(b), "is_intable":True, "boxstr":b.__repr__()})
                else:
                    print json.dumps({"docid":docid, "type":b.type, "box":serialize(b), "is_intable":None, "boxstr":b.__repr__()})
            elif docid == '1962.2':
                if pid == 15 and b.top > 1222:
                    print json.dumps({"docid":docid, "type":b.type, "box":serialize(b), "is_intable":True, "boxstr":b.__repr__()})
                else:
                    print json.dumps({"docid":docid, "type":b.type, "box":serialize(b), "is_intable":None, "boxstr":b.__repr__()})
            else:
                print json.dumps({"docid":docid, "type":b.type, "box":serialize(b), "is_intable":None, "boxstr":b.__repr__()})



for docid in os.listdir(INPUT_FOLDER):
    if docid.startswith('.'): continue

    #if docid != '14': continue

    boxes = get_boxes(docid, INPUT_FOLDER + "/" + docid)

    generate_varaibles(docid, boxes)





