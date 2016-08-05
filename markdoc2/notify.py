"""
The module allowing a user to watch for changes and rebuild pages
automatically.
"""
import sys
import os
from .render import Page
try:
    import pyinotify
except ImportError:
    print('To use this functionality, you need to be using')
    print('Linux and install `pyinotify`')
    sys.exit(1)


class OnWriteHandler(pyinotify.ProcessEvent):
    def my_init(self, builder):
        self.builder = builder

    def _build(self, filename):
        path = os.path.relpath(filename, self.builder.wiki_dir)
        print('file altered, rebuilding wiki ({})'.format(path))
        self.builder.build()

    def process_default(self, event):
        if all(not event.pathname.endswith(ext) for ext
               in self.builder.config['document-extensions']):
            return
        self._build(event.pathname)


def auto_build(builder):
    path = builder.wiki_dir
    mask = pyinotify.IN_CREATE | pyinotify.IN_CLOSE_WRITE | pyinotify.IN_DELETE

    wm = pyinotify.WatchManager()
    handler = OnWriteHandler(builder=builder)
    notifier = pyinotify.Notifier(wm, handler)

    wm.add_watch(path, mask, rec=True, auto_add=True)

    print('Started monitoring {} (type ctrl-C to exit)'.format(path))
    notifier.loop()
