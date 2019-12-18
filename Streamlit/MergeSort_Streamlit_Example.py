from mpi4py import MPI
import argparse
import os
import time
import pickle
import random
# merge sort algorithm
def mergeSort(L):
	if len(L) < 2:
		return L[:]
	else:
		middle = int(len(L)/2)
		left = mergeSort(L[:middle])
		right = mergeSort(L[middle:])
		return merge(left, right)

def merge(left, right):
	result = []
	i, j = 0, 0
	while i < len(left) and j < len(right):
		if left[i] < right[j]:
			result.append(left[i])
			i += 1
		else:
			result.append(right[j])
			j += 1
	while (i < len(left)):
		result.append(left[i])
		i += 1
	while (j < len(right)):
		result.append(right[j])
		j += 1
	return result

# construct argument parse and parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-l", "--length", type = int, default = 30,
                help = "set the length of a random generated list")
ap.add_argument("-t", "--time", type = int, default = 1, choices = [0, 1],
                help = "set status of computing running time, 0 is False, 1 is True, default 1")
ap.add_argument("-p", "--print", type = int, default = 1, choices = [0, 1],
		help = "enable printing of all lists, 0 is False, 1 is True, default 1")

ap.add_argument("-s", "--save", type = str, default = os.getcwd(),
		help = "set directory for saving results")
args = vars(ap.parse_args())

# implementation of distributed merge sort
comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size
name = comm.Get_processor_name()
ResultDict={}

if size >1:
	if rank == 0:
		# generate data in node 0
		random.seed(123)
		data = [random.randint(0, 10000) for i in range(args["length"])]
		tic = time.time()
		partitions=len(data)//size
		p_data=data[:partitions]
		ResultDict['data']=data
		ResultDict['data_part1']=p_data
		if args["print"] == 1:
			print(f"{args["length"]} random numbers generated...\n")
			print(f"Partition #1 of {args["size"]} assigned to {name}...\n")


		for i in range(1,size):
			if i == size-1:
				comm.send(data[partitions*i:], dest = i)
				ResultDict[f'data_part{i+1}']=data[partitions*i:]
			else:
				comm.send(data[partitions*i:partitions*(i+1)], dest = i)
				ResultDict[f'data_part{i+1}']=data[partitions*i:partitions*(i+1)]
		# if args["print"] == 1:
		# 	print("first partition: {}\n".format(p_data))

	for i in range(1, size):
	    if rank == i:
	    	p_data = comm.recv(source = 0)
	    	if args["print"] == 1:
				print(f"Partition #{i} of {args["size"]} assigned to {name}...\n")
	    		# print("Received partition at node {}: {}\n".format(rank, p_data))

	p_data = mergeSort(p_data)


	if args["print"] == 1:
		print(f"Partition #{rank+1} of {args["size"]} finished sorted at {name}, send back to Master...\n")
		# print("Sorted data at {}: {}\n".format(rank, p_data))

	c_data = comm.gather(p_data, root = 0)

	if rank == 0:
		final = c_data[0]
		ResultDict['sorted_data_part1']=c_data[0]
		for i in range(1,size):
			final = merge(final, c_data[i])
			ResultDict[f'sorted_data_part{i+1}']=c_data[i]
		if args["print"] == 1:
			print(f"Merge of {size} partitionsand final sorting completed at {name}...\n")

		ResultDict['sorted_data_merged']=final
		toc = time.time()
		runtime=toc-tic
		ResultDict['runtime']=runtime
		# if args["print"] == 1:
		# 	print("Final: {}\n".format(final))

		# if args["time"] == 1:
		# 	print("running time is {}s\n".format(runtime))


		with open(os.path.join(args["save"],'resultDict.pickle'), "wb+") as output_file:
			pickle.dump(ResultDict, output_file)
else:
	if rank == 0:
		data = [random.randint(0, 10000) for i in range(args["length"])]

		if args["print"] == 1:
			print(f"{args["length"]} random numbers generated...\n")
			print(f"Partition #1 of {args["size"]} assigned to {name}...\n")
		ResultDict['data']=data
		tic = time.time()
		p_data = data[:]
		final = mergeSort(p_data)
		ResultDict['sorted_data']=final
		toc = time.time()
		runtime=toc-tic
		
		if args["print"] == 1:
			print(f"Final sorting completed at {name}...\n")
		ResultDict['runtime']=runtime
		# if args["print"] == 1:
		# 	print("Final: {}\n".format(final))
		# if args["time"] == 1:
		# 	print("running time is {}s\n".format(runtime))

		with open(os.path.join(args["save"],'resultDict.pickle'), "wb+") as output_file:
			pickle.dump(ResultDict, output_file)
