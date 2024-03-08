# Gateway Service
The gateway service exposes an interim REST API entrypoint into the Information Querying Component of eCAPTION to supply URLs to be scraped and indexed.

In the future, these URLs will be sent over by the Telegram chatbot layer directly through the `Topic.NEW_ARTICLE_URL` Kafka topic.

### Local Development
1. Ensure the `.env` file is set up and configured in the root directory (e.g. in the root directory, run `cp .env.example .env` and update the relevant variables).
2. Navigate to the `gateway` directory (e.g. run `cd gateway`)
3. Run the following command to start the gateway service in development mode.
    ```bash
    uvicorn main:app --reload
    ```

4. Navigate to `http://localhost:8000` to access the REST API.
5. You can supply a URL (e.g. `https://www.example.com`) to the Information Querying Component via `http://localhost:8000/relatedarticles?url=https://www.example.com`.

### Extensions
1. Integrate the Information Querying Component with the Telegram chatbot layer. This gateway service can then be removed entirely.
    > NOTE: Alternatively, this gateway service can be maintained solely for development work of the Information Querying Component without needing to set up the Telegram bot layer.
