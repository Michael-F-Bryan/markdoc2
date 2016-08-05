import os
import pytest
import jinja2
from bs4 import BeautifulSoup

from markdoc2.render import Page, Directory


TEST_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(TEST_DIR)
DUMMY_WIKI = os.path.join(TEST_DIR, '_wiki')


@pytest.fixture
def page():
        filename = os.path.join(DUMMY_WIKI, 'index.md')
        template_dir = os.path.join(PROJECT_ROOT, 'markdoc2', 'static', 'templates')

        return Page(filename, template_dir)

@pytest.fixture
def directory():
        path = os.path.join(DUMMY_WIKI, 'subdir')
        return Directory(path)


class TestPage:
    def test_init(self):
        filename = os.path.join(DUMMY_WIKI, 'index.md')
        template_dir = os.path.join(PROJECT_ROOT, 'markdoc2', 'static', 'templates')

        p = Page(filename, template_dir)

        assert p.filename == filename
        assert p.template_dir == template_dir
        assert isinstance(p.env, jinja2.Environment)

    def test_render_markdown(self, page):
        should_be = ['<h1>Heading</h1>',
                '<p>This is some text.</p>']
        should_be = '\n'.join(should_be)

        md = page.render_markdown()
        assert md == should_be

    def test_render_html(self, page):
        md = page.render_markdown()
        html = page.render_html(md)

        assert md in html


class TestDirectory:
    def test_init(self):
        d = Directory(DUMMY_WIKI)
        assert d.path == DUMMY_WIKI
        assert d.children == []

    def test_add_child(self, page, directory):
        assert directory.children == []
        directory.add_child(page)
        assert directory.children == [page]
