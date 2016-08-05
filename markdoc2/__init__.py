"""
A Python 3 version of `Markdoc <http://markdoc.org/>`.
"""

import os



__all__ = [
        'PROJECT_ROOT', 'STATIC_DIR', 'TEMPLATE_DIR',
        'Builder', 'Crumb',
        'Page', 'Directory',
        ]

__version__ = '0.1.0'

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(PROJECT_ROOT, 'static')
TEMPLATE_DIR = os.path.join(STATIC_DIR, 'templates')


from markdoc2.builder import Builder, Crumb
from markdoc2.render import Page, Directory
