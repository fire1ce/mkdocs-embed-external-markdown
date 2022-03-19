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

## Version 2.xx

**Braking change: Section name must include Markdown Section header like: `## Section name`**

Change log:

- [x] Added support for multi level sections such as `### Section name` and `#### Section name`
- [x] Better Handling of parsing makrdowns wich contains `#` in the content

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

## Usage

- Section defined by **"##"** header (h2)
- **"#"** header (h1) will be **removed** from sorce content so you can use use your own header
- **"##"** header (h2) will be **removed** from sorce **section** content so you can use use your own header
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

- [ ] Embedding links without `.md` extension not working properly

## License

### MIT License

Copyright© 3os.org @ 2022

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to
deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
sell copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NON-INFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
