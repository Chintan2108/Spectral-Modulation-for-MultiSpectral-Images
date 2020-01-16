# -*- coding: utf-8 -*-
"""
Created on Thu Jan 16 10:57:38 2020

@author: mrg19-02144103
"""

import pickle
from tqdm import tqdm 

x = []

with open('./classified_img.data', 'rb') as pf:
    x = pickle.load(pf)

labels = set()

for row in tqdm(x):
    labels = labels.union(set(row))

print(labels)