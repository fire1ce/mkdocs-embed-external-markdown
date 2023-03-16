import os
from setuptools import setup, find_packages
from pathlib import Path


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# read the contents of your README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
    name="mkdocs-embed-external-markdown",
    version='',  # This line will be replaced by the version from .bumpversion.cfg
    url="https://github.com/fire1ce/mkdocs-embed-external-markdown",
    license="MIT",
    author="Stas Yakobov",
    author_email="dev@3os.org",
    description="Mkdocs plugin that allows injecting external markdown or markdown sections from a given URL",
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=["mkdocs", "requests", "jinja2"],
    keywords=["mkdocs", "plugin", "markdown", "external"],
    packages=find_packages(exclude=["*.tests"]),
    entry_points={"mkdocs.plugins": "external-markdown = external_markdown.plugin:EmbedExternalMarkdown"},
)
