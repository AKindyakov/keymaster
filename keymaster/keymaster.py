#!/usr/bin/env python3

import argparse
import json
import logging
import sys
import tempfile
import termcolor

_log = logging.getLogger(__name__)

ONE_INDENT = "  "
PATH_SEPARATOR = "/"
PATH_ROOT = "."
SECRET_ATTR_PREFIX = "~"
SECRET_ATTR_NAME = SECRET_ATTR_PREFIX + "value"


class IColoredOutStream():
    def _rec_print_impl(self, name, obj, indent):
        if name.startswith(SECRET_ATTR_PREFIX):
            return
        if not isinstance(obj, dict):
            return
        color = "green" if SECRET_ATTR_NAME in obj else "blue"
        self.print(
            color=color,
            text="{indent}{key}".format(
                indent=ONE_INDENT * indent,
                key=name,
            ),
        )
        for key, value in obj.items():
            self._rec_print_impl(key, value, indent + 1)

    def rec_print(self, obj):
        self._rec_print_impl("", obj, 0)


class FakeColoredOutStream(IColoredOutStream):
    def __init__(self, out_stream):
        self.out_stream = out_stream

    def print(self, color, text):
        self.out_stream.write(text)
        self.out_stream.write("\n")


class TerminalColoredOutStream(IColoredOutStream):
    def __init__(self, out_stream):
        self.out_stream = out_stream

    def print(self, color, text):
        self.out_stream.write(
            termcolor.colored(text, color)
        )
        self.out_stream.write("\n")


def prefix_search_recursive(obj, path, prefix):
    _log.debug("Prefix %r %r", prefix, path)
    out_dict = dict()
    path_str = PATH_SEPARATOR.join(path)
    if path_str.startswith(prefix):
        out_dict[path_str] = obj
    elif prefix.startswith(path_str):
        for key, value in obj.items():
            path.append(key)
            out_dict.update(
                prefix_search_recursive(
                    obj=value,
                    path=path,
                    prefix=prefix,
                )
            )
            path.pop()
    return out_dict


class Storage():
    def __init__(self, storage_file):
        self.storage = None
        with open(storage_file) as fin:
            self.storage = json.load(fin)

    def search(self, prefix):
        return prefix_search_recursive(
            obj=self.storage.get(PATH_ROOT, dict()),
            path=[],
            prefix=prefix,
        )

    def shutdown(self):
        print("shutdown")

    def generate(self):
        print("generate")

    def get(self, name):
        value = self.storage.get(".", dict()).get(name)
        if value is None:
            print("no such key")
            return
        if not isinstance(value, str):
            print("this is not a value, but path")
            return
        print("Value %r" % value)
        return value


def main():
    parser = argparse.ArgumentParser(
        description="Process some integers."
    )
    cmd = parser.add_mutually_exclusive_group()
    cmd.add_argument(
        "_get",
        metavar='NAME',
        nargs='?',
        help='an integer for the accumulator'
    )
    cmd.add_argument(
        "--get",
        metavar='NAME',
        help="sum the integers (default: find the max)"
    )
    cmd.add_argument(
        "-s", "--search",
        help="sum the integers (default: find the max)"
    )
    cmd.add_argument(
        "--shutdown",
        action="store_true",
        help="sum the integers (default: find the max)"
    )
    cmd.add_argument(
        "--generate",
        help="sum the integers (default: find the max)"
    )
    parser.add_argument(
        "-c", "--clipboard",
        action="store_true",
        help="sum the integers (default: find the max)"
    )
    parser.add_argument(
        "--colored",
        action="store_true",
        help=""
    )
    parser.add_argument(
        "--file",
        required=True,
        help="",
    )
    args = parser.parse_args()
    print("%r" % args)

    if args.colored:
        colored_out = FakeColoredOutStream(sys.stdout)
    else:
        colored_out = TerminalColoredOutStream(sys.stdout)

    storage = Storage(args.file)
    if args.search is not None:
        print("search")
        sys.stdout.write(
            "Search for prefix \"{}\"\n".format(args.search)
        )
        obj = storage.search(args.search)
        colored_out.rec_print(obj)
    elif args.shutdown:
        print("shutdown")
    elif args.generate:
        print("generate")
    elif args.clipboard:
        print("clipboard")
    else:
        if args.get is None and args._get is None:
            raise RuntimeError("GET command requires a name of secret")
        print("get")
        storage.get(args.get or args._get)

    tempfile.NamedTemporaryFile(mode='w+b')


if __name__ == "__main__":
    try:
        _log = logging.getLogger(__name__)
        _log.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(
            logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
        )
        _log.addHandler(ch)
        main()
    except SystemExit:
        raise
    except:
        _log.exception("Catched exception ")
        sys.exit(1)
