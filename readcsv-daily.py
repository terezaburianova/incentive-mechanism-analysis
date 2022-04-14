#! /usr/bin/python3

import sys
from datetime import *
import pandas as pd
import math

file_blocks = input("Enter the name of the .csv file containing blocks (default blocks-short.csv): ") or "blocks-short.csv"

#? csv parsing
tran_block = pd.read_csv(file_blocks)
tran_block = tran_block['gas_used'].tolist()
block_fin = []

for block in tran_block:
    if block != 0:
        block_fin.append(round(block / 12000))


# result = "demand_scenario = " + "[{} for i in range(1)]".format(tran_block[0])
# for i in range(1, len(tran_block)):
#     result += " + [{} for i in range(1)]".format(tran_block[i])

print("Blocks total: {}".format(len(block_fin)))

resfile = open("result.txt", "w") 
resfile.write(str(block_fin))
resfile.close()
