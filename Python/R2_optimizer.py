import pandas as pd
import numpy as np
import csv
import matplotlib.pyplot as plt

#####################################################################
####					  Linearity  Calculation                 ####
#####################################################################

def polyfit(x, y, degree):
    results = {}

    coeffs = np.polyfit(x, y, degree)

     # Polynomial Coefficients
    results['polynomial'] = coeffs.tolist()

    # r-squared
    p = np.poly1d(coeffs)
    # fit values, and mean
    yhat = p(x)                         # or [p(z) for z in x]
    ybar = np.sum(y)/len(y)          # or sum(y)/len(y)
    ssreg = np.sum((y - yhat)**2)   # or sum([ (yihat - ybar)**2 for yihat in yhat])
    sstot = np.sum((y - ybar)**2)    # or sum([ (yi - ybar)**2 for yi in y])
    results['determination'] = 1-ssreg / sstot

    return results['determination']

#####################################################################
####					  Data EXtraction                        ####
#####################################################################

T = np.arange(0+273, 105+273, 5).tolist()
diffW = np.arange(0.5, 10.5, 0.5).tolist()
diffL = np.arange(0.5, 10.5, 0.5).tolist()

raw = []
data = []

with open('newtest.csv', newline='') as csvfile:
	reader = csv.reader(csvfile, delimiter=',')
	for row in reader:
		raw.append(row)

header = raw[0]
raw = raw[1:]


for element in raw:
	data.append(element[1:])

data_post = []
for i in range(0, len(diffW)):
	data_post.append(np.array(data[i]).reshape(len(T), len(diffL)).tolist())

data_post = np.asarray(data_post).astype(np.float)

R2_total = []
for i in range(0, len(diffW)):
	Linearity = []
	
	for j in range(0, len(diffL)):
		Linearity.append(polyfit(T, T*np.log(data_post[i][:, j]), 1))

	R2_total.append(Linearity)

R2_total = np.asarray(R2_total)

max_index = np.unravel_index(np.argmax(R2_total, axis=None), R2_total.shape)
min_index = np.unravel_index(np.argmin(R2_total, axis=None), R2_total.shape)
max_value = R2_total[max_index]
min_value = R2_total[min_index]

dict_W = {k: v for k, v in enumerate(diffW)}
dict_L = {k: v for k, v in enumerate(diffL)}
print(min_index)
print(max_index)
# print(max_value, min_value)
print(dict_W[min_index[1]], dict_L[min_index[0]])
print(dict_W[max_index[1]], dict_L[max_index[0]])
# print(R2_total)

#####################################################################
####					  Heatmap Plot                           ####
#####################################################################
fig, ax = plt.subplots()
im = ax.imshow(R2_total)

# We want to show all ticks...
ax.set_xticks(np.arange(len(diffW)))
ax.set_yticks(np.arange(len(diffL)))
# ... and label them with the respective list entries
ax.set_xticklabels(diffL)
ax.set_yticklabels(diffW)
plt.gca().invert_yaxis()
plt.ylabel("L/u")
plt.xlabel("W/u")

# Rotate the tick labels and set their alignment.
plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
         rotation_mode="anchor")

ax.set_title("R2 vs W/L, max={ma} @ W={wma}, L={lma}; min={mi} @ W={wmi}, L={lmi}".format(ma=max_value, mi=min_value, 
	wma=dict_W[max_index[1]], lma=dict_L[max_index[0]], wmi=dict_W[min_index[1]], lmi=dict_W[min_index[0]]))
fig.tight_layout()
plt.show()
