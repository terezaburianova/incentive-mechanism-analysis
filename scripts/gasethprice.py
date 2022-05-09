#! /usr/bin/python3

import sys
from datetime import *
import pandas as pd
import math

file_gasprice = input("Enter the name of the .csv file containing gas price (default data/AvgGasPrice.csv): ") or "../data/AvgGasPrice.csv"
file_ethprice = input("Enter the name of the .csv file containing ETH price (default data/EtherPrice.csv): ") or "../data/EtherPrice.csv"

#? date input and parsing
start_input = input("Enter start date (YYYY-MM-DD): ")
start = datetime.strptime(start_input, '%Y-%m-%d')
end_input = input("Enter end date (YYYY-MM-DD): ")
end = datetime.strptime(end_input, '%Y-%m-%d')

#? csv parsing
gasprice = pd.read_csv(file_gasprice, parse_dates=['Date(UTC)'])
gasprice.columns=gasprice.columns.str.replace('\(UTC\)','')
gasprice.columns=gasprice.columns.str.replace(' \(Wei\)','')
gasprice = gasprice[(gasprice['Date'] >= start) & (gasprice['Date'] <= end)]
gasprice = gasprice['Value'].tolist()

ethprice_f = pd.read_csv(file_ethprice, parse_dates=['Date(UTC)'])
ethprice_f.columns=ethprice_f.columns.str.replace('\(UTC\)','')
ethprice_f = ethprice_f[(ethprice_f['Date'] >= start) & (ethprice_f['Date'] <= end)]
ethprice_f = ethprice_f['Value'].tolist()
ethprice = []
for price in ethprice_f:
    ethprice.append(round(price))

if len(gasprice) != len(ethprice):
    sys.exit("The amount of values does not match.")
 
res_gas = open("../results/gas-chart.txt", "w")
res_eth = open("../results/eth-chart.txt", "w")
res_gas.write(str(gasprice))
res_eth.write(str(ethprice))
res_gas.close()
res_eth.close()