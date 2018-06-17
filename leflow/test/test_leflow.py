#Running tests on myAdd  myDense  myMaxpool  myMaxpoolPartition  myPow  mySoftmax  myVecMul
import subprocess
import os
import time

start_time = time.time()

test_folders = ['myAdd', 'myDense', 'myMaxpool', 'myMaxpoolPartition', 'myPow', 'mySoftmax', 'myVecMul']

test_dir = os.getcwd() 

for folder in test_folders:
	errors = 0
	print("\nRunning test for {}".format(folder))

	os.chdir("./{}/".format(folder))

	#start leflow
	command = "../../src/LeFlow {}.py".format(folder, folder)
	leflow_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
	leflow_output = leflow_process.communicate()

	leflow_output = leflow_output[0].splitlines()
	for line in leflow_output:
		if "DONE" in line:
			print("Finished testing LeFlow for {}".format(folder)) 

	#start modelsim
	command = "make v -C {}_files".format(folder)
	modelsim_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=None, shell=True)
	modelsim_output = modelsim_process.communicate()

	modelsim_output = modelsim_output[0].splitlines()
	for line in modelsim_output:
		if "Cycles" in line:
			cycles = line.split()[-1]
			print("Clock cycles required: {}".format(cycles))
			print("Finished testing Modelsim for {}".format(folder))

	os.chdir(test_dir)
	

end_time = time.time()
total_time = end_time - start_time
print("Testing was done in {} seconds".format(round(total_time, 2)))
			
