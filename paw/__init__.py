#!/usr/bin/python3
from .static import csets


class Paw:
    '''
    generates patterns and wordlists based on preset or custom charsets
    '''
    def cset_lookup(self, instr):
        '''
        Determine charset from character using standard csets
        '''
        p = str()
        # digits
        if instr in csets['d']:
            p = 'd'
        # hex upper
        elif instr in csets['h']:
            p = '%h'
        # alpha upper
        elif instr in csets['u']:
            p = 'u'
        # hex lower
        elif instr in csets['i']:
            p = '%i'
        # alpha lower
        elif instr in csets['l']:
            p = 'l'
        # special chars
        elif instr in csets['s']:
            p = 's'
        # bad chars
        if ord(instr) == 0 or ord(instr) == 255:
            p = 'b'
            print('warning: bad char detected in input')
            self.wcount += 1
        return p

    def from_passwords(self):
        '''
        Reads passwords from file and generates pattern
        '''
        with open(self.infile, 'r', encoding='utf-8') as f:
            for line in f:
                self.gen_pattern(line.strip('\n'))
        print('')
        for key, value in self.patterns.items():
            print('length: %d\t pattern: %s' % (key, ''.join(value)))

    def gen_custom_charset(self):
        '''
        Generate custom charset from file or predefined charsets
        '''
        with open(self.infile, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                self.cset[i] = list(sorted(set(line.strip('\n'))))
                for j in self.cset[i]:
                    try:
                        self.patterns[i] = ''.join(
                            sorted(set(self.patterns[i]
                                       + self.cset_lookup(j))))
                    except KeyError:
                        self.patterns[i] = self.cset_lookup(j)

    def gen_hcat_cmd(self):
        '''
        Print hashcat string for standard patterns
        '''
        catstr = '-a 3 '
        print('')
        for k, i in self.patterns.items():
            pattern = ''
            hexu = ''
            hexl = ''
            if len(''.join(i)) > 0:
                if '%dh' in ''.join(sorted(i)):
                    hexu = '-1 %s%s ' % (csets['d'], csets['h'])
                elif '%h' in ''.join(sorted(i)):
                    hexu = '-1 %s ' % csets['h']
                if '%di' in ''.join(sorted(i)):
                    hexl = '-2 %s%s ' % (csets['d'], csets['i'])
                elif '%i' in ''.join(sorted(i)):
                    hexl = '-2 %s ' % csets['i']

                for j in i:
                    pattern += ('?' + j
                                .replace('%', '')
                                .replace('dh', 'h')
                                .replace('di', 'i')
                                .replace('h', '1')
                                .replace('i', '2'))
                self.catstrs[k] = (catstr + hexu + hexl +
                                   pattern.replace('??', '?'))
            else:
                print('warning: pattern %d is empty' % k)
                self.wcount += 1

        for i in self.catstrs.values():
            print(i)

    def gen_pattern(self, instr):
        '''
        Generate pattern and position specific charset from string
        '''
        # Get pattern for each string position
        pattern = ['%' + self.cset_lookup(i) for i in instr]

        # Sort pattern and keep only unique values
        pattern = [''.join(sorted(set(i))) for i in pattern]
        for i in range(len(instr)):
            try:
                self.cset[i] = ''.join(sorted(set(self.cset[i]
                                                  + instr[i])))
            except KeyError:
                self.cset[i] = instr[i]

        # Update length based dict with new charset
        try:
            self.patterns[len(instr)] = [''.join(sorted(
                set(self.patterns[len(instr)][i] + pattern[i])))
                for i in range(len(instr))]
        except KeyError:
            self.patterns[len(instr)] = pattern

    def gen_wordlist(self, arr2d):
        '''
        Recursively build wordlist
        '''
        temparr = {}
        if len(arr2d) == 1:
            return arr2d[0]
        else:
            buffer_a = sorted(set(arr2d[0]))
            # read buffer_a from arr2d (self.cset)
            for i in range(1, len(arr2d)):
                temparr[i-1] = sorted(set(arr2d[i]))
            buffer_b = self.gen_wordlist(temparr)
            buffer_c = [(i+j) for i in buffer_a for j in buffer_b]
            return buffer_c

    def parse_cset(self):
        cur = 0
        cnt = 0
        tmpsets = self.gensets

        for i in range(len(tmpsets)):
            if tmpsets[i] == '[':
                cnt += 1
                continue
            elif tmpsets[i] == ']':
                if not self.hcat:
                    self.cset[cur].replace('%', '')
                cnt -= 1
                cur += 1
            else:
                if tmpsets[i] == '%':
                    if tmpsets[i+1] in csets.keys():
                        try:
                            self.cset[cur] = (self.cset[cur] +
                                              csets[tmpsets[i+1]])
                        except KeyError:
                            self.cset[cur] = csets[tmpsets[i+1]]
                elif tmpsets[i-1] != '%':
                    try:
                        self.cset[cur] = self.cset[cur] + tmpsets[i]
                    except KeyError:
                        self.cset[cur] = tmpsets[i]
        if cnt > 0:
            print('warning: input contains uneven number of brackets')
            self.wcount += 1

    def save_wordlist(self):
        '''
        Generate wordlist, then write to file
        '''
        self.wlist = self.gen_wordlist(self.cset)
        try:
            with open(self.outfile, 'a', encoding='utf-8') as wl:
                for line in self.wlist:
                    wl.write('%s\n' % line)
        except (OSError, TypeError):  # stdout
            for i in self.wlist:
                print(i)

    def __init__(self, gensets=None, hcat=False, infile=None, outfile=None):
        self.catstrs = {}
        self.cset = {}
        self.patterns = {}
        self.wcount = 0
        self.gensets = gensets
        self.hcat = hcat
        self.infile = infile
        self.outfile = outfile
