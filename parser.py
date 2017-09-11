def parse_mdm_to_nparray(file_name):
	'''
	   Read data from .mdm files. Output is two dictionaries: 1. Data 2. Header
	   In Data dict, the keys are in string formats. The data are in float format.
	   In Header dict, everything is in string formats.
	'''
	with open(file_name,'r') as f:

		tmp = ''
		tmp = f.readline().split()

		# Ignore the uesless lines
		if len(tmp) == 0 or tmp[0] =='!':
			tmp = f.readline().split()

		# Read header (including inputs and outputs)
		header = []
		inputs = []
		outputs = []
		if (tmp[0] == "BEGIN_HEADER"):
			tmp = f.readline().split()
			while (tmp[0] != "END_HEADER"):
				header.append(tmp)
				tmp = f.readline().split()

		# Separate inputs and outputs
		i = 0
		if (header[i][0] == 'ICCAP_INPUTS'):
			while (header[i][0] != 'ICCAP_OUTPUTS'):
				i = i + 1
				inputs.append(header[i-1])
		if (header[i][0] == 'ICCAP_OUTPUTS'):
			while (i < len(header)):
				outputs.append(header[i])
				i = i+1

		# Read Data
		Condition = []
		Data_tmp = []

		while (1):
			tmp = f.readline().split()
			# Ignore the uesless lines
			if len(tmp) == 0 or tmp[0] =='!':
				tmp = f.readline().split()
				if len(tmp) == 0:
					break
			cond = []
			data = []
			if (tmp[0] == "BEGIN_DB"):
				tmp = f.readline().split()
				while (tmp[0] == "ICCAP_VAR"):
					cond.append(tmp)
					tmp = f.readline().split()
					if len(tmp) ==0:
						tmp = f.readline().split()
				while (tmp[0] != "END_DB"):
					data.append(tmp)
					tmp = f.readline().split()

			# Transfer string to float
			data[1:] = [map(float,e) for e in data[1:]]

			Condition.append(cond)
			Data_tmp.append(data)

		# Construct Data dictionary
		Data = {}

		cond_val_num = len(Condition[0])
		cond_num = len(Condition)
		data_val_num = len(Data_tmp[0][0])
		data_num = len(Data_tmp[0])-1

		store_tmp = []
		data_val_count = 0
		cond_val_count = 0
		# Data
		while (data_val_count < data_val_num):
			data_store_tmp = []
			cond_count = 0
			while (cond_count < cond_num):
				data_count = 0
				while (data_count < data_num):
					data_store_tmp.append(Data_tmp[cond_count][data_count+1][data_val_count])
					data_count = data_count+1
				cond_count = cond_count+1
			data_val_count = data_val_count+1
			store_tmp.append(data_store_tmp)
		# Condition
		while (cond_val_count < cond_val_num):
			cond_store_tmp = []
        		cond_count = 0
			while (cond_count < cond_num):
				data_count = 0
				while (data_count < data_num):
					cond_store_tmp.append(float(Condition[cond_count][cond_val_count][2]))
					data_count = data_count+1
				cond_count = cond_count+1
			cond_val_count = cond_val_count+1
			store_tmp.append(cond_store_tmp)

		# Combine together
		count = 0
		while (count < data_val_num):
			Data[Data_tmp[0][0][count]] = store_tmp[count]
			count = count+1
		while (count < data_val_num+cond_val_num):
			Data[Condition[0][count-data_val_num][1]] = store_tmp[count]
			count = count+1

		# Construct Header dictionary
		Header = {}
		Header['Inputs'] = inputs
		Header['Outputs'] = outputs

		return Header, Data

# @ Xiang: please implement this function by 09/12
def dc_iv_input(file_name):
	header, data = parse_mdm_to_nparray(file_name)
	# assert whether is it DC IV data
	# return three numpy arrays, vg, vd and id
	import numpy as np
	
	assert ('freq' not in data.keys()),'The input data is not dc measurement, abort!'

	if ('#Vd' in data.keys()):
		vd = np.array(data['#Vd'])
		vg = np.array(data['Vg'])
		id = np.array(data['Id'])
	elif ('#vd' in data.keys()):
		vd = np.array(data['#vd'])
		vg = np.array(data['vg'])
		id = np.array(data['id'])
	else:
		raise Exception('Vd not found!')

	return vg, vd, id
	
def ac_s_input(file_name):
    header, data = parse_mdm_to_nparray(file_name)

    import numpy as np

    s11arr = np.array(data["R:s(1,1)"]) + 1j*np.array(data["I:s(1,1)"])
    s12arr = np.array(data["R:s(1,2)"]) + 1j*np.array(data["I:s(1,2)"])
    s21arr = np.array(data["R:s(2,1)"]) + 1j*np.array(data["I:s(2,1)"])
    s22arr = np.array(data["R:s(2,2)"]) + 1j*np.array(data["I:s(2,2)"])
    freq = header["Inputs"][1][3]


    return s11arr,s12arr,s21arr,s22arr,freq

# if __name__ == '__main__':
#     # dict1 = (parse_mdm_to_nparray('./HEMT_bo/s_at_f_vs_Vd.mdm')[1])
#     # print (dict1["R:s(1,1)"])
#     ac_s_input('./HEMT_bo/s_at_f_vs_Vd.mdm')
