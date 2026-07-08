#!/usr/bin/env python3

import argparse

from tests.setup_test import TreeType
from tests.test_insertions import insertion_plot
from tests.test_rotations import rotations_plot
from tests.test_heights import heights_plot


def main():
    # Creating the command-line argument parser
    parser = argparse.ArgumentParser()
    
	# Arguments for the type of tests to execute
    parser.add_argument("--plot", nargs="+", choices=["insertions", "rotations", "heights"], default=["insertions", "rotations", "heights"], help="What graph(s) to plot")
    
	# Arguments for the type of trees to use
    parser.add_argument("--trees", nargs="+", choices=["AVL", "BST", "RBT"], default=["AVL", "BST", "RBT"], help="What tree(s) to plot")
    
	# Arguments for the maximum number of nodes to handle
    parser.add_argument("-n", type=int, default=1000000, help="Maximum number of nodes")
    
    args = parser.parse_args()
    
	# Ensuring number of nodes is valid
    if args.n < 1000:
        parser.error("n has to be greater than 1000 ")

	# Creating correct types of trees based on the arguments passed
    trees = [TreeType(t) for t in args.trees]

	# Creating the selected plots executing the corresponding tests
    if "insertions" in args.plot:
        insertion_plot(args.n, *trees)
    if "rotations" in args.plot:
        rotations_plot(args.n, *trees)
    if "heights" in args.plot:
        heights_plot(args.n, *trees)

if __name__ == "__main__":
    main()