import csv
import math
import time
import matplotlib.pyplot as plt

from concurrent.futures import ProcessPoolExecutor
from random import Random
from statistics import median

from tests.setup_test import *

# Generating plot in .png format and a .csv file in plots/rotations directory
# Recorded data represent the number of rotations for each tree in trees_type, for different numbers of nodes n contained in the tree. For each one 100 insertions and deletions are performed. The final data The final recorded value is the median of the 100 measured execution times
def rotations_plot(n_max: int, *trees_type: TreeType):
    # Enabling parallel execution using multiple processes
    executor = ProcessPoolExecutor(max_workers=3)

    rotations = {}
    futures = {}

    # Values of n (as number of nodes) used in the experiment
    n_values = get_n_values(n_max)

    graph_name = ""
    path = "plots/rotations/"
    end_of_path = ""

    # Created a single plot containing all selected tree types
    plt.figure(figsize=(9, 5))

    # Starting one process for each tree type
    for t in trees_type:
        print(f"\nStarting Rotations test for {t.value}...")

        # Storing in futures matrix all the resulting number of rotations, for each tree type
        futures[t] = executor.submit(_test_rotations, t, n_max, n_values)

    # Sorting trees based on their names
    trees_type = sorted(trees_type, key=lambda tree: tree.value)

    # Waiting all tree's process to finish
    for t in trees_type:
        graph_name += t.value + ", "
        end_of_path += t.value + "_"
        rotations[t] = futures[t].result()

    graph_name = end_of_path.rstrip(", ")
    end_of_path = end_of_path.rstrip("_")
    
    # Exporting data in .csv file, formatting the filename with the current timestamp to avoid overwriting on previous results
    f = open(f"{path}{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())}_{end_of_path}.csv", "w", newline="")
    wr = csv.writer(f)

    #Adding to .csv file the values of n on which the test of rotations was computed
    wr.writerow(["n"] + n_values)

    # Writing the measured number of rotations in the .csv and .png plot
    for t in trees_type:
        # For .csv file
        wr.writerow([t.value] + rotations[t])

        # For plot file
        plt.plot(n_values, rotations[t], marker=".", label=t.value)
        plt.xlabel("Nodes (number)")
        plt.ylabel("Rotations (number)")
        
	# Closing .csv file
    f.close()

    plt.legend()
    plt.title(f"{graph_name}: number of rotations times on 100 insertions")
    plt.grid(True)

    plt.savefig(f"{path}{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())}_{end_of_path}.png")

def _test_rotations(tree_type: TreeType, n_max: int, lista_val_n):
    rng = Random()
    list_rotations = []

    for n in lista_val_n:
        # Displaying progress
        print(f"{tree_type.value}: {n} ({(n-1000)/(n_max-1000)*100:.2f}%)")

        # Creating the correct type of tree
        tree = create_tree(tree_type)

        # Creating values list containing numbers in the range below
        values = list(range(0, n + 10 + round(math.sqrt(n))))
        
        # Shuffling list
        rng.shuffle(values)

        # Inserting first n values in the tree
        for i in range(0, n):
            tree.insert_key(values[i])

        # Creating array to record the measured number of rotations occured
        rotations_counter = []

        # I will perform 100 insertions and deletions in a row to get the number of rotations occured
        for _ in range(100 + round(2 * math.sqrt(n))):
            # Generating index of the element to insert and to remove
            ins = rng.randint(n, len(values) - 1)
            rem = rng.randint(0, n)

            tree.insert_key(values[ins])

            swap(values, n, ins)

			# Saving in the array the number of rotations
            rotations_counter.append(tree.rotations_counter)

            tree.remove_key(values[rem])

            swap(values, rem, n)

		#SCEGLIERE SE MEDIANO O MASSIMO, PRIMA DI INVIARE
		# Adding durations list the maximum number of rotations, out of 100 insertions samples
        rotations_counter.sort()
        list_rotations.append(median(rotations_counter))

    return list_rotations


def swap(arr, i, j):
    value = arr[i]
    arr[i] = arr[j]
    arr[j] = value
