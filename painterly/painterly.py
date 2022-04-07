"""This module is the main entry to the painterly library.  This library simulates
Chinese style paintings with from distance-based lighting from a custom recursive language"""

import grammar

OUT_FILE = r'output\output.png'
SCALING_FACTOR = 2
SIZE = (1800, 1200)


def main():
    grammar.setup_grammar()


if __name__ == '__main__':
    main()
