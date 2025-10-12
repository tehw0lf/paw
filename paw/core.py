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
    def __init__(self, gensets=None, hcat=False, infile=None, algo='auto'):
        # Map algorithm parameter to wlgen method
        # Support both 'auto' string and legacy numeric values (0, 1, 2)
        if algo == 'auto':
            self.method = 'auto'
            self.gen_wordlist = None  # Will use wlgen.generate_wordlist
        elif algo == 0 or algo == '0':
            self.method = 'iter'
            self.gen_wordlist = wlgen.gen_wordlist_iter
        elif algo == 1 or algo == '1':
            self.method = 'list'
            self.gen_wordlist = wlgen.gen_wordlist
        elif algo == 2 or algo == '2':
            self.method = 'words'
            self.gen_wordlist = wlgen.gen_words
        else:
            # Default to auto for any other value
            self.method = 'auto'
            self.gen_wordlist = None

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
        # Use smart algorithm selection if method is 'auto'
        if self.method == 'auto':
            def gen_func(charset):
                return wlgen.generate_wordlist(charset, method='auto')
        else:
            gen_func = self.gen_wordlist
        save_to_file(self.cset, gen_func, outfile, max_buf)
