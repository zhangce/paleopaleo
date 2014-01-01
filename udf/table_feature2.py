#! /usr/bin/env python

import re

from helper.easierlife import *

INPUT_FOLDER = BASE_FOLDER + "/input"


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

	bkeys = []
	for pid in sorted(boxes.keys()):
		for b in sorted(boxes[pid], key=lambda x: x.top):
			bkeys.append(b)

	for i in range(1, len(bkeys)-1):

		b  = bkeys[i]
		bb = bkeys[i+1]

		if b.type == "TEXT":
			if bb.type != "LINE":
				print json.dumps({"docid":docid, "boxstr1":b.__repr__(), "boxstr2":bb.__repr__(), "box1":serialize(b), "box2":serialize(bb), "featuretype":"CONSISTENT", "feature":"CONSISTENT"})

	return boxes


for docid in os.listdir(INPUT_FOLDER):
    if docid.startswith('.'): continue

    #if docid != '14': continue

    boxes = get_boxes(docid, INPUT_FOLDER + "/" + docid)

