# Python Program to implement
# Odd-Even / Brick Sort
import argparse
import random
import time
import os
import pickle


# Construct argument parse and parse arguments
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

def oddEvenSort(data):

    swapped = True
    pass_count = 1
    while(swapped):

        swapped = False

        for i in range(0, len(data) - 1, 2):
            if data[i] > data[i+1]:
                data[i], data[i+1] = data[i+1], data[i]
                swapped = True

        for i in range(1, len(data) - 1, 2):
            if data[i] > data[i+1]:
                data[i], data[i+1] = data[i+1], data[i]
                swapped = True

        pass_count += 1

    return data

# Generate random data
random.seed(123)
data = [random.randint(0, 10000) for i in range(args["length"])]
ResultDict={}
if args["print"] == 1:
	print("\nGenerated list: {}\n".format(data))

# Driver code to test above
tic = time.time()
result = oddEvenSort(data);
toc = time.time()

if args["print"] == 1:
    print("Result: {}\n".format(result))

runtime=toc-tic
ResultDict['runtime']=runtime
print("Execution Time: {}\n".format(runtime))

with open(os.path.join(args["save"],'resultDict.pickle'), "wb+") as output_file:
    pickle.dump(ResultDict, output_file)
