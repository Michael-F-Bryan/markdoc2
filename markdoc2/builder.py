
import os


class Builder:
    """
    An object to handle all the parts of the wiki building process.
    """

    def __init__(self, config=None):
        self.config = config or {}

        self.wiki_dir = self.config.get('wiki-dir', './wiki')

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
                crumbs = ['/'] + rel_name.split('/')[:-1]
                yield os.path.basename(rel_name), crumbs

