#!/usr/bin/env python3
"""
"""


import argparse
import json
import logging
import sys
import tempfile
import getpass

import crypto


_log = logging.getLogger(__name__)


def main():
    secret = "I'm a message"
    cr = crypto.Cryptor()
    with tempfile.NamedTemporaryFile() as pass_tmp_file:
        pass_tmp_file.write(
            getpass.getpass(
                prompt="Master password:"
            ).encode("utf-8")
        )
        pass_tmp_file.flush()
        with open("enc.secret", "w+b") as fout:
            fout.write(
                cr.encrypt(pass_tmp_file.name, secret.encode("utf-8"))
            )
        with open("enc.secret", "r+b") as fin:
            print(
                cr.decrypt(pass_tmp_file.name, fin.read())
            )


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
