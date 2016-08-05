import os
from glob import glob

from markdoc2.__main__ import build, main


class TestMain:
    def test_build(self, builder):
        args = {
                '--source-dir': builder.wiki_dir,
                '--output-dir': builder.output_dir,
                'build': True,
                }

        # Make sure there's nothing in the output directory
        assert not glob(builder.output_dir + '/*')
        assert 0 == build(args)
        # There should be something there now
        assert glob(builder.output_dir + '/*')


    def test_build_no_source(self, builder):
        args = {
                '--source-dir': '/foo/bar/baz',
                '--output-dir': builder.output_dir,
                'build': True,
                }
        assert build(args) == 1

    def test_build_with_index_md(self, builder):
        args = {
                '--source-dir': builder.wiki_dir,
                '--output-dir': builder.output_dir,
                'build': True,
                }
        index_file = os.path.join(builder.wiki_dir, 'index.md')
        with open(index_file, 'w') as f:
            f.write('')
        assert build(args) == 1
