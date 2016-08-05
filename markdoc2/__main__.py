"""
A light weight wiki, designed to be very similar to the abandoned `markdoc`
project.

Usage: markdoc2 build [options]
       markdoc2 init <path>

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
import shutil
import docopt
import markdoc2


def build(args):
    """
    Build all html files.
    """
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


def init(args):
    root_dir = args['<path>']

    os.makedirs(root_dir)
    print('mkdir', root_dir)

    for d in ['wiki', '_html']:
        path = os.path.join(root_dir, d)
        os.mkdir(path)
        print('mkdir', path)

    print()
    print('Your new wiki is ready.')
    print('To populate it with content, just add a')
    print('markdown file to', os.path.join(root_dir, 'wiki'))
    print()
    print('To render the wiki, just run `markdoc2 build`')
    print('and point your browser at any of the files in the `_html` dir')

    return 0


def main():
    args = docopt.docopt(__doc__, version=markdoc2.__version__)

    if args['build']:
        sys.exit(build(args))
    elif args['init']:
        sys.exit(init(args))


if __name__ == "__main__":
    main()



