import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
import csv
import os
import math
import random
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from matplotlib import font_manager
from error3 import error3
from error4 import error4

TK_list = range(273, 328, 5)
#TK_list = range(253, 413, 20)
N_TK = len(TK_list)
random.seed(2)
N_sample = 1100
num_counter = 100
#path = "SIM7.csv"

paths = ["./debug/chip11_27.txt","./debug/chip11_55.txt","./debug/chip11_90.txt"] # debug
def filter_data(raw, filterTK):
	idx = []
	
	for element in filterTK:
		idx.append(TK_list.index(element))

	first = idx[0]
	final = idx[-1]

	new = raw[first*N_sample:final*N_sample]

	return new

def readsingle(path):
	raw_data = []
	TK_real = []
	sum_data = []
	final_data = []

	with open(path) as f:
		spamreader = list(csv.reader(f, delimiter='\t'))	
		for i in range(0, len(spamreader)):		
			raw_data.append(spamreader[i])

	for i in range(0, len(raw_data), N_sample+1):
		TK_real.append(float(raw_data[i][0])+273)

	for i in range(int(N_sample/num_counter), len(raw_data), int(N_sample/num_counter)):
		sum_data.append(raw_data[i][0])

	for i in range(0, int(len(raw_data)/(N_sample+1))):
		a = sum_data[(i*num_counter):((i+1)*num_counter)]
		final_data.append(np.average(np.array(a).astype(np.float)))

	# if (final_data[-1] < final_data[0]):		
	# 	final_data.reverse()
	# 	TK_real.reverse()
	final_data.sort()
	TK_real.sort()
	return [TK_real, final_data]

def quickrsq(data):	
	start = 1
	return np.corrcoef(data[0][start:], np.log(data[1][start:])*data[0][start:])[0][1]

R2 = []
for path in paths:
	R2.append(quickrsq(readsingle(path)))
	print(quickrsq(readsingle(path)))
#np.savetxt("R2fn.csv", R2, delimiter=" ")
p=5
raw_data_multiple = []
N_path = len(paths)
TK_list = range(273, 328, 5)
#TK_list = range(253, 413, 20)
#TK_list = np.array([254.0, 273.0, 294.0, 313.0, 333.0, 353.0, 373.0, 393.0])
N_TK = len(TK_list)
TK_bk = []
for path in paths:
	raw_data_single = readsingle(path)[1]	
	TK_list_tmp = readsingle(path)[0]	
	FRO_fitting_list = np.log(raw_data_single)*TK_list_tmp
	k = np.polyfit(TK_list_tmp, np.log(raw_data_single), 1)[0]
	a = np.polyfit(TK_list_tmp, np.log(raw_data_single), 1)[1]
	FRO_list_new = np.exp(a)*np.exp(k*TK_list)
	#raw_data_multiple.append(FRO_list_new)
	# if (raw_data_single[0] > -10): 
	# 	raw_data_single.insert(0, FRO_list_new[0])	
	# 	TK_list_tmp.insert(0, 253)
	# 	TK_bk.append(TK_list_tmp)
	# elif (raw_data_single[-1] < 108):
	# 	raw_data_single.append(FRO_list_new[-1])	
	# 	TK_list_tmp.append(293)
	# 	TK_bk.append(TK_list_tmp)		
	if len(raw_data_single) == len(TK_list):
		print(path)
		raw_data_multiple.append(raw_data_single)
	if len(TK_list_tmp) == len(TK_list):
		TK_bk.append(TK_list_tmp)

#TK_list = TK_list[0:-1]
raw_data_multiple = np.transpose(np.array(raw_data_multiple))
#print(raw_data_multiple)
a,b = 0,11

raw_data_multiple = raw_data_multiple[a:b, :]
TK_list = TK_list[a:b]
print(TK_bk)

TK_repeat = np.array(np.repeat(TK_list, N_path, axis=0)).reshape((len(TK_list)),N_path)
#TK_repeat = np.transpose(np.array(TK_bk))
#print(TK_repeat)
constructed_data = raw_data_multiple # construct new dataset
#print(TK_repeat.shape)
# Translation of original matlab script calculating  overal sigma
for i in range(0, 6):
	for j in range(i+1,7):
		error, error_after_fitting = error3(TK_list, TK_repeat[a:b,:], constructed_data, a,b, p,f1=i,f2=j,f3=8)
		#print(error)
		#print(error_after_fitting)
		std = np.std(error_after_fitting, axis=1)

		average = np.mean(error_after_fitting, axis=1) 
		overall_sigma = np.max(average+3*std)-np.min(average-3*std)
		#print(i,j,overall_sigma)
# for i in range(0, 11):
# 	error, error_after_fitting = error4(TK_list, TK_repeat[a:b,:], constructed_data, a,b, p,f1=i,f2=i,f3=i)
# 	#print(error)
# 	#print(error_after_fitting)
# 	std = np.std(error_after_fitting, axis=1)

# 	average = np.mean(error_after_fitting, axis=1) 
# 	overall_sigma = np.max(average+3*std)-np.min(average-3*std)
# 	print(i,overall_sigma)

error, error_after_fitting = error3(TK_list, TK_repeat[a:b,:], constructed_data, a,b, p,f1=0,f2=6,f3=7) 
#print(error)
#print(error_after_fitting)
std = np.std(error_after_fitting, axis=1)

average = np.mean(error_after_fitting, axis=1) 
overall_sigma = np.max(average+3*std)-np.min(average-3*std)


np.savetxt("foofn_debug.csv", constructed_data, delimiter=" ")
np.savetxt("TKREAL.csv", TK_bk, delimiter=" ")
np.savetxt("foo1.csv", average+3*std, delimiter=" ")
np.savetxt("foo2.csv", average-3*std, delimiter=" ")

# for i in range(0, error_after_fitting.shape[1]):
# 	np.random.shuffle(error_after_fitting[i])

plt.plot(np.array(TK_list)-273, error_after_fitting, "-")

plt.plot(np.array(TK_list)-273, average+3*std,'r*--');
plt.plot(np.array(TK_list)-273, average-3*std,'r*--');

plt.show()

print(np.max(average+3*std))
print(np.min(average-3*std))
