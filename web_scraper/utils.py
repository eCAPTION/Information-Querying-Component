from trafilatura import fetch_url, bare_extraction


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
