"""
Module for rendering an individual page from markdown to HTML.
"""

import os

import markdown
import jinja2


class Page:
    def __init__(self, filename, template_dir, crumbs):
        self.filename = filename
        self.template_dir = template_dir
        self.crumbs = crumbs

        self.env = jinja2.Environment(
            autoescape=False,
            loader=jinja2.FileSystemLoader(self.template_dir),
            trim_blocks=False)

    def render_markdown(self):
        text = open(self.filename).read()
        return markdown.markdown(text)

    def render_html(self, md_text):
        template = self.env.get_template('document.html')
        return template.render(
                content=md_text,
                crumbs=self.crumbs)

    def __eq__(self, other):
        return (self.filename == other.filename and
                self.template_dir == other.template_dir and
                sorted(self.crumbs) == sorted(other.crumbs))

    def __repr__(self):
        return '<{}: {}>'.format(
                self.__class__.__name__,
                self.filename)


class Directory:
    def __init__(self, path, crumbs, template_dir):
        self.path = path
        self.crumbs = crumbs
        self.template_dir = template_dir
        self.children = []

        self.env = jinja2.Environment(
            autoescape=False,
            loader=jinja2.FileSystemLoader(self.template_dir),
            trim_blocks=False)

    def add_child(self, child):
        self.children.append(child)

    def render_html(self):
        template = self.env.get_template('listing.html')
        return template.render(children=self.children)

    def __repr__(self):
        return '<{}: {} ({} {})>'.format(
                self.__class__.__name__,
                self.path,
                len(self.children),
                'children' if len(self.children) != 1 else 'child')

    def __eq__(self, other):
        return (self.path == other.path and
                sorted(self.children, key=lambda c: c.filename) ==
                    sorted(other.children, key=lambda c: c.filename))

