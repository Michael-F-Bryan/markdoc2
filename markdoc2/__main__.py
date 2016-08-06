"""
A light weight wiki, designed to be very similar to the abandoned `markdoc`
project.

Usage: markdoc2 build [options]
       markdoc2 init <path>
       markdoc2 watch [options]

Options:
    -o=OUTDIR --output-dir=OUTDIR   The directory to put all rendered html
                                        into [Default: _html]
    -s=SRC --source-dir=SRC         The directory containing the wiki's
                                        source files [Default: wiki]
    -b --browser                    Open the wiki up in your browser after
                                        building
    -h --help                       Show this help text
    -V --version                    Print the version number and exit
"""

import os
import sys
import shutil
import subprocess
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
    except markdoc2.MarkdocError as e:
        print('Error encountered while building!')
        print()
        print(e)
        return 1

    if args['--browser']:
        index_page = os.path.join(b.output_dir, 'index.html')
        subprocess.Popen('xdg-open "{}"'.format(index_page), shell=True)

    return 0


def init(args):
    """
    Set up a basic wiki that the user can build from.
    """
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


def watch(args):
    """
    Watch for changes and rebuild pages if they are edited.
    """
    print('Doing initial build...')
    build(args)

    from . import notify

    config = {
            'wiki-dir': args['--source-dir'],
            'output-dir': args['--output-dir'],
            }
    b = markdoc2.Builder(config)
    notify.auto_build(b)


def main():
    args = docopt.docopt(__doc__, version=markdoc2.__version__)

    if args['build']:
        sys.exit(build(args))
    elif args['init']:
        sys.exit(init(args))
    elif args['watch']:
        sys.exit(watch(args))


if __name__ == "__main__":
    main()



