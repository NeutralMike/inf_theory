#!/usr/bin/python

import os
import argparse
import math


def encode(raw_bin):
    print(len(raw_bin))
    print(type(raw_bin))
    print(list(raw_bin))
    res = b'3\n'
    raw = list(raw_bin)
    for i in range(len(raw_bin)):
        res += bin(raw[-1])
        raw = raw[1:] + raw[:1]
    return res


def decode(coded_bin):
    return coded_bin


def compress(paths, destination):
    destination = destination or os.getcwd()
    for path in paths:
        new_path = os.path.join(destination, path+'.nbf')
        if not os.path.exists(os.path.join(destination, os.path.dirname(path))):
            os.makedirs(os.path.join(destination, os.path.dirname(path)))

        with open(path, 'rb') as input_file, open(new_path, 'wb') as output_file:
            input_data = input_file.read()
            print('H(X): H(input_data)')
            output_file.write(encode(input_data))


def extract(paths, destination):
    destination = destination or os.getcwd()
    for path in paths:
        new_path = os.path.join(destination, path.replace('.nbf', ''))
        if not os.path.exists(os.path.join(destination, os.path.dirname(path))):
            os.makedirs(os.path.join(destination, os.path.dirname(path)))

        with open(path, 'rb') as input_file, open(new_path, 'wb') as output_file:
            output_file.write(decode(input_file.read()))


def get_paths_of_dir(dir_path):
    res = []
    for f in os.listdir(dir_path):
        path = os.path.join(dir_path, f)
        if os.path.isfile(path):
            res.append(path)
        elif os.path.isdir(path):
            res.extend(get_paths_of_dir(path))
    return res


parser = argparse.ArgumentParser(description='This is a Burrows Wheeler algorithm implementation by Mikhail (neutralmike) Diatlov.')
parser.add_argument('-V', '--version', action='version', version='%(prog)s 1.0')
parser.add_argument("-c", "--compress", help="run script in compress mode", action="store_true")
parser.add_argument("-e", "--extract", help="run script in extract mode", action="store_true")
parser.add_argument('-d', '--destination', help="name or path of a new directory with compressed/extracted files", action="store")
parser.add_argument('path', help="path to file or directory", action="store", nargs='+')

args = parser.parse_args()

paths = []
for path in args.path:
    isFile = os.path.isfile(path)
    isDirectory = os.path.isdir(path)

    if isFile:
        paths.append(path)
    elif isDirectory:
        paths.extend(get_paths_of_dir(path))

if args.extract:
    extract(paths, args.destination)
else:
    compress(paths, args.destination)
