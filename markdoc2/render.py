"""
Module for rendering an individual page from markdown to HTML.
"""

import os

import markdown
import jinja2


class BasePage:
    """
    The base class containing functionality common to both Page and Directory.
    """
    def __init__(self, path, crumbs, template_dir, wiki_dir):
        """
        Parameters
        ----------
        path: str
            The location of the document, relative to the wiki's root.
        crumbs: list(Crumb)
            A list of breadcrumbs that lead from the wiki root to the document.
        template_dir: str
            The directory containing templates to use when rendering as html.
        wiki_dir: str
            The absolute location of the wiki's source files on disk.
        """
        self.path = path
        self.template_dir = template_dir
        self.crumbs = crumbs
        self.wiki_dir = wiki_dir

        self.env = jinja2.Environment(
            autoescape=False,
            loader=jinja2.FileSystemLoader(self.template_dir),
            trim_blocks=False)

    def render(self):
        raise NotImplementedError

    @property
    def fullpath(self):
        return os.path.join(self.wiki_dir, self.path)

    def __eq__(self, other):
        return (self.path == other.path and
                self.template_dir == other.template_dir and
                sorted(self.crumbs) == sorted(other.crumbs))



class Page(BasePage):
    def render_markdown(self):
        text = open(self.fullpath).read()
        return markdown.markdown(text)

    def render(self):
        md_text = self.render_markdown()
        template = self.env.get_template('document.html')
        return template.render(
                content=md_text,
                crumbs=self.crumbs)

    def __repr__(self):
        return '<{}: {}>'.format(
                self.__class__.__name__,
                self.path)


class Directory(BasePage):
    def __init__(self, path, crumbs, template_dir, wiki_dir):
        """
        Parameters
        ----------
        path: str
            The location of the document, relative to the wiki's root.
        crumbs: list(Crumb)
            A list of breadcrumbs that lead from the wiki root to the document.
        template_dir: str
            The directory containing templates to use when rendering as html.
        wiki_dir: str
            The absolute location of the wiki's source files on disk.
        """
        super().__init__(path, crumbs, template_dir, wiki_dir)
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def render(self):
        template = self.env.get_template('listing.html')
        return template.render(
                children=self.children,
                crumbs=self.crumbs)

    def __repr__(self):
        return '<{}: {} ({} {})>'.format(
                self.__class__.__name__,
                self.path,
                len(self.children),
                'children' if len(self.children) != 1 else 'child')

    def __eq__(self, other):
        return (super().__eq__(other) and
                sorted(self.children, key=lambda c: c.path) ==
                    sorted(other.children, key=lambda c: c.path))

