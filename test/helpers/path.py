import glob, sys
from os.path import join


def path(args):
    return join(*args)


def paths(args, exclude=[]):
    return filter(lambda p: p not in exclude, glob.glob(join(*args)))
