"""
A Python 3 version of `Markdoc <http://markdoc.org/>`.
"""

import os

# Put definitions for constants above to prevent circular imports
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
STATIC_DIR = os.path.join(PROJECT_ROOT, 'static')
TEMPLATE_DIR = os.path.join(STATIC_DIR, 'templates')

# flake8: NOQA
from .builder import Builder, Crumb
from .render import Page, Directory
from .exceptions import MarkdocError, InvalidFileName


__all__ = [
    'PROJECT_ROOT', 'STATIC_DIR', 'TEMPLATE_DIR',
    'Builder', 'Crumb',
    'Page', 'Directory',
    'MarkdocError', 'InvalidFileName',
    ]

__version__ = '0.2.0'

