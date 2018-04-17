[![Build Status](https://travis-ci.org/tehw0lf/paw.svg?branch=master)](https://travis-ci.org/tehw0lf/paw) [![codecov](https://codecov.io/gh/tehw0lf/paw/branch/master/graph/badge.svg)](https://codecov.io/gh/tehw0lf/paw)

![paw.py -h](/res/help.png)

# Prerequisites
Python 3.x (developed on Python 3.6.4)

# Instructions
## Installation
```
pip install git+https://github.com/tehw0lf/paw
```

or download the [latest release](https://github.com/tehw0lf/paw/releases/latest).

## Command line usage
Installation via pip will add paw to PATH, thus the command line interface can be called with `paw`.

## Library usage
In order to use individual components from the library, simply `import paw`.

# Commands (CLI)
- `-p`: pattern from passwords
> Read a list of strings from an input file (specified with `-i`) and output the patterns detected for each string length (patterns of the same string length are merged).

- `-g`: wordlist from generated character sets
> Create a wordlist from provided charsets, whereas each string position is represented by brackets (`[ABC][123]` will create `'A1', 'A2', ...,'C3'`). Supports  standard charset integration preceded by `%` (`[%igh] == 'abcdefgh'`).  
The built in charsets are `%d, %h, %i, %u, %l, %s`, which are defined in `static.py` and can be freely combined and customized for each string position of the resulting wordlist.

- `-c`: wordlist from file containing character sets
> Like `-g` above, with the difference that the charsets are read from an input file (like the pattern when using `-p`).

- `-a`: algorithm to use for wordlist generation
> There are three options:  
`0 (stable, default)`: This uses `itertools.product` to generate the wordlist, which is memory efficient and provides a decent speed.  
`1`: `gen_wordlist` builds the whole wordlist in memory before writing it to a file. While the write process itself is faster than option `0`, this does
not work for large lists as paw will run into memory errors.  
`2`: `gen_words` generates the wordlist word for word, which is memory efficient, but not as fast as `itertools.product`.

- `-H`: generate [hashcat](https://github.com/hashcat/hashcat) command
> This will output the hashcat command corresponding to a (detected) pattern, allowing keyspace reduction and usage with hashcats mask attack mode. `-H` is experimental and can only be used with `-p` and `-c`. This project is not affiliated with [hashcat](https://github.com/hashcat/hashcat) in any way.

- `-b`: maximum buffer size
> This argument enables the user to define a custom buffer size. By default, paw will buffer 256 words before writing to the file.

# Functions (library use)
- `cset_lookup()`: determine charset for character
> Return the standard character containing the input character, or a warning if it's a bad character (e.g. `0` or `255`).  
This function uses the predefined character sets from static.py.

> Arguments:
>> `instr`: Single ASCII character.

- `from_passwords()`: read passwords and generate pattern
> Read passwords from a file and generates a pattern that fits all of them. Individual patterns are generated for passwords of different length. The equivalent CLI command is `-p`.

> Arguments:
>> `infile`: Path to input file to read passwords from.

- `gen_custom_charset()`: generate custom character set from file
> Read character sets from a file and generate a wordlist. The equivalent CLI command is `-c`.

> Arguments:
>> `infile`: Path to input file to read character sets from.

- `gen_hcat_cmd()`: Generate [hashcat](https://github.com/hashcat/hashcat) command
> Build a [hashcat](https://github.com/hashcat/hashcat) brute force (`-a 3`) command using the supplied pattern. Since [hashcat](https://github.com/hashcat/hashcat) supports two custom character sets in addition to its builtin sets, this function provides the possibility to use lower and upper hex as individual sets to reduce the keyspace. The equivalent CLI command is `-H`.

> Requires to build a dict of compatible patterns (`paw.patterns`) first. This can be done by either calling `gen_patterns()` directly or by using `from_passwords()` or `gen_custom_charset()`.

- `gen_pattern()`: generate pattern from string
> Build pattern from a provided string by looking up each string position using `cset_lookup()`.

> Arguments:
>> `instr`: String to build pattern from.

- `gen_wordlist()`: generate wordlist from character set
> Create a wordlist from the provided charsets through recursion, ensuring that all characters are used. Requires `paw.cset` to be built either manually or by using the functions `parse_cset()` or `gen_custom_charset()` beforehand.

- `parse_cset()`: parse input character set
> Read user input custom character set and replace standard charset identifiers with the associated characters (e.g. `%d` will be converted to `0123456789`). Requires that `paw.gensets` contains position specific character sets within brackets. The equivalent CLI command is `-g`.

- `save_wordlist()`: write wordlist to file
> After wordlist generation, this function will either write it to a specified file or print it. This way it can be used to pipe the generated wordlist to other tools. Requires `paw.cset` (dict of character sets) to be created beforehand.

> Arguments:
>> `outfile`: The output file, default is `None` for stdout.
>> `max_buf`: Maximum buffer size, default is 256.
