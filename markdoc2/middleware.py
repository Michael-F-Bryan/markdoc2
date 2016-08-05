# TODO: Test this entire module!!!
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def relative_paths(page, html):
    """
    A middleware function that will transform all links from being absolute
    (starting with "/") to relative.

    Behind the scenes, this goes through all anchor tags, images, iframes,
    script tags,
    """
    soup = BeautifulSoup(html, 'html.parser')
    combos = [
            ('a', 'href'),
            ('link', 'href'),
            ]

    for tag, attr in combos:
        _relative_tag(soup, tag, attr, page)

    return soup.prettify()


def _relative_tag(soup, tag, attr, page):
    """
    Alters the `attr` attribute for each `tag` tag in `soup` to be relative
    instead of absolute. The `soup` object is changed in-place.
    """
    for element in soup.find_all(tag):
        if attr not in element.attrs:
            continue

        href = element[attr]

        parsed = urlparse(href)

        if parsed.netloc or parsed.scheme:
            # Skip all external elements
            continue

        rel_path =_relative(page.href, parsed.path)
        element[attr] = rel_path

def _relative(src, dest):
    """
    Get the path to go from `src` to `dest`.
    """
    rel_path = os.path.relpath(dest, start=os.path.dirname(src))
    if rel_path.endswith('.'):
        rel_path += '/index.html'
    return rel_path

