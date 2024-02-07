## Installing dev dependencies
```
pip install -r requirements.dev.txt
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
1. To visualize the graph, the `MockKnowledgeGraph` class contains a `draw()` method which plots the graph via matplotlib.pyplot.show().
