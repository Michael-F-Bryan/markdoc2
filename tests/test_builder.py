import os

from markdoc2.builder import Builder, Crumb
from markdoc2.render import Page, Directory
import markdoc2


TEST_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(TEST_DIR)
DUMMY_WIKI = os.path.join(TEST_DIR, '_wiki')


class TestBuilder:
    def test_init(self):
        b = Builder()
        assert b.config == {'document-extensions': ['md']}
        assert b.wiki_dir == os.path.abspath('wiki')

    def test_init_with_config(self):
        config = {
                'document-extensions': ['md', 'markdown'],
                'wiki-dir': 'stuff',
                'output-dir': 'outdir',
                }

        b = Builder(config)
        assert b.config == config
        assert b.wiki_dir == os.path.abspath('stuff')
        assert b.output_dir == os.path.abspath('outdir')

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
        template_dir = os.path.join(PROJECT_ROOT,
                                    'markdoc2',
                                    'static',
                                    'templates')

        # Create the directories
        crumbs = [Crumb('index', '/')]
        d1 = Directory('.', crumbs, markdoc2.TEMPLATE_DIR, DUMMY_WIKI)
        more_crumbs = [Crumb('index', '/'), Crumb('subdir', '/subdir/')]
        d2 = Directory('subdir',
                       more_crumbs,
                       markdoc2.TEMPLATE_DIR,
                       DUMMY_WIKI)

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

    def test_create_page(self, builder, page):
        dest = os.path.join(builder.output_dir, page.path)
        parent_dir = os.path.dirname(dest)

        # Make sure the page's file doesn't exist (except if the page is
        # At the wiki root
        if parent_dir != builder.output_dir:
            assert not os.path.exists(parent_dir)

        builder.create_page(page)

        # Now make sure the parent dirs were created
        assert os.path.exists(parent_dir)

        # And that the page's html was written to a file
        html_should_be = page.render()
        html_got = open(dest).read()
        assert html_got == html_should_be
