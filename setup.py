from setuptools import setup

setup(
    name="mkdocs-embed-external-markdown",
    version="220224",
    url="https://github.com/fire1ce/mkdocs-embed-external-markdown",
    license="MIT",
    author="Stas Yakobov",
    author_email="dev@3os.org",
    description="Mkdocs plugin that allow to inject external markdown or markdown section from given url",
    install_requires=["mkdocs"],
    # The following rows are important to register your plugin.
    # The format is "(plugin name) = (plugin folder):(class name)"
    # Without them, mkdocs will not be able to recognize it.
    entry_points={
        "mkdocs.plugins": [
            "external-markdown = external_markdown.plugin:externalMarkdown",
        ]
    },
)
