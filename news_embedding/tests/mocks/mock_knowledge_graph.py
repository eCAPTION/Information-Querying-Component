import networkx as nx
import matplotlib.pyplot as plt
from knowledge_graph.abstract_knowledge_graph import AbstractKnowledgeGraph
from tests.mocks.data.files_enum import MockGraphData


class MockKnowledgeGraph(AbstractKnowledgeGraph):
    def __init__(self, data: MockGraphData) -> None:
        super().__init__()

        # Create networkx undirected graph
        self.G: nx.Graph = nx.read_adjlist(
            data.value, create_using=nx.Graph, nodetype=str
        )

    def get_nodes_with_name_containing(self, label_name: str) -> list[str]:
        nodes = self.G.nodes
        filtered_nodes = filter(lambda node: label_name in node, nodes)

        return list(filtered_nodes)

    def get_neighbors(self, entity_id: str) -> list[str]:
        return self.G.neighbors(entity_id)

    def draw(self):
        """
        Plots the underlying networkx graph for visualization and debugging purposes.
        """
        nx.draw(self.G, with_labels=True)
        plt.show()
