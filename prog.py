#!/usr/bin/env python2
# This file is part of unix_intro (github.com/U8NWXD/unix_intro),
# which is distributed under the terms in the LICENSE.txt file in the
# root folder of the project.
# Copyright (c) 2020 U8N WXD (github.com/U8NWXD) <cs.temporary@icloud.com>

# TODO: Add huge comment


from __future__ import print_function

import argparse
from datetime import timedelta
import filecmp
import os
from random import SystemRandom
import sys
import time


DISABLE_EPILOG_KEY = "UNIX_INTRO_DISABLE_EPILOG"


def handler_edited(args):
    mod_timestamp = os.path.getmtime(args.file)
    now = time.time()
    delta = timedelta(seconds=now - mod_timestamp)
    print(delta)


def handler_diff(args):
    same = filecmp.cmp(args.file1, args.file2)
    print(same)


def handler_pass(args):
    if args.seed:
        print(
            "WARNING: The password is NOT SECURE because seed set",
            file=sys.stderr,
        )
    rand = SystemRandom(args.seed)
    with open("/usr/share/dict/words", "r") as f:
        words = [word.strip() for word in f]
    password = [rand.choice(words) for _ in range(args.len)]
    for word in password:
        print(word)


def main():
    parser = argparse.ArgumentParser(
        description="A program to help you experiment with some UNIX commands"
    )
    subparsers = parser.add_subparsers()

    parser_edited = subparsers.add_parser(
        "edited", description="Find how long ago a file was modified")
    parser_edited.set_defaults(func=handler_edited)
    parser_edited.add_argument("file", type=str, action="store")

    parser_diff = subparsers.add_parser(
        "diff", description="Find whether 2 files are the same")
    parser_diff.set_defaults(func=handler_diff)
    parser_diff.add_argument("file1", type=str, action="store")
    parser_diff.add_argument("file2", type=str, action="store")

    parser_pass = subparsers.add_parser(
        "pass", description="Generate a password of random words")
    parser_pass.set_defaults(func=handler_pass)
    parser_pass.add_argument("len", type=int, action="store")
    parser_pass.add_argument(
        "--seed", type=int, action="store", default=None,
        help="seed to make behavior deterministic"
    )

    args = parser.parse_args()
    args.func(args)

    if not os.getenv(DISABLE_EPILOG_KEY, False):
        print(
            "This program is part of unix_intro "
            "(https://github.com/U8NWXD/unix_intro)"
        )


if __name__ == "__main__":
    main()
