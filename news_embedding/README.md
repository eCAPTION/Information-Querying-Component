# News Embedding Service
The news embedding service takes in the maximal entity coocurrence set and does a Lowest Common Ancestor Graph traversal on each segment to get the knowledge graph subgraph-embedding. The final document embedding is then the union of all subgraph-embeddings of all segments in the maximal entity cooccurrence set as outlined in the NewsLink paper.

### Local Development
1. Ensure the `.env` file is set up and configured in the root directory (e.g. in the root directory, run `cp .env.example .env` and update the relevant variables).
2. Navigate to the `news_embedding` directory (e.g. run `cd news_embedding`)
3. Install the dev dependencies (e.g. run `pip3 install -r requirements.dev.txt`, preferably in a virtual environment).
4. Startup MongoDB (and setup the knowledge graph collections if yet to be done).
5. Run the following command to start the web scraper service in development mode.
    ```bash
    faust -A main worker -l info
    ```

### Knowledge Graph Setup
1. Generate a bidirected version of the WikiData knowledge graph and store the adjacency list in an external store like MongoDB for graph traversal.

## Tests
### Running tests
In the `news_embedding` directory, run:
```
python -m tests.priority_queue_tests;
python -m tests.g_star_search_tests
```

### Writing tests
1. We use [networkx](https://networkx.org/) for our mock knowledge graph representation in the test suite.
1. Adjacency list information for each mock graph is stored under `./tests/mocks/data/*.adjlist`.
1. To visualize the graph, the `MockKnowledgeGraph` class contains a `draw()` method which plots the graph
via `matplotlib.pyplot.show()`. Run this method within the testcase to visualize the graph for that
particular testcase. (Note that this `draw()` method is blocking).

### Extensions
1. Explore the usage of a smaller bidirected subgraph with entities within n-hops of Singapore to reduce the effects of noise and outliers in the maximal entity cooccurrence set. This may improve performance and speed of the news embedding component since this is currently applied to the Singapore context.
