#!/usr/bin/env python
# This file is part of unix_intro (github.com/U8NWXD/unix_intro),
# which is distributed under the terms in the LICENSE.txt file in the
# root folder of the project.
# Copyright (c) 2020 U8N WXD (github.com/U8NWXD) <cs.temporary@icloud.com>


from __future__ import print_function

import argparse
from datetime import timedelta
import filecmp
import getpass
import hashlib
import os
from random import SystemRandom
import sys
import time


DISABLE_EPILOG_KEY = "UNIX_INTRO_DISABLE_EPILOG"
PBKDF2_ITERS = 100000
PBKDF2_ALGO = "sha512"
PBKDF2_SALT_BYTES = 16
HASH_FILE = "secret_hash.txt"
ENCODING = "utf-8"


def hash_password(salt, password):
    salt_bytes = salt.encode(ENCODING)
    pass_bytes = password.encode(ENCODING)
    digest = hashlib.pbkdf2_hmac(
        PBKDF2_ALGO, pass_bytes, salt_bytes, PBKDF2_ITERS)
    try:
        return digest.hex()
    except AttributeError:
        return digest.encode('hex')


def check_password(submitted, stored):
    # Stored is a string: "[hex-encoded salt] [hex-encoded hash]"
    salt_str, hash_str = stored.split()
    expected_hash = hash_password(salt_str, submitted)
    return expected_hash == hash_str


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


def handler_secret(args):
    print("There is a file in /usr/ called 'words'.")
    print("Count the words in that file that have the 'not' prefix.")
    print("Assume the prefix takes the forms: il-, ir-, im-, in-.")
    password = getpass.getpass("Password: ")
    with open(HASH_FILE, "r") as f:
        stored_hash = f.read().rstrip()
    if check_password(password, stored_hash):
        with open (".secret", "r") as f:
            secret = f.read().strip()
            print(secret)
    else:
        print("Incorrect")


def handler_hash(args):
    rand = SystemRandom()
    salt = rand.getrandbits(16)
    salt_str = format(salt, "x")
    hash_str = hash_password(salt_str, args.password)
    print(salt_str + " " + hash_str)


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

    parser_hash = subparsers.add_parser(
        "hash", description="Generate a hash string for a password")
    parser_hash.set_defaults(func=handler_hash)
    parser_hash.add_argument(
        "password", type=str, action="store"
    )

    parser_secret = subparsers.add_parser("secret")
    parser_secret.set_defaults(func=handler_secret)

    args = parser.parse_args()
    args.func(args)

    if not os.getenv(DISABLE_EPILOG_KEY, False):
        print(
            "This program is part of unix_intro "
            "(https://github.com/U8NWXD/unix_intro)"
        )


if __name__ == "__main__":
    main()
