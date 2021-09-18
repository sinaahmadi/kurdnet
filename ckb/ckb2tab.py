#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
        Sina Ahmadi (ahmadi.sina@outlook.com)
        A script to convert the Kurdish WordNet (KurdNet) into OMW format
        Kurdish WordNet project: https://github.com/sinaahmadi/kurdnet
        2014-2021
        Last updated on September 17, 2021
"""
import collections

###
### mappings
###
mapdir = "mapping-20-30/"
maps = ["wn20-30.adj", "wn20-30.adv", "wn20-30.noun", "wn20-30.verb"]
pos = {"wn20-30.adj" : "a", "wn20-30.adv" : "r", 
       "wn20-30.noun" : "n", "wn20-30.verb" : "v", }
map2030 = collections.defaultdict(lambda: 'unknown');
for m in maps:
    mf = open(mapdir + m)
    p = pos[m]
    for l in mf:
        lst = l.strip().split()
        fsfrom = lst[0] + "-" + p
        fsto = sorted([(lst[i+1], lst[i]) for i in range(1,len(lst),2)])[-1][1]
        ##print "%s-%s\t%s-%s" % (fsfrom, p, fsto, p)
        map2030[fsfrom] = "%s-%s" % (fsto, p)



import json

gloss_translations, base_concepts, omw = dict(), dict(), list()
with open("../Translated_Glosses.tsv", "r") as f:
        for i in f.read().split("\n")[1:]:
                gloss_translations[i.split("\t")[0]] = i.split("\t")[3]

with open("../Base_Concepts/Base_Concepts_in_KurdNet - min.tsv", "r") as f: # min outperforms max (see the paper)
        for i in f.read().split("\n")[1:]:
                if len(i.split("\t")[1].strip()):
                        base_concepts[i.split("\t")[0].strip()] = [j for j in i.split("\t")[1].strip().split(";") if len(j)]

with open("../5000_bc.json", "r") as f:
        KurdNet = json.load(f)["kurdnet"]["synsets"]

for element in KurdNet:
        for ss20 in KurdNet[element]:
                ss30 = map2030[ss20["ID"][6:]]
                dfn = gloss_translations[ss20["ID"]]
                omw.append("\t".join([ss30, "ckb:def", '0',  dfn])) # no synsets have two definitions (version 0.1.0)

for ss20 in base_concepts:
        for lemma in base_concepts[ss20]:
                ss30 = map2030[ss20[6:]]
                omw.append("\t".join([ss30, "ckb:lemma", lemma]))
                
header = "# KurdNet (Kurdish WordNet)\tckb\thttps://github.com/sinaahmadi/kurdnet\tCC BY SA 4.0\n"
with open("wn-data-ckb.tab", "w") as f:
        f.write(header + "\n".join(sorted(omw)))
