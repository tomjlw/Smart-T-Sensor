import random
import numpy as np
from errorq import errorq
random.seed(1)
def error3(TK_list, TK_repeat, constructed_data, a, b, k=3,f1=2,f2=-2, f3=0):

	# Translation of original matlab script calculating  overal sigma
	Process = np.around(np.array([TK_list*np.log(constructed_data[:, i]).T for i in range(0, constructed_data.shape[1])]).T, decimals=2)
	P2 = np.array([np.polyfit(TK_list, Process[:, i], 1)[1] for i in range(0, constructed_data.shape[1])])
	P1 = np.array([np.polyfit(TK_list, Process[:, i], 1)[0] for i in range(0, constructed_data.shape[1])])
	P2 = np.array([np.polyfit([TK_list[f1], TK_list[f2]], [Process[f1, i], Process[f2, i]], 1)[1] for i in range(0, constructed_data.shape[1])])
	P1 = np.array([np.polyfit([TK_list[f1], TK_list[f2]], [Process[f1, i], Process[f2, i]], 1)[0] for i in range(0, constructed_data.shape[1])])
	# P2 = np.array([np.polyfit([TK_list[f3]], [Process[f3, i]], 1)[1] for i in range(0, constructed_data.shape[1])])
	# P1 = np.array([np.polyfit([TK_list[f3]], [Process[f3, i]], 1)[0] for i in range(0, constructed_data.shape[1])])
	Meas = np.array([np.divide(P2[i],np.log(constructed_data[:, i])-P1[i]) for i in range(0, constructed_data.shape[1])]).T
	error = Meas - np.array(TK_repeat)
	#FF = np.array([np.polyfit(TK_list, error[:, i], 3) for i in range(0, constructed_data.shape[1])]).T
	FF = np.polyfit(TK_list, error, k)
	#FF = [np.polyfit(TK_repeat[:,i], error, k) for i in range(0, TK_repeat.shape[1])]
	#print(TK_repeat[:,0])
	#error_after_fitting = [error - np.polyval(FF[i], TK_repeat[:,i]) for i in range(0, TK_repeat.shape[1])]
	error_after_fitting = (error - np.polyval(FF, TK_repeat))
	# for i in range(0, error_after_fitting.shape[1]):
	# 		error_after_fitting[:, i] += random.uniform(0.001,0.003)
	# 		pass


	return error, error_after_fitting