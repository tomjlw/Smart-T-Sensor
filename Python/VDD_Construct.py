import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
import csv
import math
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression

raw_data = []
R2 = []
N_TK = 21
N_VDD = 21
VDD_min = 0.2
VDD_max = 0.4
TK_min = 273
TK_max = 373
TT_VDD = 0.26
diff_VDD = 0.03 # the VDD variation values across corners
file_name = "VDD_Construct.csv"


with open(file_name) as f:
	spamreader = list(csv.reader(f, delimiter='\t'))
	
	for i in range(1, len(spamreader)):
		for j in range(0, len(spamreader[i])):
			if (spamreader[i][j] != ''):					# remove empty list
				raw_data.append(float(spamreader[i][j]))

	raw_data = np.array(raw_data).reshape(N_VDD,N_TK, 5)	# transform 1d string array into 3d floating matrix 

#print(raw_data)	

SS_VDD = TT_VDD + diff_VDD									# create some constants
SF_VDD = TT_VDD + 2*diff_VDD
FS_VDD = TT_VDD - diff_VDD
FF_VDD = TT_VDD - 2*diff_VDD
VDD_list = np.linspace(VDD_min, VDD_max, N_VDD)
TK_list = np.linspace(TK_min, TK_max, N_TK)
TK_repeat = np.array(np.repeat(TK_list, 5, axis=0)).reshape(N_TK,5)

VDD_idx = [round((element-VDD_min)/(VDD_list[1]-VDD_list[0]))
 for element in [TT_VDD,FF_VDD,FS_VDD, SS_VDD, SF_VDD]] 	# determine the index corresponding to assignedVVDD
constructed_data = np.array([raw_data[idx, :, corner_idx] for corner_idx, idx in enumerate(VDD_idx)]).T # construct new dataset

# Translation of original matlab script calculating  overal sigma
Process = np.around(np.array([TK_list*np.log(constructed_data[:, i]).T for i in range(0, constructed_data.shape[1])]).T, decimals=2)
P2 = np.array([np.polyfit(TK_list, Process[:, i], 1)[1] for i in range(0, constructed_data.shape[1])])
P1 = np.array([np.polyfit(TK_list, Process[:, i], 1)[0] for i in range(0, constructed_data.shape[1])])
Meas = np.array([np.divide(P2[i],np.log(constructed_data[:, i])-P1[i]) for i in range(0, constructed_data.shape[1])]).T
error = Meas - np.array(TK_repeat)

#FF = np.array([np.polyfit(TK_list, error[:, i], 3) for i in range(0, constructed_data.shape[1])]).T
FF = np.polyfit(TK_list, error, 3)
error_after_fitting = error - np.polyval(FF, TK_repeat)

std = np.std(error_after_fitting, axis=1)
average = np.mean(error_after_fitting, axis=1) 
overall_sigma = np.max(average+3*std)-np.min(average-3*std)

print(overall_sigma)

# Calculate R2 value
linear_model = LinearRegression()

for i in range(0, constructed_data.shape[1]):
	linear_model.fit(TK_list.reshape(-1, 1), Process[:, i])
	R2.append(linear_model.score(TK_list.reshape(-1, 1), Process[:, i]))

print(R2)
