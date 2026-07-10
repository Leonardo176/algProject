#!/bin/python3

# Corso di Algoritmi e Strutture Dati - Università degli Studi di Udine - A.A 2025-26
# Progetto di Sebastiano Babich (172249), Leonardo Mazzon (172587) e Damiano Netto (171948)

import numpy as np
import matplotlib.pyplot as plt
import argparse
import os
import sys

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csvpath", required=True)
    args = parser.parse_args()

    if not os.path.exists(args.csvpath):
        sys.stderr.write("[ERROR] file not found\n")
        sys.exit(-1)

    data = np.genfromtxt(args.csvpath,delimiter=",")

    # codomain
    n = data[0,1:]
    avl = data[1,1:]
    bst = data[2,1:]
    rbt = data[3,1:]

    c = [0]*3
    b = [0]*3

    # plot the trees
    c[0],b[0] = np.polyfit(np.log(n),avl,1)
    c[1],b[1] = np.polyfit(np.log(n),bst,1)
    c[2],b[2] = np.polyfit(np.log(n),rbt,1)

    # dump the result to stdout
    sys.stdout.write(f"AVL\nf(n) = {c[0]} log(n) + {b[0]}\n")
    sys.stdout.write(f"BST\nf(n) = {c[1]} log(n) + {b[1]}\n")
    sys.stdout.write(f"RBT\nf(n) = {c[2]} log(n) + {b[2]}\n")

    # dump csv data and log regression
    plt.xlabel("Nodes (number)")
    plt.ylabel("Rotations (number)")
    plt.xscale("log")
    plt.plot(n, avl, marker=".", label="AVL")
    plt.plot(n, bst, marker=".", label="BST")
    plt.plot(n, rbt, marker=".", label="RBT")
    plt.plot(n, c[0]*np.log(n)+b[0], color="blue", label="AVL regression")
    plt.plot(n, c[1]*np.log(n)+b[1], color="green", label="BST regression")
    plt.plot(n, c[2]*np.log(n)+b[2], color="red", label="RBT regression")
    plt.legend()
    plt.savefig("fit_check.png")
    pass

if __name__ == "__main__":
    main()
    pass

