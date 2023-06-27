# MkDocs Embed External Markdown Plugin

[![PyPI - Downloads][pypi-image]][pypi-url]
[![contributions welcome][contributions-image]][contributions-url]
[![MIT license][license-image]][license-url]

[pypi-image]: https://img.shields.io/pypi/dm/mkdocs-embed-external-markdown
[pypi-url]: https://pypi.org/project/mkdocs-embed-external-markdown/
[contributions-image]: https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat
[contributions-url]: https://github.com/fire1ce/mkdocs-embed-external-markdown
[license-image]: https://img.shields.io/badge/License-MIT-blue.svg
[license-url]: https://mit-license.org/

## About

MkDocs Embed External Markdown plugin that allows to inject **section** or **full markdown** content from a given url.
The goal is to embed different markdown from different sources inside your MkDocs project.

## Installation

Install the package with pip:

```shell
pip install mkdocs-embed-external-markdown
```

## Configuration

Enable the plugin in your `mkdocs.yml` file:

```yaml
plugins:
  - external-markdown
```

## Compatibility with Github private repos

If the GH_TOKEN environment variable is set with an authorized personal access token then the authorization header will be added to the request and content from private repositories can be fetched

## Usage

- Section defined by **"##/###/####..."** header (h2/h3/h4...)
- **"#"** header (h1) will be **removed** from source content so you can use use your own header
- **"##/###/####..."** header (h2/h3/h4...) will be **removed** from source **section** content so you can use use your own header
- Supports multiple **sections** from any source

`external_markdown` requires 2 parameters: **url** and **section name**.

```makrdown
{{ external_markdown('url', '## section name') }}
```

### Full Markdown Content

Embed full markdown content from a given url, you can use the following example:

```markdown
{{ external_markdown('https://raw.githubusercontent.com/fire1ce/DDNS-Cloudflare-Bash/main/README.md', '') }}
```

### Specific Section

Embed markdown section from a given url, you can use the following example:

```markdown
{{ external_markdown('https://raw.githubusercontent.com/fire1ce/DDNS-Cloudflare-Bash/main/README.md', '## Installation') }}
```

## MkDocs Example

The following example shows how to use the plugin in mkdocs project:

````markdown
# Example Page

This is an example page.

## Embedding Multiple Markdown Sections From Different URLs

### First Embedded Section

```markdown
{{ external_markdown('https://raw.githubusercontent.com/mkdocs/mkdocs/master/README.md', '## Features') }}
```

### Second Embedded Section

```markdown
{{ external_markdown('https://raw.githubusercontent.com/squidfunk/mkdocs-material/master/README.md', '## Quick start') }}
```
````

Will produce the following page:

![MkDocs Embed External Markdown Plugin](https://user-images.githubusercontent.com/16795594/155761254-17b47e65-d27e-438b-a476-15bd04fdc3ec.jpg)

## How To Prevent Accidental Interpretation Of `Jinja-like` Statements

The most frequent issue when adding the `MkDocs Embed External Markdown Plugin` to an existing mkdocs project, is that some markdown pages may not be rendered correctly, or cause a syntax error, or some other error.

The reason is that if Jinja2 template engine in the **MkDocs Embed External Markdown Plugin** meets any text that has the standard markers (typically starting with `{%`} or `{{`) this will cause a conflict: it will try to interpret that text as a macro and fail to behave properly.

The most likely places where this can occur are the following:

| Location in Markdown file (Block or Inline) | Description                                                                                                |
| ------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| **Code**                                    | Documented Jinja2 statements (or similar syntax), LaTeX                                                    |
| **Maths**                                   | LaTeX statements                                                                                           |
| _*Elsewhere*_                               | Some pre-existing templating or macro language, typically with some constructs starting with `{#` or `{{`. |

### Code Blocks Containing Similar Languages

With MkDocs, this situation typically occurs when the website
is documenting an application that relies on a
[djangolike/jinjalike language](https://medium.com/@i5ar/template-languages-a7b362971cbc) like:

- Django Template Language
- Jinja2 (Python)
- Nunjucks (Javascript)
- Twig (PHP)
- ...

This may also happen for pages that documents
[Ansible](https://ansible-docs.readthedocs.io/zh/stable-2.0/rst/intro.html) directives, which often contain
[variables expressed in a Jinja2 syntax](https://ansible-docs.readthedocs.io/zh/stable-2.0/rst/playbooks_variables.html#using-variables-about-jinja2).

### Solutions - Explicitly Marking The Snippets as `raw`

````markdown
{% raw %}

```bash
docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container_name_or_id
```

{% endraw %}
````

## Known Issues

- [ ]

## Changelog

### Version 3.xx

Version 3.0.1 (2023-06-21)

Fixed:

- [x] Crash caused by conflict with Jinja2 render engine expects `config` parameter from other 3rd party plugins.

Version 3.0.0 (2023-06-20)

Added

- [x] Modularized the code into separate methods for improved readability and maintainability.
- [x] Added type hints for better code understanding and possible performance improvements.
- [x] Included regex pre-compilation for performance enhancement.
- [x] Enhanced URL validation to check for the structure of a URL rather than just the presence of .md.
- [x] Improved error logging through the use of logger.warning instead of print statements, which integrates with MkDocs' logging system.
- [x] Added handling for relative links in the markdown, making them absolute based on the base URL.
- [x] Introduced better error handling for Connection Errors and Status Codes through optional return types.

Removed:

- [x] Removed the use of sys.exit(1) on error, allowing the MkDocs build process to continue even if the plugin encounters an issue.
- [x] Removed the strict requirement for a section level at the beginning of a section name.

Changed

- [x] Switched from using re.compile for one-time regex patterns to using re.match or re.search.
- [x] Extracted the GitHub token once at the beginning of the request method instead of multiple times.
- [x] Replaced the check for .md at the end of the URL with a more comprehensive regular expression to validate the URL's structure.

Fixed:

- [x] Handling of section extraction is now more robust and less prone to errors.

Please note that this is a major version update and may contain breaking changes. Carefully read the updated documentation and test the plugin thoroughly before upgrading in a production environment.

### Version 2.xx Changelog Archive

**Braking change: Section name must include Markdown Section header like: `## Section name`**

Changelog:

- [x] Add ability to import content from private github repositories. Thanks to @sd0408
- [x] Added support for multi level sections such as `### Section name` and `#### Section name`
- [x] Better Handling of parsing makrdowns wich contains `#` in the content
- [x] Failing Mkdocs Build when Markdown content cannot be fetched

## License

This project is licensed under the terms of the [MIT License](LICENSE.md).
