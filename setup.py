import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="mkdocs-embed-external-markdown",
    version="0.0.14",
    url="https://github.com/fire1ce/mkdocs-embed-external-markdown",
    license="MIT",
    author="Stas Yakobov",
    author_email="dev@3os.org",
    description="Mkdocs plugin that allow to inject external markdown or markdown section from given url",
    install_requires=["mkdocs", "requests", "jinja2"],
    keywords=["mkdocs", "plugin", "markdown", "external"],
    packages=find_packages(exclude=["*.tests"]),
    entry_points={
        "mkdocs.plugins": "external-markdown = external_markdown.plugin:externalMarkdown"
    },
)
