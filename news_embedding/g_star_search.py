from math import inf
from queue import Queue
from utils.priority_queue import PriorityQueue
from knowledge_graph.abstract_knowledge_graph import AbstractKnowledgeGraph
from utils.types import *


class GStarSearch:
    def __init__(self, kg: AbstractKnowledgeGraph) -> None:
        self.kg = kg

    def get_lcag(self, L: Labels) -> set[Node]:
        """
        Apply G* Search Algorithm to get the Lowest Common Ancestor Graph outlined by the NewsLink paper.

        Input:
        - L: The set of entity labels L = { l_1, l_2, ..., l_m } identified from a news segment

        Returns: Lowest common ancestor graph G* for given labels in KG
        """

        # Getting labels that actually have a corresponding representation in the KG
        label_to_node_names = {
            label: self.kg.get_nodes_with_name_containing(label) for label in L
        }
        L = list(filter(lambda label: len(label_to_node_names[label]), L))

        # Handle edge cases
        if len(L) == 0:
            return set()
        elif len(L) == 1:
            return set([label_to_node_names[L[0]][0]])

        # Initialize distances and priority queues
        distances: Distances = {label: {} for label in L}
        p_queues: P_Queues = {
            label: PriorityQueue() for label in L
        }  # each queue contains elements [D(label, v_f), v_f.entity_id]
        parents: Parents = {label: {} for label in L}

        # Setup each priority queue with set of nodes matching `label` with distance 0
        for label in L:
            for matching_node in label_to_node_names[label]:
                p_queues[label].push(0, matching_node)

        results = {"candidates": {}, "min_depth": inf}

        # LCA graph traversal
        while True:
            node = self.__path_enumeration(p_queues, distances, parents)
            self.__candidate_collection(node, L, distances, parents, results)

            min_distance_across_p_queues = self.__get_min_distance_node_across_p_queues(
                p_queues
            )

            if (
                len(results["candidates"].items())
                and results["min_depth"] < min_distance_across_p_queues
            ):
                break

        return GStarSearch.__get_most_compact_embedding(
            results["candidates"], L, distances
        )

    def __path_enumeration(
        self, p_queues: P_Queues, distances: Distances, parents: Parents
    ):
        """
        Path enumeration procedure described in NewsLink. Explores the next smallest-distance node across all priority queues.

        Returns the node explored.
        """
        label, node, dist = self.__pop_min_distance_node_and_label_across_p_queues(
            p_queues
        )

        for neighbor in self.kg.get_neighbors(node):
            # If node has not been visited before for this label, push it to the queue or update its priority if it already exists.
            # Once a node has been visited already for this label, that distance would have been smaller due to BFS-invariant on unweighted graphs - so we do nothing.
            if distances[label].get(neighbor) == None:
                current_priority_in_queue = p_queues[label].get_priority(neighbor)
                updated_priority = dist + 1

                if current_priority_in_queue == None:
                    # Node is reached from S(l_i) for the first time
                    p_queues[label].push(updated_priority, neighbor)
                    parents[label][neighbor] = [node]
                elif updated_priority <= current_priority_in_queue:
                    # Node is reached by an alternative shortest path
                    # We add this parent too to increase the width of the embedding
                    parents[label][neighbor].append(node)
                else:
                    # Node is reached by a longer path from S(l_i) -> ignore
                    continue

        # No need to take min here, since the first time a node is visited from label i, it must be the minimal distance
        # due to the BFS invariant on unit edges.
        # Also, once a node is visited, it can't be visited again since we don't add visited nodes to the queue, and each queue
        # cannot have duplicate nodes.
        distances[label][node] = dist

        return node

    @classmethod
    def __candidate_collection(
        cls,
        candidate_root_node: Node,
        L: Labels,
        distances: Distances,
        parents: Parents,
        results: dict[str, any],
    ):
        depth = -1
        for label in L:
            if candidate_root_node not in distances[label]:
                # Some label has not reached this node yet -> no candidate graph yet
                return

            depth = max(depth, distances[label][candidate_root_node])

        # Generate embedding from candidate_root_node by backtracking on each label
        G = set()
        for label in L:
            cls.__backtrack_for_label(candidate_root_node, parents[label], G)

        results["candidates"][candidate_root_node] = G
        results["min_depth"] = depth

    @classmethod
    def __backtrack_for_label(
        cls,
        root_node: Node,
        parents_dict: dict[Node, list[Node]],
        result_set: set[Node],
    ):
        q = Queue()
        q.put(root_node)

        while not q.empty():
            curr_node = q.get()
            result_set.add(curr_node)
            node_parents = parents_dict.get(curr_node)

            # Original node containing label is reached
            if not node_parents:
                continue

            for node in node_parents:
                q.put(node)

    @classmethod
    def __get_compactness_order(cls, root_node: Node, L: Labels, distances: Distances):
        """
        Returns distance from root_node to each label in descending order.
        """
        compactness_order = [distances[label][root_node] for label in L]
        compactness_order.sort(reverse=True)
        return compactness_order

    @classmethod
    def __get_compactness_orders(
        cls, candidates: Candidates, L: Labels, distances: Distances
    ):
        compactness_orders: dict[Node, list[Distance]] = {}

        for root_node, G in candidates.items():
            compactness_order = cls.__get_compactness_order(root_node, L, distances)
            compactness_orders[root_node] = compactness_order

        return compactness_orders

    @classmethod
    def __get_most_compact_embedding(
        cls, candidates: Candidates, L: Labels, distances: Distances
    ):
        compactness_orders = cls.__get_compactness_orders(candidates, L, distances)
        filtered_compactness_orders = compactness_orders

        for i in range(len(L)):
            if len(filtered_compactness_orders.items()) == 1:
                return candidates[list(filtered_compactness_orders.keys())[0]]

            min_ith_index = min(
                [
                    compactness_order[i]
                    for compactness_order in filtered_compactness_orders.values()
                ]
            )

            filtered_compactness_orders = {
                k: v
                for k, v in filtered_compactness_orders.items()
                if v[i] == min_ith_index
            }

        # If all compactness orderings are equally good, take the first one
        return list(candidates.values())[0]

    @classmethod
    def __get_min_priority_in_queue(cls, p_queue: PriorityQueue):
        try:
            return p_queue.peek()[0]
        except KeyError:
            return inf

    @classmethod
    def __get_min_distance_queue_and_label_across_p_queues(cls, p_queues: P_Queues):
        """
        Gets the entry with argmin distance across all the 'top' elements in the input priority queues
        """
        return min(
            [key_value for key_value in p_queues.items()],
            key=lambda key_value: cls.__get_min_priority_in_queue(key_value[1]),
        )

    @classmethod
    def __get_min_distance_node_across_p_queues(cls, p_queues: P_Queues):
        _, p_queue_with_min_entry = (
            cls.__get_min_distance_queue_and_label_across_p_queues(p_queues)
        )
        dist, _ = p_queue_with_min_entry.peek()

        return dist

    @classmethod
    def __pop_min_distance_node_and_label_across_p_queues(cls, p_queues: P_Queues):
        label, p_queue_with_min_entry = (
            cls.__get_min_distance_queue_and_label_across_p_queues(p_queues)
        )
        dist, node = p_queue_with_min_entry.pop()

        return label, node, dist
