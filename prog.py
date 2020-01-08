#!/usr/bin/env python2
# This file is part of unix_intro (github.com/U8NWXD/unix_intro.git),
# which is distributed under the terms in the LICENSE.txt file in the
# root folder of the project.
# Copyright (c) 2020 U8N WXD (github.com/U8NWXD) <cs.temporary@icloud.com>

# TODO: Add huge comment


import argparse
from datetime import timedelta
import filecmp
import os
import time


def handler_edited(args):
    mod_timestamp = os.path.getmtime(args.file)
    now = time.time()
    delta = timedelta(seconds=now - mod_timestamp)
    print(delta)


def handler_diff(args):
    same = filecmp.cmp(args.file1, args.file2)
    print(same)


def main():
    parser = argparse.ArgumentParser(
        description="A program to help you experiment with some UNIX commands"
    )
    subparsers = parser.add_subparsers()

    parser_edited = subparsers.add_parser(
        "edited", description="Find how long ago a file was modified")
    parser_edited.set_defaults(func=handler_edited)
    parser_edited.add_argument("file", type=str, action="store")

    parser_edited = subparsers.add_parser(
        "diff", description="Find whether 2 files are the same")
    parser_edited.set_defaults(func=handler_diff)
    parser_edited.add_argument("file1", type=str, action="store")
    parser_edited.add_argument("file2", type=str, action="store")


    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
