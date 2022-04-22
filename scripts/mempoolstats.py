#! /usr/bin/python3

from datetime import *
import pandas as pd
import math
from ast import literal_eval

file_blocks = input("Enter the name of the .csv file containing blocks (default data/blocks-day.csv): ") or "../data/blocks-day.csv"
file_mempool = input("Enter the name of the .log file containing mempool statistics (default data/mempool-day.log): ") or "../data/mempool-day.log"

#? csv parsing
tran_block = pd.read_csv(file_blocks)
tran_block.timestamp = pd.to_datetime(tran_block.timestamp, unit='s')
f = open(file_mempool, "r")
blocks_total = 0


resfile = open("../results/demand-scenario.txt", "w") 


min1 = f.readline() # read the first line
min1 = min1[:-2]
min1 = literal_eval(min1)
new_users = []
pool = []
while True:
    min2 = f.readline()
    pool.append(math.trunc(sum(min1[2])/21000))
    if not min2:
        break
    min2 = min2[:-2]
    min2 = literal_eval(min2)
    cond1 = tran_block['timestamp'].dt.day == datetime.utcfromtimestamp(min1[0]).day
    cond2 = tran_block['timestamp'].dt.hour == datetime.utcfromtimestamp(min1[0]).hour
    cond3 = tran_block['timestamp'].dt.minute == datetime.utcfromtimestamp(min1[0]).minute
    blocks = tran_block[cond1 & cond2 & cond3]
    blocks = blocks.drop(blocks[blocks.gas_used == 0].index)
    new = math.trunc((sum(min2[2]) - sum(min1[2]) + sum(blocks['gas_used'])) / 21000)
    if new < 0:
        new = 0
    new_users.extend([new] * blocks.shape[0])
    blocks_total += blocks.shape[0]
    min1 = min2

resfile.write("demand_scenario = {}".format(str(new_users)))
resfile.write("real_demand_scenario = {}".format(str(pool)))
resfile.close()
f.close()

print("Blocks total: {}".format(blocks_total))
