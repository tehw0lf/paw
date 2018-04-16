import argparse
import paw
from .static import csets


def parse_cmdline():
        '''
        Parses input arguments and returns parser
        '''
        parser = argparse.ArgumentParser(
            description=''' paw - patterns and wordlists in python
                        \n standard charsets:\n %%d: {d}\n %%u: {u}
 %%l: {l}\n %%h: {h}\n %%i: {i}\n %%s: {s}
                        '''.replace('%%', '%').format(**csets),
            formatter_class=argparse.RawDescriptionHelpFormatter)
        parser.add_argument(
            '-i',
            action='store',
            dest='infile',
            default=None,
            help=' Path to the input file')
        parser.add_argument(
            '-p',
            action='store_true',
            dest='pattern',
            help=''' Read strings from input file,
            generate pattern and print it
            ''')
        parser.add_argument(
            '-g',
            action='store',
            dest='gensets',
            default=None,
            help=(''' Generate wordlist with specified
                charsets for each position
                ([foo][bar][baz] or [%%d%%l][%%l][%%d%%u])
                or [fo%%d][b%%lr][%%uaz]'''))
        parser.add_argument(
            '-c',
            action='store_true',
            dest='custsets',
            help=''' Read charsets from input file
                (line number = string position)''')
        parser.add_argument(
            '-a',
            action='store',
            dest='algo',
            default=0,
            help=''' Algorithm to use for wordlist generation.
                0: itertools.product (stable, default) | 1: build wordlist
                in memory (do not use this for large lists) | 2: generate
                wordlist on the fly (slowest)''')
        parser.add_argument(
            '-H',
            action='store_true',
            dest='hcat',
            help=''' Generate hashcat command
                (cannot be used alone)''')
        parser.add_argument(
            '-o',
            action='store',
            dest='outfile',
            default=None,
            help=''' Path to the output file (stdout if none
                provided)''')
        parser.add_argument(
            '-b',
            action='store',
            dest='max_buf',
            default=256,
            help=' Maximum buffer size (default: 256)')
        return parser, parser.parse_args()


def main():
    parser, args = parse_cmdline()
    paw_cli = paw.Paw(args.gensets, args.hcat, args.infile)
    if (args.custsets and args.gensets):
        parser.print_help()
        print('\nerror: -c, -g, and -p can only be used alone.')
        exit()

    if (args.hcat and args.gensets):
        parser.print_help()
        print('''\nerror: -H has to be used in combination
        with either\t-c, or -p.''')
        exit()

    if args.custsets:
        if args.infile:
            if args.pattern:
                parser.print_help()
                print('\nerror: -c, -g, and -p can only be used alone.')
                exit()
            else:
                paw_cli.gen_custom_charset()
                paw_cli.save_wordlist(args.outfile, args.max_buf)
                if args.hcat:
                    paw_cli.gen_hcat_cmd()
        else:
            parser.print_help()
            print('\nerror: no input file specified.')

    if args.gensets:
        if args.pattern:
            print(args.gensets)
            parser.print_help()
            print('\nerror: -c, -g, and -p can only be used alone.')
            exit()
        else:
            paw_cli.parse_cset()
            paw_cli.save_wordlist(args.outfile, args.max_buf)

    if args.pattern:
        if args.infile:
            paw_cli.from_passwords()
            if args.hcat:
                paw_cli.gen_hcat_cmd()
        else:
            parser.print_help()
            print('\nerror: no input file specified.')

    if paw_cli.wcount > 1:
        print('done with %d warnings' % paw_cli.wcount)
    elif paw_cli.wcount > 0:
        print('done with %d warning' % paw_cli.wcount)
