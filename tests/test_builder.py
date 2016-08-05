import os

import pytest

from markdoc2.builder import Builder


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
        assert b.wiki_dir == './wiki'

    def test_init_with_config(self):
        config = {
                'document-extensions': ['md', 'markdown'],
                'wiki-dir': 'stuff',
                }

        b = Builder(config)
        assert b.config == config
        assert b.wiki_dir == 'stuff'

    def test_valid_filename(self, builder):
        good_filenames = ['stuff.md', '/path/to/page.md']
        for filename in good_filenames:
            assert builder._valid_extension(filename)

        bad_filenames = ['stuff.pdf', '/path/to/page.md.csv']
        for filename in bad_filenames:
            assert not builder._valid_extension(filename)

    def test_walk(self, builder):
        should_be = [
                ('index.md', ['/']),
                ('stuff.md', ['/', 'subdir']),
                ]

        got = list(builder.walk())
        assert got == should_be
