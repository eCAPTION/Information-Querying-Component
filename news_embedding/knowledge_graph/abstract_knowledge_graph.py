from abc import ABC, abstractmethod
from utils.types import *


class AbstractKnowledgeGraph(ABC):
    """
    NOTE: Assumes KG has been pre-processed to be bi-directed
    """

    @abstractmethod
    def get_nodeids_with_name_containing(self, label_name: str) -> list[NodeID]:
        """
        Get the node IDs of nodes with names containing `label_name` via exact string matching.

        Returns: The node IDs of nodes matched
        """
        ...

    @abstractmethod
    def get_neighbors(self, entity_id: NodeID) -> list[tuple[NodeID, PropertyID]]:
        """
        Get the entity IDs of the neighbors of node with `entity_id`.

        Input:
        - entity_id: The entity ID of the node whose neighbors are returned

        Returns: The entity IDs of the neighboring node
        """
        ...
