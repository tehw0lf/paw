![paw.py -h](/res/help.png)

# Prerequisites
Python 3.x (developed on Python 3.6.3)

# Install Instructions
```
git clone https://github.com/tehw0lf/paw.git
cd paw
./tests.py (optional unit tests)
./paw.py
```

# Functions
- `-p`: pattern from passwords
> Read a list of strings from an input file (specified with `-i`) and output the patterns detected for each string length (patterns of the same string length are merged).

- `-s`: wordlist from standard character sets
> Create a wordlist based on specified standard charsets. The built in charsets are `%d, %h, %i, %u, %l, %s`, which are defined in `static.py` and can be freely customized. Charsets can be combined and customized for each string position of the resulting wordlist.

- `-g`: wordlist from generated character sets
> Creates a wordlist from provided charsets, whereas each string position is represented by brackets (`[ABC][123]` will create `'A1', 'A2', ...,'C3'`). Supports hybrid mode to integrate standard charsets preceded by `%` (`[%igh] == 'abcdefgh'`).

- `-c`: wordlist from file containing character sets
> Like `-g` above, with the difference that the charsets are read from an input file (like the pattern when using `-p`).

- `-H`: generate [hashcat](https://github.com/hashcat/hashcat) command
> This will output the hashcat command corresponding to a (detected) pattern, allowing keyspace reduction and usage with hashcats mask attack mode. `-H` is experimental and can only be used with `-p` and `-c`. This project is not affiliated with [hashcat](https://github.com/hashcat/hashcat) in any way.