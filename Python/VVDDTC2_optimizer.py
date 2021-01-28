import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt


#####################################################################################
## Scipt used to find optimal sizing that minimize 2nd TC of VVDD for 2T+Header(G) ##
#####################################################################################

raw=[]
data=[]
T=[]

with open('test.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		raw.append(row)

header = raw[0]
raw = raw[1:]

for i in range(0, len(raw)):
	T.append(float(raw[i][0]))
	data.append(raw[i][1:])

data = np.array(data).astype(np.float)	
T = np.array(T).astype(np.float)	
coeffs = np.abs(np.polyfit(T,data,2))
min_TC2 = min(coeffs[0, :])
opt_index = int(np.where(coeffs==min_TC2)[1])

opt_header = header[opt_index+1]
print(" ".join(opt_header.split(" ")[1:]))
print(min_TC2)
