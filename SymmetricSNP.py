import pandas as pd
import re
import csv
import os
import sys
from collections import Counter
import collections
import numpy as np

path1 = input("Provide the path to the first group of annotated variants:")
path2 = input("Provide the path to the second group of annotated variants:")

dir_list1 = os.listdir(path1)
dir_list2 = os.listdir(path2)

def import_command(dir_list, path):
    set_dict = {}
    for item in dir_list:
        if item in dir_list:
            try:
                cp = pd.read_csv(path + item + "/annotated_variants.tab", delimiter="\t")
                cp = cp[cp['is_snp'] == True]
                set_dict[item] = set(cp['#Uploaded_variation'])
            except Exception:
                pass
    return set_dict

set_dict1 = import_command(dir_list1, path1)
set_dict2 = import_command(dir_list2, path2)

dict1 = {}
for key1, value1 in set_dict1.items():
    dict2= {}
    for key2, value2 in set_dict2.items():
        dict2[key2] = len(value1.symmetric_difference(value2))
    dict1[key1] = dict2

df = pd.json_normalize([{'index': k, **v} for k, v in dict1.items()])
df = df.set_index('index')
print("The minimum symmetric SNP-difference is: " + str(df.min().min()))
print("The rounded mean symmetric SNP-difference is: " + str(round(df.mean().mean(), 0)))
print("The maximum symmetric SNP-difference is: " + str(df.max().max()))
print(df)
