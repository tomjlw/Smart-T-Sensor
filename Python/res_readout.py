import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
import csv
import math
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from matplotlib import font_manager

resol = 0.1
query_TK = 293
total = 19
total_s = 15
sample = 6
sample_s = 1
ref_clk = 300000

TK_min = 273
TK_max = 373
N_TK = 21
N_TK_new = 21
N_sample = 5

file_name = ("hope.csv")
raw_data = []
SIMULATION = 0
MANUAL = 0

# Change Font to Arial Narrow
font_dirs = ['./']
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)

for font_file in font_files:
		font_manager.fontManager.addfont(font_file)

plt.rcParams['font.size'] = 12
plt.rcParams['font.family'] = 'Arial Narrow'

# Main Part Begins
with open(file_name) as f:
	spamreader = list(csv.reader(f, delimiter='\t'))
	
	for i in range(1, len(spamreader)):
		for j in range(1, len(spamreader[i])):
			if (spamreader[i][j] != ''):					# remove empty list
				raw_data.append(float(spamreader[i][j]))
	
	raw_data = np.array(raw_data).reshape(N_TK, N_sample)	# transform 1d string array into 3d floating matrix 

TK_list = np.linspace(TK_min, TK_max, N_TK)
TK_list_new = np.linspace(TK_min, TK_max, N_TK_new)
FRO_list = raw_data[:,0]
FRO_list = raw_data[:,0]
FRO_fitting_list = np.log(FRO_list)*TK_list
k = np.polyfit(TK_list, np.log(FRO_list), 1)[0]
a = np.polyfit(TK_list, np.log(FRO_list), 1)[1]
FRO_list_new = np.exp(a)*np.exp(k*TK_list_new)
FRO_fitting_list_new = np.log(FRO_list_new)*TK_list_new

# Calculate PSS after fitting the given curve
f1 = 5040
f2 = 5096
PSS = np.log(f1/np.exp(a))/k-np.log(f2/np.exp(a))/k
print("PSS: "+str(round(PSS, 3))+("°C/V"))

#code_list = np.true_divide(FRO_fitting_list/TK_list,resol)
#T_conv_list = np.true_divide(code_list, FRO_list)

#print(FRO_list)
#print(code_list)

if (MANUAL):
	FRO_list_new = 0.05*np.exp(TK_list*0.043)

############################## Resolution v.s # Total #############################################################
res_total = []
kk = []
cycle_total = []
range_total = []
for ttl in range(total_s, (total+1)):
	res_readout_list_row = []
	cycle_row = []
	for idx, rofreq in enumerate(FRO_list_new):
		MSB_flag = 0
		stop_MSB = -1

		sample_time = np.true_divide(sample, rofreq) # time taken to wait for #sample cycle from CNT1 
		stop = np.binary_repr(int(sample_time * ref_clk), width=32) # cycles CNT2 passed when CNT1 passes #sample cycles

		for index in range(0, len(list(stop))):
			if (MSB_flag == 0):
				if (list(stop)[index]=="1"):
					MSB_flag = 1
					stop_MSB = len(list(stop)) - 1 -index

		stop_final = ttl - stop_MSB - 1 # faster OSC, smaller sample_time, smaller MSB(stop1), larger stop_final(stop2) -> better resol
		#print(stop_MSB, stop_final)
		# if (not SIMULATION and stop_final > 18):
		# 	stop_final = 18
		stop_final_cycle = np.power(2, stop_final)
		kk.append(stop_final_cycle)
		stop_final_time = np.true_divide(stop_final_cycle,rofreq)

		res_readout = FRO_list_new[idx]/(TK_list_new[idx]*stop_final_cycle) #TEST
		#res_readout = TK_list_new[idx]/stop_final_cycle #TEST
	
		res_readout_list_row.append(res_readout)
		cycle_row.append(stop_final_cycle)
		#print(stop_final_cycle, np.true_divide(rofreq, stop_final_cycle))
		#print(stop_final_cycle, FRO_fitting_list[idx]/(TK_list[idx]*res_readout))

	res_total.append(res_readout_list_row)
	cycle_total.append(cycle_row)
	
res_total = np.asarray(res_total)
cycle_total = np.asarray(cycle_total)
print(cycle_total)
#print(cycl_total)
# for i in range(0, 5, 1):
# 	res_tmp = 1/np.power(10,i)
# 	code_tmp = np.true_divide(FRO_fitting_list/TK_list,res_tmp)
# 	T_conv_tmp = np.true_divide(code_tmp, FRO_list)

fig = plt.figure()
ax = plt.subplot(2,2,1)
for colidx in range(0, N_TK_new):
	plt.plot(np.arange(total_s, (total+1)), res_total[:, colidx], "o-", label=str(TK_list_new[colidx]))	
plt.xticks(range(total_s,(total+1)), rotation=45)
plt.xlabel("# Total")
plt.ylabel("Resolution")
plt.yscale("log")
#plt.legend(loc="upper right")
plt.title("Resolution vs #Total @ #Sample= "+str(sample))
plt.tight_layout()
plt.grid()
#plt.show()
with open('ressim.txt', 'w') as f:	      
    # using csv.writer method from CSV package
    write = csv.writer(f)      
    write.writerows(res_total)

#fig = plt.figure()
ax =  plt.subplot(2,2,2)
for colidx in range(0, (total-total_s+1)):
	plt.plot(TK_list_new, res_total[colidx, :], "o-", label=str(colidx+total_s))
	#plt.plot(TK_list_new[1:], np.diff(TK_list_new)/np.diff(cycle_total[colidx, :],1), "o-", label=str(colidx+total_s))

#plt.xticks(TK_list_new, rotation=45)

# Remove repetitive legend
handles, labels = plt.gca().get_legend_handles_labels()
newLabels, newHandles = [], []
for handle, label in zip(handles, labels):
  if label not in newLabels:
    newLabels.append(label)
    newHandles.append(handle)

plt.xlabel("TK")
plt.ylabel("Resolution")
plt.yscale("log")
#plt.legend(loc="upper right")
plt.title("Resolution vs TK for #Total @ #Sample= "+str(sample))
plt.tight_layout()
plt.grid()


#fig = plt.figure()
ax = plt.subplot(2,2,3)
for colidx in range(0, (total-total_s+1)):
	range_row = []

	index = np.argmax(res_total[colidx, :])
	plt.plot(TK_list_new[index], res_total[colidx, :][index], "o", label=str(colidx+total_s))

	for idx in range(0, len(res_total[colidx, :])-1):	
		if (res_total[colidx, idx]>res_total[colidx, idx+1]):
			range_row.append(float(TK_list_new[idx]))
	
	range_total.append(range_row)

# Remove repetitive legend
handles, labels = plt.gca().get_legend_handles_labels()
newLabels, newHandles = [], []
for handle, label in zip(handles, labels):
  if label not in newLabels:
    newLabels.append(label)
    newHandles.append(handle)
range_total = np.asarray(range_total)
range_total_copy = np.empty([np.shape(range_total)[0], np.shape(range_total)[1]+2])

#plt.xticks(TK_list_new, rotation=45)
plt.xlabel("TK")
plt.ylabel("Resolution")
plt.yscale("log")
#plt.legend(loc="upper right")
plt.title("Worst Case TK & Res for #Total @ #Sample= "+str(sample))
plt.tight_layout()
plt.grid()

#fig = plt.figure()
ax = plt.subplot(2,2,4)
for colidx in range(0, (total-total_s+1)):
	tmp_list = range_total[colidx, :].tolist()
	tmp_list.append(TK_list_new[-1])
	tmp_list.insert(0, TK_list_new[0])
	range_total_copy[colidx, :] = np.array(tmp_list)
	plt.plot(range_total_copy[colidx, :],np.repeat(colidx, len(tmp_list)),"o-", label=str(colidx+total_s))

# Remove repetitive legend
handles, labels = plt.gca().get_legend_handles_labels()
newLabels, newHandles = [], []
for handle, label in zip(handles, labels):
  if label not in newLabels:
    newLabels.append(label)
    newHandles.append(handle)

plt.xlabel("TK")
plt.ylabel("# Total")
plt.xticks(range_total_copy[0, :])
#plt.legend(loc="upper right")
plt.title("Range for #Total @ #Sample= "+str(sample))#+"\n Ranges: "+str(range_total_copy[0, :]))
plt.grid()
plt.tight_layout()
plt.show()
