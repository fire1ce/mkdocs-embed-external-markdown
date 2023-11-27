import pytest

from external_markdown.plugin import EmbedExternalMarkdown

BASE_URL = "https://BASEURL/"
BASE_FILE = "https://BASEURL/FILE.md"
TEST_DATA = [
    (
        "external link",
        "https://github.com",
        "https://github.com"),
    (
        "external link with anchor",
        "https://ansible-docs.readthedocs.io/zh/stable-2.0/rst/playbooks_variables.html#using-variables-about-jinja2",
        "https://ansible-docs.readthedocs.io/zh/stable-2.0/rst/playbooks_variables.html#using-variables-about-jinja2",
    ),
    (
        "anchor",
        "#links",
        "#links"),
    (
        "local link",
        "page.md",
        f"{BASE_URL}page.md"),
    (
        "local link with anchor",
        "page.md#test-subsection",
        f"{BASE_URL}page.md#test-subsection",
    ),
]


class TestEmbedExternalMarkdown:
    @pytest.mark.parametrize("label,link_url,expected_url", TEST_DATA)
    def test_update_relative_links_external(self, label, link_url, expected_url):
        # Regression tests for #11
        link = f"[{label}]({link_url})"
        expected = f"[{label}]({expected_url})"
        assert EmbedExternalMarkdown().update_relative_links(link, BASE_FILE) == expected
