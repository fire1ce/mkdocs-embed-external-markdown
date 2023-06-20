import os
import logging
import re
from mkdocs.plugins import BasePlugin
from requests import get, ConnectionError, Response
from jinja2 import Template
from urllib.parse import urljoin
from typing import Optional

# Pre-compile regular expressions
SECTION_LEVEL_REGEX = re.compile("^#+ ", re.IGNORECASE)
LINK_PATTERN_REGEX = re.compile(r"\[(?P<alt_text>[^\]]*)\]\((?P<link_url>[^\)]*)\)", re.MULTILINE | re.IGNORECASE)

logger = logging.getLogger("mkdocs.plugins")


class EmbedExternalMarkdown(BasePlugin):
    """
    A MkDocs plugin to embed external Markdown content into the documentation.
    """

    def is_valid_url(self, url: str) -> bool:
        """
        Check if the provided URL is valid and is a markdown file.
        """
        # Regex pattern to validate URLs
        pattern = re.compile(
            r"http[s]?://"  # http:// or https://
            r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain...
            r"localhost|"  # localhost...
            r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
            r"(?::\d+)?"  # optional port
            r"(?:/?|[/?]\S+)$",
            re.IGNORECASE,
        )

        # Check if URL is valid and ends with .md
        if re.match(pattern, url) and url.lower().endswith(".md"):
            return True
        else:
            logger.warning(f"{url} is not a valid markdown URL")
            return False

    def make_request(self, url: str) -> Optional[Response]:
        """
        Make a GET request to the specified URL and return the response.
        """
        try:
            headers = {}
            gh_token = os.getenv("GH_TOKEN")
            if gh_token:
                headers = {"Authorization": "token " + gh_token}

            return get(url, headers=headers)
        except ConnectionError:
            logger.warning(f"{url} returned connection error")
            return None

    def get_markdown_from_response(self, response: Response, url: str) -> Optional[str]:
        """
        Extract markdown text from the response object.
        """
        if response.status_code == 200:
            markdown = response.text
            return markdown[markdown.find("\n") + 1 :]
        else:
            logger.warning(f"{url} returned status code: {str(response.status_code)}")
            return None

    def get_section_level(self, section_name: str) -> Optional[int]:
        """
        Get the level of the section based on markdown headers (e.g., ##, ###, etc.)
        """
        try:
            return SECTION_LEVEL_REGEX.search(section_name).span()[1] - 1
        except AttributeError:
            logger.warning(f"Missing markdown section level at the beginning of section name: {section_name}")
            return None

    def extract_section_from_markdown(
        self, markdown: str, section_name: str, section_level: int, url: str
    ) -> Optional[str]:
        """
        Extract a specific section from the markdown text.
        """
        try:
            section_pattern = f"^{section_name.strip()}(?:[^#]|$)"
            start_index = re.compile(section_pattern, re.MULTILINE | re.IGNORECASE).search(markdown).span()[1]
        except AttributeError:
            logger.warning(f'Section: "{section_name}" not found in markdown {url}')
            return None

        try:
            end_index = (
                re.compile("^#{2," + str(section_level) + "} ", re.MULTILINE | re.IGNORECASE)
                .search(markdown[start_index:])
                .span()[0]
            )
            return markdown[start_index : end_index + start_index]
        except AttributeError:
            return markdown[start_index:]

    def update_relative_links(self, markdown: str, base_url: str) -> str:
        """
        Update relative links in markdown to absolute links.
        """

        def replace_link(match):
            link_url = urljoin(base_url, match.group("link_url"))
            return f'[{match.group("alt_text")}]({link_url})'

        return LINK_PATTERN_REGEX.sub(replace_link, markdown)

    def external_markdown(self, url: str, section_name: Optional[str] = None) -> str:
        """
        Retrieve and process external markdown content from the specified URL.
        Optionally extract a section if section_name is provided.
        """
        if not self.is_valid_url(url):
            return ""

        response = self.make_request(url)
        if response is None:
            return ""

        markdown = self.get_markdown_from_response(response, url)
        if markdown is None:
            return ""

        markdown = self.update_relative_links(markdown, url)

        if section_name:
            section_level = self.get_section_level(section_name)
            if section_level is not None:
                markdown = self.extract_section_from_markdown(markdown, section_name, section_level, url) or ""
            else:
                markdown = ""

        return markdown

    def on_page_markdown(self, markdown: str, config, **kwargs) -> str:
        """
        Render the markdown content using the Jinja2 template engine.
        """
        return Template(markdown).render(external_markdown=self.external_markdown, config=config)
