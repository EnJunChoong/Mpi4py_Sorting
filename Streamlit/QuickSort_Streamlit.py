# Python program for implementation of Quicksort Sort
import argparse
import random
import time
import os
import pickle


# Construct argument parse and parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-l", "--length", type = int, default = 1000,
                help = "set the length of a random generated list")
ap.add_argument("-t", "--time", type = int, default = 1, choices = [0, 1],
                help = "set status of computing running time, 0 is False, 1 is True, default 1")
ap.add_argument("-p", "--print", type = int, default = 1, choices = [0, 1],
		help = "enable printing of all lists, 0 is False, 1 is True, default 1")

ap.add_argument("-s", "--save", type = str, default = os.getcwd(),
		help = "set directory for saving results")
args = vars(ap.parse_args())

# This function takes last element as pivot, places
# the pivot element at its correct position in sorted
# array, and places all smaller (smaller than pivot)
# to left of pivot and all greater elements to right
# of pivot
def partition(data,low,high):
	i = ( low-1 )		 # index of smaller element
	pivot = data[high]	 # pivot

	for j in range(low , high):

		# If current element is smaller than or
		# equal to pivot
		if data[j] <= pivot:

			# increment index of smaller element
			i = i+1
			data[i],data[j] = data[j],data[i]

	data[i+1],data[high] = data[high],data[i+1]
	return ( i+1 )

# The main function that implements QuickSort
# data[] --> Array to be sorted,
# low --> Starting index,
# high --> Ending index

# Function to do Quick sort
def quickSort(data,low,high):
    if low < high:

        # pi is partitioning index, arr[p] is now
        # at right place
        pi = partition(data,low,high)

        # Separately sort elements before
        # partition and after partition
        quickSort(data, low, pi-1)
        quickSort(data, pi+1, high)
        return data

# Generate random data
random.seed(123)
data = [random.randint(0, 10000) for i in range(args["length"])]
ResultDict={}
if args["print"] == 1:
	print("\nGenerated list: {}\n".format(data))

# Driver code to test above
tic = time.time()
n = len(data)
result = quickSort(data, 0, n-1)
toc = time.time()

if args["print"] == 1:
    print("Result: {}\n".format(result))

runtime=toc-tic
ResultDict['runtime']=runtime
print("Execution Time: {}\n".format(runtime))

with open(os.path.join(args["save"],'resultDict.pickle'), "wb+") as output_file:
    pickle.dump(ResultDict, output_file)
