import os
import shutil
import tempfile
import pytest
from markdoc2 import Crumb, TEMPLATE_DIR, Directory, Page, Builder


TEST_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(TEST_DIR)
DUMMY_WIKI = os.path.join(TEST_DIR, '_wiki')


@pytest.fixture
def page():
    crumbs = [Crumb('index', '/'), Crumb('home.md', None)]
    return Page('home.md', crumbs, TEMPLATE_DIR, DUMMY_WIKI)


@pytest.fixture
def directory():
    path = os.path.relpath(DUMMY_WIKI, start=DUMMY_WIKI)
    crumbs = [Crumb('index', '/')]
    return Directory(path, crumbs, TEMPLATE_DIR, DUMMY_WIKI)


@pytest.fixture
def builder(request):
    output_dir = tempfile.mkdtemp()

    # Copy the dummy wiki to a temporary directory so we don't alter the
    # original. use mkdtemp() to get a temporary directory name.
    wiki_dir = tempfile.mkdtemp()
    os.rmdir(wiki_dir)
    shutil.copytree(DUMMY_WIKI, wiki_dir)

    config = {
            'wiki-dir': wiki_dir,
            'output-dir': output_dir,
            }
    b = Builder(config)
    request.addfinalizer(lambda: shutil.rmtree(output_dir))
    request.addfinalizer(lambda: shutil.rmtree(wiki_dir))
    return b
