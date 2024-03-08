# News Search Service
The news search service takes in the text, metadata content and subgraph embedding of a particular URL and stores them in a reversed index such as OpenSearch. The entries are then indexed and queried using the weighted sum similarity score outlined in the NewsLink paper.

### Local Development
1. Ensure the `.env` file is set up and configured in the root directory (e.g. in the root directory, run `cp .env.example .env` and update the relevant variables).
2. Navigate to the `news_search` directory (e.g. run `cd news_search`)
3. Install the dependencies (e.g. run `pip3 install -r requirements.txt`, preferably in a virtual environment).
4. Install and run an instance of OpenSearch and update the relevant variables in the `.env` file.
5. Run the following command to start the web scraper service in development mode.
    ```bash
    faust -A main worker -l info
    ```

### OpenSearch Setup
1. Install OpenSearch on your local machine, or run the Dockerized container with instructions [here](https://opensearch.org/docs/latest/install-and-configure/install-opensearch/docker/)
2. In the `news_search` directory, run `python -m scripts.opensearch_setup` to run the OpenSearch setup script to set up the index for the news search component.

### Extensions
1. Other metrics of similarity scoring could be included, such as favoring articles from diversified viewpoints.
