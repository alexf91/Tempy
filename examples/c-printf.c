<<<
import argparse

name = 'printf'
description = 'Print an argument passed during file creation'

parser = argparse.ArgumentParser()
parser.add_argument('message', type=str, default='Hello World')
>>>
#include <stdio.h>

int main(int argc, char **argv) {
    printf("${message}");
    return 0;
}
