#!/usr/bin/python3
from .static import csets
import functools
import logging
import operator
import re
import sys
import wlgen

logging.getLogger(__name__).addHandler(logging.NullHandler())


class Paw:
    """
    generates patterns and wordlists based on preset or custom charsets
    """

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
        """
        Determine charset from character using standard csets
        """
        p = str()
        # digits
        if instr in csets["d"]:
            p = "d"
        # hex upper
        elif instr in csets["h"]:
            p = "%h"
        # alpha upper
        elif instr in csets["u"]:
            p = "u"
        # hex lower
        elif instr in csets["i"]:
            p = "%i"
        # alpha lower
        elif instr in csets["l"]:
            p = "l"
        # special chars
        elif instr in csets["s"]:
            p = "s"
        # bad chars
        if ord(instr) == 0 or ord(instr) == 255:
            p = "b"
            logging.warning("bad char detected in input")
            self.wcount += 1
        return p

    def from_passwords(self):
        """
        Reads passwords from file and generates pattern
        """
        with open(self.infile, "r", encoding="utf-8") as f:
            for line in f:
                self.gen_pattern(line.strip("\n"))
        print("")
        for key, value in self.patterns.items():
            print("length: %d\t pattern: %s" % (key, "".join(value)))

    def gen_custom_charset(self):
        """
        Generate custom charset from file
        """
        with open(self.infile, "r", encoding="utf-8") as f:
            for i, line in enumerate(f):
                self.cset[i] = list(set(line.strip("\n")))
                for j in self.cset[i]:
                    try:
                        self.patterns[i] = set(
                            self.patterns[i] + self.cset_lookup(j)
                        )
                    except KeyError:
                        self.patterns[i] = self.cset_lookup(j)

    def gen_hcat_cmd(self):
        """
        Print hashcat string for standard patterns
        """
        catstr = "-a 3 "
        print("")
        for k, i in self.patterns.items():
            pattern = ""
            hexu = ""
            hexl = ""
            if len("".join(i)) > 0:
                if "%dh" in "".join(sorted(i)):
                    hexu = "-1 %s%s " % (csets["d"], csets["h"])
                elif "%h" in "".join(sorted(i)):
                    hexu = "-1 %s " % csets["h"]
                if "%di" in "".join(sorted(i)):
                    hexl = "-2 %s%s " % (csets["d"], csets["i"])
                elif "%i" in "".join(sorted(i)):
                    hexl = "-2 %s " % csets["i"]
                for j in i:
                    pattern += "?" + j.replace("%", "").replace(
                        "dh", "h"
                    ).replace("di", "i").replace("h", "1").replace("i", "2")
                self.catstrs[k] = (
                    catstr + hexu + hexl + pattern.replace("??", "?")
                )
            else:
                logging.warning("pattern %d is empty" % k)
                self.wcount += 1
        for i in self.catstrs.values():
            print(i)

    def gen_pattern(self, instr):
        """
        Generate pattern and position specific charset from string
        """
        pattern = list()
        # Get pattern and charset for each string position
        for index, _ in enumerate(instr):
            pattern.append("%" + self.cset_lookup(instr[index]))
            try:
                self.cset[index] = "".join(
                    set(self.cset[index] + instr[index])
                )
            except KeyError:
                self.cset[index] = instr[index]
        # Filter duplicates from pattern and sort it
        pattern = ["".join(sorted(set(i))) for i in pattern]

        # Update length based dict with new pattern
        try:
            self.patterns[len(instr)] = [
                "".join(
                    sorted(
                        set(self.patterns[len(instr)][index] + pattern[index])
                    )
                )
                for index, _ in enumerate(instr)
            ]
        except KeyError:
            self.patterns[len(instr)] = pattern

    def parse_cset(self):
        """
        Parses character sets in the form [abc][123]
        ([] represents a string position in the output)
        """
        tmpsets = self.gensets
        matches = re.findall("\[(.*?\]?)\]", tmpsets)
        for midx, match in enumerate(matches):
            if match == "":
                logging.error("empty character set detected, aborting")
                sys.exit()
            else:
                for cidx, char in enumerate(match):
                    if char == "%":
                        if match[cidx + 1] in csets.keys():
                            try:
                                self.cset[midx] = (
                                    self.cset[midx] + csets[match[cidx + 1]]
                                )
                            except KeyError:
                                self.cset[midx] = csets[match[cidx + 1]]
                    elif match[cidx - 1] != "%":
                        try:
                            self.cset[midx] = self.cset[midx] + char
                        except KeyError:
                            self.cset[midx] = char
        for key in self.cset.keys():
            self.cset[key] = "".join(sorted(set(self.cset[key])))

    def save_wordlist(self, outfile=None, max_buf=256):
        """
        Write wordlist to file
        """
        try:
            buffer = []
            with open(outfile, "w", encoding="utf-8") as wl:
                print(
                    "generating %d lines."
                    % functools.reduce(
                        operator.mul, [len(i) for i in self.cset.values()], 1
                    )
                )
                for word in self.gen_wordlist(self.cset):
                    buffer.append(word)
                    if len(buffer) == max_buf:
                        wl.write("\n".join(buffer) + "\n")
                        buffer = []
                wl.write("\n".join(buffer))

        except (OSError, TypeError):  # stdout
            for word in self.gen_wordlist(self.cset):
                print(word)
