# NLP Service
The NLP service takes in the text content of a URL supplied by the web scraper component and generates the maximal entity cooccurrence  set as outlined by the NewsLink paper.

Briefly, the text content is split into individual sentences on which named entity linking via [ReFinED](https://github.com/amazon-science/ReFinED) is performed to identify entities (as opposed to exact 'string contains' matching proposed in the original NewsLink paper). Refer to the `get_maximal_entity_cooccurrence_set` function for more details.

### Local Development
1. Ensure the `.env` file is set up and configured in the root directory (e.g. in the root directory, run `cp .env.example .env` and update the relevant variables).
2. Navigate to the `nlp` directory (e.g. run `cd nlp`)
3. Install the dependencies (e.g. run `pip3 install -r requirements.txt`, preferably in a virtual environment).
4. Run the following command to start the web scraper service in development mode.
    ```bash
    faust -A main worker -l info
    ```
