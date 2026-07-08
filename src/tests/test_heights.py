import csv
import math
import time
import matplotlib.pyplot as plt

from concurrent.futures import ProcessPoolExecutor
from random import Random
from statistics import median

from tests.setup_test import *


# Generating plot in .png format and a .csv file in plots/heights directory
# Recorded data represent the maximum height reached for each tree in trees_type for different numbers of nodes n. For each one 100 insertions and deletions are performed

def heights_plot(n_max: int, *trees_type: TreeType):
    # Enabling parallel execution using multiple processes
    executor = ProcessPoolExecutor(max_workers=3)

    heights = {}
    futures = {}

    # Values of n (as number of nodes) used in the experiment
    n_values = get_n_values(n_max)

    graph_name = ""
    path = "plots/heights/"
    end_of_path = ""

    # Created a single plot containing all selected tree types
    plt.figure(figsize=(9, 5))

    # Starting one process for each tree type
    for t in trees_type:
        print(f"\nStarting Heights test for {t.value}...")

        # Storing in futures matrix all the resulting heights computations, for each tree type
        futures[t] = executor.submit(_test_heights, t, n_max, n_values)

    # Sorting trees based on their names
    trees_type = sorted(trees_type, key=lambda tree: tree.value)

    # Waiting all tree's process to finish
    for t in trees_type:
        graph_name += t.value + ", "
        end_of_path += t.value + "_"
        heights[t] = futures[t].result()

    graph_name = end_of_path.rstrip(", ")
    end_of_path = end_of_path.rstrip("_")
    
    # Exporting data in .csv file, formatting the filename with the current timestamp to avoid overwriting on previous results
    f = open(f"{path}{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())}_{end_of_path}.csv", "w", newline="")
    wr = csv.writer(f)

    #Adding to .csv file the values of n on which the test of heights was computed
    wr.writerow(["n"] + n_values)

    # Writing the measured heights in the .csv and .png plot
    for t in trees_type:
        # For .csv file
        wr.writerow([t.value] + heights[t])

        # For plot file
        plt.plot(n_values, heights[t], marker=".", label=t.value)
        plt.xlabel("Nodes (number)")
        plt.ylabel("Heights (number)")

    # Closing .csv file
    f.close()
    
    # Adding the height bounds for comparison with the experimental data
    log2_values = [math.log2(n) for n in n_values]

    # Lower bound for the height of any binary tree
    plt.plot(n_values, log2_values, label="Binary tree lower bound", color="black", linestyle=":", linewidth=2)

    # Upper bound for the height of AVL trees
    if TreeType.AVL in trees_type:        
        plt.plot(n_values, [x * 1.44 for x in log2_values], label="AVL upper bound", color="blue", linestyle=":", linewidth=2)

    # Upper bound for the height of RBT trees
    if TreeType.RBT in trees_type:        
        plt.plot(n_values, [x * 2 for x in log2_values], label="RBT upper bound", color="red", linestyle=":", linewidth=2) #In realtà doveva essere 2*log2(n+1), non con parametro n e basta

    plt.legend()
    plt.title(f"{graph_name}: maximum height reached on 100 insertions and deletions")
    plt.grid(True)

    # Exporting plot file as .png
    plt.savefig(f"{path}{time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime())}_{end_of_path}.png")

def _test_heights(tree_type: TreeType, n_max: int, n_values):
    rng = Random()
    list_heights = []

    for n in n_values:
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

        # Creating array to record the height reached by the tree after each insertion
        heights_reached = []

        # I will perform 100 insertions and deletions in a row
        for _ in range(100):
            # Generating index of the element to insert and to remove
            ins = rng.randint(n, len(values) - 1)
            rem = rng.randint(0, n)

            tree.insert_key(values[ins])

            # Saving in the array che height reached
            heights_reached.append(height_ric(tree.root))

            swap(values, n, ins)
            tree.remove_key(values[rem])
            swap(values, rem, n)

        # Adding to all the heights the maximum height reached in all 100 insertions
        list_heights.append(max(heights_reached))

    return list_heights


def swap(arr, i, j):
    value = arr[i]
    arr[i] = arr[j]
    arr[j] = value
