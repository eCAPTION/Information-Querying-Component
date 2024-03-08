# Web Scraper Service
The web scraper service takes in a URL and scrapes it, returning the article's text and corresponding metadata.

It currently supports the following features:
1. Whitelisting of URLs
   - Must be configured in the `.whitelist` file under the `web_scraper` directory.
2. Stripping of URL query/ hash parameters
   - Supplied URLs will have their URL parameters removed before being sent for scraping and eventual indexing.

> NOTE: URLs must be supplied with the HTTPS prefix (e.g. `https://`).

### Local Development
1. Ensure the `.env` file is set up and configured in the root directory (e.g. in the root directory, run `cp .env.example .env` and update the relevant variables).
2. Navigate to the `web_scraper` directory (e.g. run `cd web_scraper`)
3. Install the dependencies (e.g. run `pip3 install -r requirements.txt`, preferably in a virtual environment)
4. Run the following command to start the web scraper service in development mode.
    ```bash
    faust -A main worker -l info
    ```

### Extensions
1. Implement periodic scraping of news sites to pre-populate the news search index with the latest news (so that the latest news have relevant results show up too).
2. Consider implementing a caching layer before the web scraper service to return cached results before a set TTL to improve speed for repeated queries in quick succession.
