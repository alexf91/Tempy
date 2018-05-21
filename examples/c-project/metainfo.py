import argparse

name = 'c-project'
description = 'C project with Makefile'
parser = argparse.ArgumentParser()
parser.add_argument('--name', '-n', default='foo')
parser.add_argument('--license', '-l', choices=('MIT', 'GPL'),
        help='license header for the file')
