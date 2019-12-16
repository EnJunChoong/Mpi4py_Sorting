# Python program for implementation of Insertion Sort
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

# Function to do insertion sort
def insertionSort(data):

    # Traverse through 1 to len(data)
    for i in range(1, len(data)):
        key = data[i]
        # Move elements of data[0..i-1], that are
        # greater than key, to one position ahead
        # of their current position
        j = i-1
        while j >=0 and key < data[j] :
            data[j+1] = data[j]
            j -= 1
        data[j+1] = key

    return data

# Generate random data
random.seed(123)
data = [random.randint(0, 10000) for i in range(args["length"])]
ResultDict={}
if args["print"] == 1:
	print("\nGenerated list: {}\n".format(data))

# Driver code to test above
tic = time.time()
result = insertionSort(data)
toc = time.time()

if args["print"] == 1:
    print("Result: {}\n".format(result))

runtime=toc-tic
ResultDict['runtime']=runtime
print("Execution Time: {}\n".format(runtime))

with open(os.path.join(args["save"],'resultDict.pickle'), "wb+") as output_file:
    pickle.dump(ResultDict, output_file)
