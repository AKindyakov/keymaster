#!/usr/bin/env python3

import logging
import mimetypes
import os
import re
import subprocess


_log = logging.getLogger(__name__)


class Cryptor:
    def __init__(
        self,
        binary="openssl",
        cipher="aes-256-cbc",
        timeout=4,
    ):
        self.timeout = timeout
        self.cmd = [
            binary,
            cipher,
            "-base64",
        ]

    def encrypt(self, password_filepath, secret):
        # openssl aes-256-cbc -kfile password -in secret -out enc -e
        proc = subprocess.Popen(
            self.cmd + [
                "-kfile", password_filepath,
                "-e",
            ],
            shell=False,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            out, err = proc.communicate(
                input=secret,
                timeout=self.timeout,
            )
            proc.wait()
            if 0 != proc.returncode:
                raise RuntimeError(err)
        except subprocess.TimeoutExpired:
            proc.kill()
            raise
        return out

    def decrypt(self, password_filepath, encrypted_secret):
        # openssl aes-256-cbc -kfile password -in secret -out enc -e
        proc = subprocess.Popen(
            self.cmd + [
                "-kfile", password_filepath,
                "-d",
            ],
            shell=False,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            out, err = proc.communicate(
                input=encrypted_secret,
                timeout=self.timeout,
            )
        except TimeoutExpired:
            proc.kill()
            raise
        return out
