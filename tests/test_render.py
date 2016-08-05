import os
import pytest

from markdoc2.render import Page


TEST_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(TEST_DIR)
DUMMY_WIKI = os.path.join(TEST_DIR, '_wiki')


class TestPage:
    def test_init(self):
        filename = os.path.join(DUMMY_WIKI, 'index.md')
        template_dir = os.path.join(PROJECT_ROOT, 'markdoc2', 'static', 'templates')

        p = Page(filename, template_dir)

        assert p.filename == filename
        assert p.template_dir == template_dir
