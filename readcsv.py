#! /usr/bin/python3

import sys
from datetime import *
import pandas as pd
import math

file_blocks = input("Enter the name of the .csv file containing block count (default blocks.csv): ") or "blocks.csv"
file_tran = input("Enter the name of the .csv file containing total gas used (default gas.csv): ") or "gas.csv"
scale = input("Enter the scale for hardware restriction purposes (default 1): ") or "1"
scale = int(scale)
#percentage = input("Enter the percentage of requests to add in case of data containing only included transactions (default 25): ")

#? date input and parsing
start_input = input("Enter start date (YYYY-MM-DD): ")
start = datetime.strptime(start_input, '%Y-%m-%d')
end_input = input("Enter end date (YYYY-MM-DD): ")
end = datetime.strptime(end_input, '%Y-%m-%d')

#? csv parsing
blocks = pd.read_csv(file_blocks, parse_dates=['Date(UTC)'])
blocks.columns=blocks.columns.str.replace('\(UTC\)','')
blocks = blocks[(blocks['Date'] >= start) & (blocks['Date'] <= end)]
blocks = blocks['Value'].tolist()

tran_total = pd.read_csv(file_tran, parse_dates=['Date(UTC)'])
tran_total.columns=tran_total.columns.str.replace('\(UTC\)','')
tran_total = tran_total[(tran_total['Date'] >= start) & (tran_total['Date'] <= end)]
tran_total = tran_total['Value'].tolist()

if len(blocks) != len(tran_total):
    sys.exit("The count of blocks and gas data does not match.")
 

#? average incoming transaction requests per block
tran = []
for block_index, tran_total in enumerate(tran_total):
    tvalue = math.trunc(tran_total / 12000 / blocks[block_index] / scale)
    #tvalue = math.trunc(tvalue + (tvalue / 100 * percentage))
    tran.append(tvalue)

blocks_scaled = blocks #TODO remove later
# blocks_scaled = []
# for bvalue in blocks:
#     blocks_scaled.append(math.trunc(bvalue / scale))


result = "demand_scenario = " + "[{} for i in range({})]".format(tran[0], blocks_scaled[0])
blocks_total = blocks_scaled[0]
for index in range(1, len(blocks_scaled)):
    result += " + [{} for i in range({})]".format(tran[index], blocks_scaled[index])
    blocks_total += blocks_scaled[index]

print("Blocks total: {}".format(blocks_total))
print("Set the following constants: ")
# print("\"TARGET_GAS_USED\": {}".format(12500000 / scale))
# print("\"MAX_GAS_EIP1559\": {}".format(25000000 / scale))
print(result)
