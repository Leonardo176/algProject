#!/usr/bin/env python3

from tests.bst import test_insert, test_insert_and_remove, test_rotate


def main():
    test_insert()
    test_insert_and_remove()
    test_rotate()


if __name__ == "__main__":
    main()
