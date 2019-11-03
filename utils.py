#!/usr/bin/env python3


import pathlib
import time


def touch(filename):
    """ Creates a file with filename. """
    pathlib.Path(filename).touch()

def block(filename):
    """ Blocks program execution while file exist. """
    p = pathlib.Path(filename)
    while p.exists():
        time.sleep(1)

def read_index(filename):
    """ Reads index and returns 2 lists ([names], [images]). """
    with open(filename, 'r') as f:
        data = [line.rstrip().split(',') for line in f.readlines()]
    names, images = [], []
    for name, image in data:
        names.append(name)
        images.append(image)
    return names, images

