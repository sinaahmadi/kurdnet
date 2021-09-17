#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
	Sina Ahmadi (ahmadi.sina@outlook.com)
	A script to convert the Kurdish WordNet (KurdNet) into OMW format
	Kurdish WordNet project: https://github.com/sinaahmadi/kurdnet
	2014-2021
	Last updated on September 17, 2021
"""
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
	for synset in KurdNet[element]:
		omw.append("\t".join([synset["ID"], "ckb:lemma_def", gloss_translations[synset["ID"]]])) # no synsets have two definitions (version 0.1.0)

for synset in base_concepts:
	for lemma in base_concepts[synset]:
		omw.append("\t".join([synset, "ckb:lemma", lemma]))
		
header = "# KurdNet (Kurdish WordNet)	ckb	https://github.com/sinaahmadi/kurdnet	Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)\n"
with open("wn-data-ckb.tab", "w") as f:
	f.write(header + "\n".join(sorted(omw)))
