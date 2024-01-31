from trafilatura import fetch_url, extract


def get_text_from_article_url(url: str) -> str:
    downloaded = fetch_url(url)
    if downloaded:
        return extract(downloaded)
    else:
        raise Exception("Invalid URL provided!")
