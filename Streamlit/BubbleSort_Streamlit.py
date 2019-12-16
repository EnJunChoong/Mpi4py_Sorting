# Python program for implementation of Bubble Sort
import argparse
import random
import time
import os
import pickle

# Construct argument parse and parse arguments
ap = argparse.ArgumentParser()
ap.add_argument("-l", "--length", type = int, default = 100,
                help = "set the length of a random generated list")
ap.add_argument("-t", "--time", type = int, default = 1, choices = [0, 1],
                help = "set status of computing running time, 0 is False, 1 is True, default 1")
ap.add_argument("-p", "--print", type = int, default = 1, choices = [0, 1],
		help = "enable printing of all lists, 0 is False, 1 is True, default 1")

ap.add_argument("-s", "--save", type = str, default = os.getcwd(),
		help = "set directory for saving results")
args = vars(ap.parse_args())

def bubbleSort(data):
    n = len(data)

    # Traverse through all array elements
    for i in range(n):

        # Last i elements are already in place
        for j in range(0, n-i-1):

            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if data[j] > data[j+1] :
                data[j], data[j+1] = data[j+1], data[j]
    return data

# Generate random data
random.seed(123)
data = [random.randint(0, 10000) for i in range(args["length"])]
ResultDict={}
if args["print"] == 1:
	print("\nGenerated list: {}\n".format(data))

# Driver code to test above
tic = time.time()
result = bubbleSort(data)
toc = time.time()

if args["print"] == 1:
    print("Result: {}\n".format(result))

runtime=toc-tic
ResultDict['runtime']=runtime
print("Execution Time: {}\n".format(runtime))

with open(os.path.join(args["save"],'resultDict.pickle'), "wb+") as output_file:
    pickle.dump(ResultDict, output_file)
