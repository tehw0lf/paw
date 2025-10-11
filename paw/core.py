#!/usr/bin/python3
import logging

import wlgen

from .patterns import (
    cset_lookup,
    generate_hcat_command,
    generate_pattern,
    parse_charsets,
)
from .wordlist import save_to_file

logging.getLogger(__name__).addHandler(logging.NullHandler())


class Paw:
    def __init__(self, gensets=None, hcat=False, infile=None, algo=0):
        if algo == 0:
            self.gen_wordlist = wlgen.gen_wordlist_iter
        elif algo == 1:
            self.gen_wordlist = wlgen.gen_wordlist
        elif algo == 2:
            self.gen_wordlist = wlgen.gen_words
        self.catstrs = {}
        self.cset = {}
        self.patterns = {}
        self.wcount = 0
        self.gensets = gensets
        self.hcat = hcat
        self.infile = infile

    def cset_lookup(self, instr):
        """Original cset_lookup as instance method for compatibility"""
        p, is_bad = cset_lookup(instr)
        if is_bad:
            self.wcount += 1
        return p

    def gen_custom_charset(self):
        with open(self.infile, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                self.cset[i] = list(set(line.strip("\n")))
                for j in self.cset[i]:
                    p, is_bad = cset_lookup(j)
                    if is_bad:
                        self.wcount += 1
                    try:
                        self.patterns[i] = set(self.patterns[i] + p)
                    except KeyError:
                        self.patterns[i] = p

    def from_passwords(self):
        with open(self.infile, "r", encoding="utf-8") as f:
            for line in f:
                self.patterns, self.cset = generate_pattern(
                    line.strip("\n"), self.patterns, self.cset
                )
        print("")
        for key, value in self.patterns.items():
            print("length: %d\t pattern: %s" % (key, "".join(value)))

    def gen_hcat_cmd(self):
        self.catstrs, self.wcount = generate_hcat_command(
            self.patterns, self.catstrs, self.wcount
        )
        for i in self.catstrs.values():
            print(i)

    def parse_cset(self):
        self.cset = parse_charsets(self.gensets, self.cset)

    def save_wordlist(self, outfile=None, max_buf=256):
        save_to_file(self.cset, self.gen_wordlist, outfile, max_buf)
