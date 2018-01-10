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
        return parser, parser.parse_args()


if __name__ == '__main__':  # pragma: no cover
    parser, args = parse_cmdline()
    paw = paw.Paw(args.gensets, args.hcat, args.infile, args.outfile)  # ?
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
        if args.pattern:
            parser.print_help()
            print('\nerror: -c, -g, and -p can only be used alone.')
            exit()
        else:
            paw.gen_custom_charset()
            paw.save_wordlist()
            if args.hcat:
                paw.gen_hcat_cmd()

    if args.gensets:
        if args.pattern:
            print(args.gensets)
            parser.print_help()
            print('\nerror: -c, -g, and -p can only be used alone.')
            exit()
        else:
            paw.parse_cset()
            paw.save_wordlist()

    elif args.pattern:
        paw.from_passwords()
        if args.hcat:
            paw.gen_hcat_cmd()

    if paw.wcount > 1:
        print('done with %d warnings' % paw.wcount)
    elif paw.wcount > 0:
        print('done with %d warning' % paw.wcount)
