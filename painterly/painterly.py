"""This module is the main entry to the painterly library.  This library simulates
Chinese style paintings with from distance-based lighting from a custom recursive language"""
from script_traverser import ScriptTraverser


def main():
    script_traverser = ScriptTraverser()
    script_traverser.setup_grammar()


if __name__ == '__main__':
    main()
