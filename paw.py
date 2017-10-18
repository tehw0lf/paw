#!/usr/bin/python3
import argparse
import os
import sys
import static

class paw:
    '''
    generates patterns and wordlists based on preset or custom charsets
    '''
    def cset_lookup(self, instr):
        '''
        Determine charset from character using standard csets
        '''
        p = str()
        #digits
        if instr in static.csets['d']:
            p = 'd'
        # hex upper
        elif instr in static.csets['h']:
            p = '%h'
        # alpha upper
        elif instr in static.csets['u']:
            p = 'u'
        # hex lower
        elif instr in static.csets['i']:
            p = '%i'
        # alpha lower
        elif instr in static.csets['l']:
            p = 'l'
        # special chars
        elif instr in static.csets['s']:
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
        with open(self.args.infile, 'r', encoding='utf-8') as f:
            for line in f:
                self.gen_pattern(line.strip('\n'))
        print('')
        for key, value in self.patterns.items():
            print('length: %d\t pattern: %s'  % (key, ''.join(value)))
                
    def gen_charset(self):
        '''
        Generate charset from file or predefined charsets
        '''
        if self.args.custsets:  # -c
            if self.args.gensets:
                self.parser.print_help()
                print('\nerror: -c, -g, and -p can only be used alone.')
                exit()
            else:
                with open(self.args.infile, 'r', encoding='utf-8') as f:
                    for i, line in enumerate(f):
                        self.cset[i] = list(sorted(set(line.strip('\n'))))
                        for j in self.cset[i]:
                            try:
                                self.patterns[i] = ''.join(
                                    sorted(set(self.patterns[i]
                                               + self.cset_lookup(j))))
                            except KeyError:
                                self.patterns[i] = self.cset_lookup(j)
        
        elif self.args.gensets: # -g
            self.parse_cset()

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
                    hexu = '-1 %s%s ' % (static.csets['d'], static.csets['h'])
                elif '%h' in ''.join(sorted(i)):
                    hexu = '-1 %s ' % static.csets['h']
                if '%di' in ''.join(sorted(i)):
                    hexl = '-2 %s%s ' % (static.csets['d'], static.csets['i'])
                elif '%i' in ''.join(sorted(i)):
                    hexl = '-2 %s ' % static.csets['i']
                    
                for j in i:
                    pattern += ('?' + j
                                    .replace('%', '')
                                    .replace('dh', 'h')
                                    .replace('di', 'i')
                                    .replace('h', '1')
                                    .replace('i', '2'))
                self.catstrs[k] = catstr + hexu + hexl + pattern.replace('??', '?')
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
        if self.args.pattern:
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
            #read buffer_a from arr2d (self.cset)
            for i in range(1, len(arr2d)):
                temparr[i-1] = sorted(set(arr2d[i]))
            buffer_b = self.gen_wordlist(temparr)
            buffer_c = [(i+j) for i in buffer_a for j in buffer_b]
            return buffer_c

    def parse_args(self):
        '''
        Parses input arguments and executes functions
        '''
        self.parser = argparse.ArgumentParser(
            description = ''' paw - patterns and wordlists in python
                        \n standard charsets:\n %%d: {d}\n %%u: {u}
 %%l: {l}\n %%h: {h}\n %%i: {i}\n %%s: {s}
                        '''.replace('%%', '%').format(**static.csets),
            formatter_class = argparse.RawDescriptionHelpFormatter)
        self.parser.add_argument('-i',
                            action='store',
                            dest='infile',
                            help=' Path to the input file')
        self.parser.add_argument('-p',
                            action='store_true',
                            dest='pattern',
                            help=''' Read strings from input file,
                            generate pattern and print it
                            ''')
        self.parser.add_argument('-g',
                            action='store',
                            dest='gensets',
                            help=(''' Generate wordlist with specified
                                charsets for each position
                            ([foo][bar][baz] or [%%d%%l][%%l][%%d%%u])
                            or [fo%%d][b%%lr][%%uaz]'''))
        self.parser.add_argument('-c',
                            action='store_true',
                            dest='custsets',
                            help=''' Read charsets from input file
                            (line number = string position)''')
        self.parser.add_argument('-H',
                            action='store_true',
                            dest='hcat',
                            help=''' Generate hashcat command
                                (cannot be used alone)''')
        self.parser.add_argument('-o',
                            action='store',
                            dest='outfile',
                            default='',
                            help=''' Path to the output file (stdout if none
                            provided)''')
        self.args = self.parser.parse_args()

        if (self.args.hcat
            and self.args.gensets):
                self.parser.print_help()
                print('''\nerror: -H has to be used in combination with either
\t-c, -g, or -p.''')
                exit()
        
        if (self.args.custsets
            or self.args.gensets):
            if self.args.pattern:
                self.parser.print_help()
                print('\nerror: -c, -g, and -p can only be used alone.')
                exit()
            else:
                self.gen_charset()
                self.save_wordlist()
                if self.args.hcat:
                    if self.args.custsets:
                        self.gen_hcat_cmd()
            
        elif self.args.pattern:
            self.from_passwords()
            if self.args.hcat:
                self.gen_hcat_cmd()

        if self.wcount > 0:
            print('done with %d warnings' % self.wcount)

    def parse_cset(self):
        cur = 0
        cnt = 0
        if self.args.gensets:
            tmpsets = self.args.gensets
        for i in range(len(tmpsets)):
            if tmpsets[i] == '[':
                cnt += 1
                continue
            elif tmpsets[i] == ']':
                if not self.args.hcat:
                    self.cset[cur].replace('%', '')
                cnt -= 1
                cur += 1
            else:
                if tmpsets[i] == '%':
                    if tmpsets[i+1] in static.csets.keys():
                        try:
                            self.cset[cur] = (self.cset[cur] +
                                              static.csets[tmpsets[i+1]])
                        except KeyError:
                            self.cset[cur] = static.csets[tmpsets[i+1]]
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
        wlist = self.gen_wordlist(self.cset)
        try:
            with open(self.args.outfile, 'a', encoding='utf-8') as wl:
                for line in wlist:
                    wl.write('%s\n' % line)
        except OSError:
            for i in wlist:
                print(i)
            
    def __init__(self):
        self.catstrs = {}
        self.cset = {}
        self.patterns = {}        
        self.wcount = 0
        self.parse_args()
        
if __name__ == '__main__':
    paw()
    
