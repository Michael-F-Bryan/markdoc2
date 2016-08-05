import os
import pytest

from markdoc2.builder import Builder, Crumb
from markdoc2.render import Page, Directory
import markdoc2



TEST_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(TEST_DIR)
DUMMY_WIKI = os.path.join(TEST_DIR, '_wiki')

@pytest.fixture
def builder():
    config = {
            'wiki-dir': DUMMY_WIKI,
            }
    b = Builder(config)
    return b


class TestBuilder:
    def test_init(self):
        b = Builder()
        assert b.config == {'document-extensions': ['md']}
        assert b.wiki_dir == os.path.abspath('wiki')

    def test_init_with_config(self):
        config = {
                'document-extensions': ['md', 'markdown'],
                'wiki-dir': 'stuff',
                }

        b = Builder(config)
        assert b.config == config
        assert b.wiki_dir == os.path.abspath('stuff')

    def test_valid_filename(self, builder):
        good_filenames = ['stuff.md', '/path/to/page.md']
        for filename in good_filenames:
            assert builder._valid_extension(filename)

        bad_filenames = ['stuff.pdf', '/path/to/page.md.csv']
        for filename in bad_filenames:
            assert not builder._valid_extension(filename)

    def test_walk(self, builder):
        should_be = [
                ('index.md', [
                    Crumb('index', '/'),
                    Crumb('index.md', None)]),
                ('another_page.md', [
                    Crumb('index', '/'),
                    Crumb('another_page.md', None)]),
                ('stuff.md', [
                    Crumb('index', '/'),
                    Crumb('subdir', '/subdir/'),
                    Crumb('stuff.md', None)]),
                ]

        got = list(builder.walk())
        assert got == should_be

    def test_paths_to_pages(self, builder):
        # Note that this test takes a lot of lines due to
        # the amount of setup required :(
        template_dir = os.path.join(PROJECT_ROOT, 'markdoc2', 'static', 'templates')

        # Create the directories
        crumbs = [Crumb('index', '/')]
        d1 = Directory('.', crumbs, markdoc2.TEMPLATE_DIR, DUMMY_WIKI)
        more_crumbs = [Crumb('index', '/'), Crumb('subdir', '/subdir/')]
        d2 = Directory('subdir', more_crumbs, markdoc2.TEMPLATE_DIR, DUMMY_WIKI)

        # /index.md
        crumbs = [Crumb('index', '/'),
                Crumb('index.md', None)]
        p1 = Page('index.md', crumbs, template_dir, DUMMY_WIKI)
        d1.add_child(p1)

        # /another_page.md
        crumbs = [Crumb('index', '/'),
                Crumb('another_page.md', None)]
        p2 = Page('another_page.md', crumbs, template_dir, DUMMY_WIKI)
        d1.add_child(p2)

        # /subdir/stuff.md
        crumbs = [Crumb('index', '/'),
                Crumb('subdir', '/subdir/'),
                Crumb('stuff.md', None)]
        p3 = Page('subdir/stuff.md', crumbs, template_dir, DUMMY_WIKI)
        d2.add_child(p3)

        directories_should_be = {
                '.': d1,
                'subdir': d2,
                }
        pages_should_be = [p1, p2, p3]

        # Get the directories and pages
        directories, pages = builder.paths_to_pages()

        assert pages == pages_should_be
        assert directories == directories_should_be
