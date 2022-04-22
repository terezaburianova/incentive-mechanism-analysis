#! /usr/bin/python3

# get fees from real data, receipts.csv file needs to be edited for the day only

from datetime import *
import pandas as pd
import math
from ast import literal_eval
import statistics

file_receipts = input("Enter the name of the .csv file containing txns receipts (default data/receipts.csv): ") or "../data/receipts.csv"
file_blocks = input("Enter the name of the .csv file containing blocks (default data/blocks-day.csv): ") or "../data/blocks-day.csv"

#? csv parsing - blocks list
blocks_csv = pd.read_csv(file_blocks)
blocks_nums = blocks_csv['number'].tolist()

#? csv parsing - receipts
receipts = pd.read_csv(file_receipts)

resultmean = []
resultmedian = []
resfile = open("../results/average-fees.txt", "w") 
for blocknum in blocks_nums:
    current = receipts[receipts['block_number'] == blocknum]
    all_fees = []
    for index, row in current.iterrows():
        cfee = math.trunc(row['effective_gas_price'] * (10 ** (-9)))
        if (cfee != 0):
            all_fees.append(cfee)
    if (len(all_fees) > 0):
        resultmean.append(round(statistics.mean(all_fees)))
        resultmedian.append(round(statistics.median(all_fees)))
resfile.write("mean = {}\n\n".format(str(resultmean)))
resfile.write("median = {}".format(str(resultmedian)))
resfile.close()

