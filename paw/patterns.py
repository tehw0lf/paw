import logging
import re
import sys

from .static import csets


def cset_lookup(instr):
    p = str()
    if instr in csets["d"]:
        p = "d"
    elif instr in csets["h"]:
        p = "%h"
    elif instr in csets["u"]:
        p = "u"
    elif instr in csets["i"]:
        p = "%i"
    elif instr in csets["l"]:
        p = "l"
    elif instr in csets["s"]:
        p = "s"
    if ord(instr) == 0 or ord(instr) == 255:
        p = "b"
        logging.warning("bad char detected in input")
        return p, True
    return p, False


def generate_pattern(instr, patterns, charset):
    pattern = []
    for index, char in enumerate(instr):
        p, _ = cset_lookup(char)
        pattern.append("%" + p)
        try:
            charset[index] = "".join(set(charset[index] + char))
        except KeyError:
            charset[index] = char

    pattern = ["".join(sorted(set(i))) for i in pattern]
    try:
        patterns[len(instr)] = [
            "".join(sorted(set(patterns[len(instr)][index] + pattern[index])))
            for index, _ in enumerate(instr)
        ]
    except KeyError:
        patterns[len(instr)] = pattern

    return patterns, charset


def generate_hcat_command(patterns, catstrs, wcount):
    catstr = "-a 3 "
    print("")
    for k, i in patterns.items():
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
                pattern += "?" + j.replace("%", "").replace("dh", "h").replace(
                    "di", "i"
                ).replace("h", "1").replace("i", "2")
            catstrs[k] = catstr + hexu + hexl + pattern.replace("??", "?")
        else:
            logging.warning("pattern %d is empty" % k)
            wcount += 1
    return catstrs, wcount


def parse_charsets(infile, charset):
    matches = re.findall(r"\[(.*?\]?)\]", infile)
    for midx, match in enumerate(matches):
        if match == "":
            logging.error("empty character set detected, aborting")
            sys.exit()
        else:
            for cidx, char in enumerate(match):
                if char == "%":
                    if match[cidx + 1] in csets.keys():
                        try:
                            charset[midx] = (
                                charset[midx] + csets[match[cidx + 1]]
                            )
                        except KeyError:
                            charset[midx] = csets[match[cidx + 1]]
                elif match[cidx - 1] != "%":
                    try:
                        charset[midx] = charset[midx] + char
                    except KeyError:
                        charset[midx] = char

    for key in charset.keys():
        charset[key] = "".join(sorted(set(charset[key])))
    return charset
