from trafilatura import fetch_url, bare_extraction
from urllib.parse import ParseResult

whitelisted_domains: set[str] = set()
with open(".whitelist", "rb") as file:
    whitelisted_domains = set([url.strip().decode() for url in file])


def is_https(parsed_url: ParseResult) -> bool:
    return parsed_url.scheme == "https"


def check_whitelist(parsed_url: ParseResult) -> bool:
    return parsed_url.hostname in whitelisted_domains


def extract_article_url(url: str) -> dict[str, str]:
    downloaded = fetch_url(url)
    if downloaded:
        extracted: dict[str, str] = bare_extraction(downloaded)

        return {
            "title": extracted.get("title"),
            "description": extracted.get("description"),
            "text": extracted.get("text"),
            "image": extracted.get("image"),
        }

    else:
        raise Exception("Invalid URL provided!")
