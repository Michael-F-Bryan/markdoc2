"""
Module for rendering an individual page from markdown to HTML.
"""

import os

import markdown
import jinja2


class Page:
    def __init__(self, filename, template_dir):
        self.filename = filename
        self.template_dir = template_dir

        self.env = jinja2.Environment(
            autoescape=False,
            loader=jinja2.FileSystemLoader(self.template_dir),
            trim_blocks=False)

    def render_markdown(self):
        text = open(self.filename).read()
        return markdown.markdown(text)

    def render_html(self, md_text):
        template = self.env.get_template('document.html')
        return template.render(content=md_text)

    def __repr__(self):
        return '<{}: {}>'.format(
                self.__class__.__name__,
                self.filename)
