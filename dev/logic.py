from requests import get, exceptions
from re import compile, match, MULTILINE
from sys import exit


# url = "https://raw.githubusercontent.com/fire1ce/DDNS-Cloudflare-PowerShell/main/README.md"
# section_name = "License"
# section_name = "License"

url = "https://raw.githubusercontent.com/wsargent/docker-cheat-sheet/master/READMEdd.md"
section_name = "## CPU Constraints"

# check if url is valid and had ".md" extension
def is_valid_url(url):
    if not match(r"^https?:\/\/.*\.md$", url):
        exit(f"Error! {url} is not a valid markdown url")
    return True


# get markdown from url if status code is 200
def get_markdown_from_url(url):
    try:
        response = get(url)
        if response.status_code == 200:
            # remove the heading
            markdown = response.text
            markdown = markdown[markdown.find("\n") + 1 :]
            return markdown
        else:
            exit(f"Error! {url} returned status code: {str(response.status_code)}")
    except exceptions.ConnectionError:
        exit(f"Error! {url} returned connection error")


# get the section content from markdown
def get_section_from_markdown(markdown, section_name):
    # Get the section level from section_name
    try:
        section_level = compile("^#+ ").search(section_name).span()[1] - 1
    except:
        exit(
            f"Error! Missing markdown section level at the beginning of section name: {section_name}"
        )
    # Gets the srart index of the section from markdown
    try:
        start_index = compile("^" + section_name + "$", MULTILINE).search(markdown).span()[1]
    except:
        exit(f'Error! Section: "{section_name}" not found in markdown {url}')
    # Gets the end index of the section from markdown (last section handle)
    try:
        end_index = (
            compile("^#{2," + str(section_level) + "} ", MULTILINE)
            .search(markdown[start_index:])
            .span()[0]
        )
        markdown = markdown[start_index : end_index + start_index]
    except:
        markdown = markdown[start_index:]
    return markdown


# get the markdown from url or markdown section
def external_markdown(url, section_name):
    is_valid_url(url)
    if section_name:
        markdown = get_markdown_from_url(url)
        if markdown:
            return get_section_from_markdown(markdown, section_name)
    else:
        return get_markdown_from_url(url)


print(external_markdown(url, section_name))
