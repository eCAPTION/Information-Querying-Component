## Installing dev dependencies
```bash
cd news_embedding
pip install -r requirements.dev.txt
```

## Knowledge Graph Setup

## Running locally
1. Setup the `.env` file at the root of the repository (by copying and modifying `.env.example`).
1. Run the following command to start the faust worker on localhost with debug info enabled:
```bash
faust -A main worker -l info
```

## Running tests
In the `news_embedding` directory, run:
```
python -m tests.priority_queue_tests;
python -m tests.g_star_search_tests
```

## Writing tests
1. We use [networkx](https://networkx.org/) for our mock knowledge graph representation in the test suite.
1. Adjacency list information for each mock graph is stored under `./tests/mocks/data/*.adjlist`.
1. To visualize the graph, the `MockKnowledgeGraph` class contains a `draw()` method which plots the graph
via `matplotlib.pyplot.show()`. Run this method within the testcase to visualize the graph for that
particular testcase. (Note that this `draw()` method is blocking).
