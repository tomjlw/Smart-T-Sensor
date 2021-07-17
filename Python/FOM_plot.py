import numpy as np 
import matplotlib.pyplot as plt
import pandas as pd 
import csv
import math
from adjustText import adjust_text
pd.set_option("display.max_rows", None, "display.max_columns", None)

path ='TSensor_survey.xlsx'
shape_color_map = {"BJT":"or", "Resistor":"^g", "MOS":"sb", "TD":"Dc", "MEMS":"Pm"} # "shape,color"
filterdict = {"Acc": 10, "Res": 1e9, "Pow": 1e9, "Ene": 1e9, "Yea": 1000}
annotation = 1
Y_total = []
X_total = []
pd_total = []

# Merge all data in Tsensor_survey.xlsx by Makinwwa 
all_sheet = pd.ExcelFile(path)
related_sheet = [all_sheet.sheet_names[i] for i in range(1, 5)]
raw_data_pd = pd.concat([pd.read_excel(path, sheet_name=related_sheet[i]).dropna(subset=['Type']) 
	for i in range(0, 4)], join="inner", ignore_index=1) # drop empty rows

# Categorize Sensors
raw_data_pd.loc[raw_data_pd['Type'].str.contains("NPN"),'Type'] = 'BJT'
raw_data_pd.loc[raw_data_pd['Type'].str.contains("PNP"),'Type'] = 'BJT'
raw_data_pd.loc[raw_data_pd['Type'].str.contains("Diode"),'Type'] = 'BJT'
raw_data_pd.loc[raw_data_pd['Type'].str.contains("Hybrid"),'Type'] = 'BJT'
raw_data_pd.loc[raw_data_pd['Type'].str.contains("TD"),'Type'] = 'TD'
raw_data_pd.loc[raw_data_pd['Type'].str.contains("MEMS"),'Type'] = 'TD'
raw_data_pd.loc[raw_data_pd['Type'].str.contains("MOS"),'Type'] = 'MOS'
raw_data_pd.loc[raw_data_pd['Type'].str.contains("RC"),'Type'] = 'Resistor'
raw_data_pd.loc[raw_data_pd['Type'].str.contains("RR"),'Type'] = 'Resistor'
raw_data_pd.loc[raw_data_pd['Type'].str.contains("WB"),'Type'] = 'Resistor'
raw_data_pd.loc[raw_data_pd['Type'].str.contains("WhB"),'Type'] = 'Resistor'
raw_data_pd.loc[raw_data_pd['Type'].str.contains("PF"),'Type'] = 'Resistor'

# Customize Filter 
raw_data_pd = raw_data_pd[raw_data_pd['Year'] > filterdict["Yea"]] # filter by year
raw_data_pd = raw_data_pd[raw_data_pd['uW'] < filterdict["Pow"]] # filter by power
raw_data_pd = raw_data_pd[raw_data_pd['nJ'] < filterdict["Ene"]] # filter by Eneregy/conversion
raw_data_pd = raw_data_pd[raw_data_pd['PP IA [°C]'] < filterdict["Acc"]] # filter by Accuracy
raw_data_pd = raw_data_pd[raw_data_pd['Res [mK]'] < filterdict["Res"]] # filter by resolution

# Construct new categorize for reference
reference_list = []

for i in range(0, len(raw_data_pd['Source'].tolist())):
	reference_list.append(raw_data_pd['Author'].tolist()[i].split(". ")[-1] + "\n" + raw_data_pd['Source'].tolist()[i]+ " '" + str(raw_data_pd['Year'].tolist()[i])[2:-2])

raw_data_pd["Reference"] = reference_list

#plt.figure()
ax = plt.subplot(3,1,1)
YSPEC = "PP IA [°C]"
XSPEC = "nJ"
adjust = []
Y = raw_data_pd[YSPEC].tolist()
X = raw_data_pd[XSPEC].tolist()
for i in range(0, len(X)):
	style = shape_color_map[raw_data_pd["Type"].tolist()[i]]
	if (annotation):
		plt.text(X[i], Y[i], raw_data_pd["Reference"].tolist()[i])
	plt.plot(X[i],Y[i], style, label=raw_data_pd["Type"].tolist()[i])

# Remove repetitive legend
handles, labels = plt.gca().get_legend_handles_labels()
newLabels, newHandles = [], []
for handle, label in zip(handles, labels):
  if label not in newLabels:
    newLabels.append(label)
    newHandles.append(handle)

plt.xscale("log")
plt.xticks(np.logspace(-3.0, 8.0, num=12))
plt.yticks(np.arange(0, 10, 0.8))
plt.ylabel("Accuracy [°C]")
plt.xlabel("Energy [nJ]")
plt.legend(newHandles, newLabels, loc="upper right")
plt.grid()
plt.tight_layout()

ax = plt.subplot(3,1,2)
YSPEC = "PP IA [°C]"
XSPEC = "uW"
Y = raw_data_pd[YSPEC].tolist()
X = raw_data_pd[XSPEC].tolist()
for i in range(0, len(X)):
	style = shape_color_map[raw_data_pd["Type"].tolist()[i]]
	if (annotation):
		plt.text(X[i], Y[i], raw_data_pd["Reference"].tolist()[i])
	plt.plot(X[i],Y[i], style, label=raw_data_pd["Type"].tolist()[i])

# Remove repetitive legend
handles, labels = plt.gca().get_legend_handles_labels()
newLabels, newHandles = [], []
for handle, label in zip(handles, labels):
  if label not in newLabels:
    newLabels.append(label)
    newHandles.append(handle)

plt.xscale("log")
plt.xticks(np.logspace(-3.0, 4.0, num=8))
plt.yticks(np.arange(0, 10, 0.8))
plt.ylabel("Accuracy [°C]")
plt.xlabel("Power [uW]")
plt.legend(newHandles, newLabels, loc="upper right")
plt.grid()
plt.tight_layout()

ax = plt.subplot(3,1,3)
YSPEC = "Res [mK]"
XSPEC = "uW"
Y = raw_data_pd[YSPEC].tolist()
X = raw_data_pd[XSPEC].tolist()
for i in range(0, len(X)):
	style = shape_color_map[raw_data_pd["Type"].tolist()[i]]
	if (annotation):
		plt.text(X[i], Y[i], raw_data_pd["Reference"].tolist()[i])
	plt.plot(X[i],Y[i], style, label=raw_data_pd["Type"].tolist()[i])

# Remove repetitive legend
handles, labels = plt.gca().get_legend_handles_labels()
newLabels, newHandles = [], []
for handle, label in zip(handles, labels):
	if label not in newLabels:
		newLabels.append(label)
		newHandles.append(handle)

plt.xscale("log")
plt.xticks(np.logspace(-3.0, 5.0, num=9))
#plt.yticks(np.arange(0, 10, 0.4))
plt.ylabel("Resolution [mK]")
#plt.ylim(top=10000)
plt.yscale("log")
plt.yticks(np.logspace(-2.0, 4.0, num=7))
plt.xlabel("Power [uW]")
plt.legend(newHandles, newLabels, loc="upper right")
plt.grid()
plt.tight_layout()
plt.show()