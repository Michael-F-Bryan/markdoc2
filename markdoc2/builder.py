from collections import namedtuple
import os

from . import TEMPLATE_DIR
from .render import Page

Crumb = namedtuple('Crumb', ['name', 'href'])



class Builder:
    """
    An object to handle all the parts of the wiki building process.
    """

    def __init__(self, config=None):
        self.config = config or {}

        self.root_path = os.path.abspath(self.config.get('wiki-root', '.'))

        self.wiki_dir = os.path.join(self.root_path,
                self.config.get('wiki-dir', 'wiki'))
        self.output_dir = os.path.join(self.root_path,
                self.config.get('output-dir', '_html'))
        self.template_dir = os.path.join(self.root_path,
                self.config.get('template-dir', TEMPLATE_DIR))

        # Make sure we can handle at least markdown documents
        if 'document-extensions' not in self.config:
            self.config['document-extensions'] = ['md']

    def _valid_extension(self, filename):
        """
        Check if a file is part of the wiki.
        """
        return any(filename.endswith(ext)
                for ext in self.config['document-extensions'])

    def walk(self):
        """
        Walk through the wiki, yielding info for each document.

        For each document encountered, a `(filename, crumbs)` tuple will be
        yielded.
        """
        for dirpath, subdirs, files in os.walk(self.wiki_dir):
            # Skip hidden stuff
            subdirs = filter(lambda d: not d.startswith('.'), subdirs)
            files = filter(lambda d: not d.startswith('.'), files)

            for filename in filter(self._valid_extension, files):
                full_filename = os.path.join(dirpath, filename)
                rel_name = os.path.relpath(full_filename, start=self.wiki_dir)
                name = os.path.basename(rel_name)
                dirs = rel_name.split('/')[:-1]

                crumbs = []

                # Add the root dir
                crumbs.append(Crumb('index', '/'))

                # Add all other parent directories
                for d in dirs:
                    href = os.path.join(crumbs[-1].href, d) + '/'
                    temp = Crumb(d, href)
                    crumbs.append(temp)

                # Then add the page itself
                crumbs.append(Crumb(name, None))
                yield name, crumbs

    def paths_to_pages(self):
        directories = {}
        pages = []

        for filename, crumbs in self.walk():
            path = '/'.join(c.name for c in crumbs)
            full_path = os.path.join(self.wiki_dir, path)
            page = Page(full_path, self.template_dir)

            print(page)


