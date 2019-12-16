# Python program for implementation of Selection
# Sort
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

def sequential(data):
    # Traverse through all array elements
    for i in range(len(data)):

        # Find the minimum element in remaining
        # unsorted array
        min_idx = i
        for j in range(i+1, len(data)):
            if data[min_idx] > data[j]:
                min_idx = j

        # Swap the found minimum element with
        # the first element
        data[i], data[min_idx] = data[min_idx], data[i]

    return data

# Generate random data
random.seed(123)
data = [random.randint(0, 10000) for i in range(args["length"])]
ResultDict={}
if args["print"] == 1:
	print("\nGenerated list: {}\n".format(data))

# Driver code to test above
tic = time.time()
result = sequential(data)
toc = time.time()

if args["print"] == 1:
    print("Result: {}\n".format(result))


runtime=toc-tic
ResultDict['runtime']=runtime
print("Execution Time: {}\n".format(runtime))

with open(os.path.join(args["save"],'resultDict.pickle'), "wb+") as output_file:
    pickle.dump(ResultDict, output_file)
