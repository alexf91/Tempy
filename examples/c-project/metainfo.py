import argparse

description = 'C project with Makefile'
parser = argparse.ArgumentParser()
parser.add_argument('--name', '-n', help='name of the *.c file', default='foo')
