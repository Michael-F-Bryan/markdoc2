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
    crumbs = [Crumb('index', '/'), Crumb('index.md', None)]
    return Page('index.md', crumbs, TEMPLATE_DIR, DUMMY_WIKI)


@pytest.fixture
def directory():
    path = os.path.relpath(DUMMY_WIKI, start=DUMMY_WIKI)
    crumbs = [Crumb('index', '/')]
    return Directory(path, crumbs, TEMPLATE_DIR, DUMMY_WIKI)


@pytest.fixture
def builder(request):
    temp_dir = tempfile.mkdtemp()
    config = {
            'wiki-dir': DUMMY_WIKI,
            'output-dir': temp_dir,
            }
    b = Builder(config)
    request.addfinalizer(lambda: shutil.rmtree(temp_dir))
    return b

