"""
A light weight wiki, designed to be very similar to the abandoned `markdoc`
project.

Usage: markdoc2 build [options]

Options:
    -o=OUTDIR --output-dir=OUTDIR       The directory to put all rendered html
                                            into [Default: _html]
    -s=SRC --source-dir=SRC             The directory containing the wiki's
                                            source files [Default: wiki]
    -h --help                           Show this help text
    -V --version                        Print the version number and exit
"""

import os
import sys
import docopt
import markdoc2


def build(args):
    config = {
            'wiki-dir': args['--source-dir'],
            'output-dir': args['--output-dir'],
            }

    if not os.path.exists(args['--source-dir']):
        print('No wiki found at {}'.format(args['--source-dir']))
        print('Aborting...')
        return 1

    b = markdoc2.Builder(config)

    try:
        b.build()
        return 0
    except markdoc2.MarkdocError as e:
        print('Error encountered while building!')
        print()
        print(e)
        return 1


def main():
    args = docopt.docopt(__doc__, version=markdoc2.__version__)

    if args['build']:
        sys.exit(build(args))


if __name__ == "__main__":
    main()



