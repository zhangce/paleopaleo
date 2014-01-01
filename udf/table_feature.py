#! /usr/bin/env python

import re


from helper.easierlife import *


INPUT_FOLDER = BASE_FOLDER + "/input"


"""
psql -U $DB_USER -c "CREATE TABLE features ( id     bigserial primary key, \
											 docid  text,                  \
											 box    text,				   \
											 featuretype text,			   \
											 feature text);"               $DB_NAME

"""
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

	for pid in boxes:
		for b in sorted(boxes[pid], key=lambda x: x.top):
			if b.type == "TEXT":
				if b in boxfeatures:	
					if (b.left < 100 and b.right > 2000) or (b.right-b.left) > 1900:
						print json.dumps({"docid":docid, "box":serialize(b), "featuretype":"ISWHOLELINE", "feature":"WHOLELINE"})
					else:
						print json.dumps({"docid":docid, "box":serialize(b), "featuretype":"ISWHOLELINE", "feature":"NO IDEA !"})

				if b in boxfeatures:
					if len(boxfeatures[b]) > 1:
						if boxfeatures[b][0][0].lower() == 'table':
							print json.dumps({"docid":docid, "box":serialize(b), "featuretype":"HASKEYWORD", "feature":"KEYWORD:TABLE"})

		bkeys = sorted(boxes[pid], key=lambda x: x.top)
		for i in range(1, len(bkeys)-1):
			b  = bkeys[i-1]
			bb = bkeys[i]
			bbb= bkeys[i+1]

			if b.type == 'LINE' and bb.type == 'TEXT':
				print json.dumps({"docid":docid, "box":serialize(bb), "featuretype":"TABLECANDIDATE", "feature":"TABLECANDIDATE"})
				for j in range(1,20):
					if i+j < len(bkeys) and bkeys[i+j].type == "TEXT":
						if bkeys[i+j].voverlap(bb):
							print json.dumps({"docid":docid, "box":serialize(bkeys[i+j]), "featuretype":"TABLECANDIDATE", "feature":"TABLECANDIDATE"})
						else:
							break

			if bb.type == 'TEXT' and bbb.type == 'LINE':
				print json.dumps({"docid":docid, "box":serialize(bb), "featuretype":"TABLECANDIDATE", "feature":"TABLECANDIDATE"})
				for j in range(1,20):
					if i-j > 0:
						if bkeys[i-j].voverlap(bb) and bkeys[i-j].type == "TEXT":
							print json.dumps({"docid":docid, "box":serialize(bkeys[i-j]), "featuretype":"TABLECANDIDATE", "feature":"TABLECANDIDATE"})
						else:
							break

	return boxes


for docid in os.listdir(INPUT_FOLDER):
    if docid.startswith('.'): continue

    #if docid != '14': continue

    boxes = get_boxes(docid, INPUT_FOLDER + "/" + docid)
    
