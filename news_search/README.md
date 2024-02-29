## Installing dependencies
```bash
cd news_search
pip install -r requirements.txt
```

## OpenSearch Setup
1. Install OpenSearch on your local machine, or run the Dockerized container with instructions [here](https://opensearch.org/docs/latest/install-and-configure/install-opensearch/docker/)
2. In the `news_search` directory, run `python -m scripts.opensearch_setup` to run the OpenSearch setup script to set up the index for the news search component.

## Running locally
1. Setup the `.env` file at the root of the repository (by copying and modifying `.env.example`).
2. Startup the OpenSearch instance (and setup the index if yet to be done).
3. Run the following command to start the faust worker on localhost with debug info enabled:
```bash
faust -A main worker -l info
```
