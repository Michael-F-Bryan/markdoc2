import os
import pytest
import jinja2
from bs4 import BeautifulSoup

from markdoc2.render import Page, Directory
from markdoc2.builder import Crumb
import markdoc2


TEST_DIR = os.path.abspath(os.path.dirname(__file__))
DUMMY_WIKI = os.path.join(TEST_DIR, '_wiki')



class TestPage:
    def test_init(self):
        filename = os.path.join(DUMMY_WIKI, 'index.md')
        path = os.path.relpath(filename, start=DUMMY_WIKI)
        crumbs = [Crumb('index', '/'), Crumb('index.md', None)]

        p = Page(path, crumbs, markdoc2.TEMPLATE_DIR, DUMMY_WIKI)

        assert p.path == path
        assert p.wiki_dir == DUMMY_WIKI
        assert p.template_dir == markdoc2.TEMPLATE_DIR
        assert isinstance(p.env, jinja2.Environment)
        assert p.crumbs == crumbs

    def test_render_markdown(self, page):
        should_be = ['<h1>Heading</h1>',
                '<p>This is some text.</p>']
        should_be = '\n'.join(should_be)

        md = page.render_markdown()
        assert md == should_be

    def test_render_html(self, page):
        md = page.render_markdown()
        html = page.render()
        assert md in html

    def test_eq(self):
        filename = os.path.join(DUMMY_WIKI, 'index.md')
        crumbs = [Crumb('index', '/'), Crumb('index.md', None)]
        p1 = Page(filename, crumbs, markdoc2.TEMPLATE_DIR, DUMMY_WIKI)
        p2 = Page(filename, crumbs, markdoc2.TEMPLATE_DIR, DUMMY_WIKI)

        another_filename = os.path.join(DUMMY_WIKI, 'stuff.md')
        more_crumbs = [Crumb('index', '/'), Crumb('stuff.md', None)]
        p3 = Page(another_filename, markdoc2.TEMPLATE_DIR, more_crumbs, DUMMY_WIKI)

        assert p1 is not p2
        assert p1.path == p2.path
        assert p1.template_dir == p2.template_dir
        assert p1.crumbs == p2.crumbs
        assert p1 == p2
        assert p1 != p3


class TestDirectory:
    def test_init(self):
        crumbs = [Crumb('index', '/')]
        path = os.path.relpath(DUMMY_WIKI, start=DUMMY_WIKI)
        d = Directory(path, crumbs, markdoc2.TEMPLATE_DIR, DUMMY_WIKI)
        assert d.path == path
        assert d.wiki_dir == DUMMY_WIKI
        assert d.crumbs == crumbs
        assert d.children == []

    def test_add_child(self, page, directory):
        assert directory.children == []
        directory.add_child(page)
        assert directory.children == [page]

    def test_eq(self, page):
        crumbs = [Crumb('index', '/')]
        path = os.path.relpath(DUMMY_WIKI, start=DUMMY_WIKI)
        d1 = Directory(path, crumbs, markdoc2.TEMPLATE_DIR, DUMMY_WIKI)
        d2 = Directory(path, crumbs, markdoc2.TEMPLATE_DIR, DUMMY_WIKI)
        d3 = Directory(path, crumbs, markdoc2.TEMPLATE_DIR, DUMMY_WIKI)

        d1.add_child(page)
        d2.add_child(page)

        assert d1.path == d2.path
        assert d1.crumbs == d2.crumbs
        assert d1.children == d2.children
        assert d1 == d2

        assert d1.children != d3.children
        assert d1 != d3

    def test_render_html(self, directory):
        html = directory.render()
