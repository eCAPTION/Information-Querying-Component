import unittest

from g_star_search import GStarSearch
from tests.mocks.mock_knowledge_graph import MockKnowledgeGraph
from tests.mocks.data.files_enum import MockGraphData


class TestGStarSearch(unittest.TestCase):
    graph1 = MockKnowledgeGraph(MockGraphData.Graph1)
    gstar1 = GStarSearch(graph1)

    def test_singleNode(self):
        adjlist = self.gstar1.get_lcag(["bird"])
        expected = {"bird": set()}
        self.assertEqual(adjlist, expected)

    def test_adjacentNodes(self):
        adjlist = self.gstar1.get_lcag(["bird", "animal"])
        possible_results = [
            {"bird": set(["animal"]), "animal": set()},
            {"bird": set(), "animal": set(["bird"])},
        ]
        self.assertIn(adjlist, possible_results)

    def test_singlePathBetweenNodes(self):
        adjlist = self.gstar1.get_lcag(["ball", "cat"])
        possible_results = [
            {
                "animal": set(["cat", "dog"]),  # animal as root
                "dog": set(["ball"]),
                "cat": set(),
                "ball": set(),
            },
            {
                "dog": set(["ball", "animal"]),  # dog as root
                "animal": set(["cat"]),
                "cat": set(),
                "ball": set(),
            },
        ]
        self.assertIn(adjlist, possible_results)

    def test_widthOfEmbedding_shouldIncludeAllShortestPaths(self):
        adjlist = self.gstar1.get_lcag(["ball", "herbivore"])
        expected = {
            "animal": set(["dog", "elephant", "goat", "giraffe"]),
            "dog": set(["ball"]),
            "elephant": set(["herbivore"]),
            "goat": set(["herbivore"]),
            "giraffe": set(["herbivore"]),
            "herbivore": set(),
            "ball": set(),
        }
        self.assertEqual(adjlist, expected)

    def test_multipleWidths_shouldIncludeAllShortestPaths(self):
        adjlist = self.gstar1.get_lcag(["ball", "carnivore", "herbivore"])
        expected = {
            "animal": set(
                ["tiger", "lion", "cat", "bird", "dog", "goat", "giraffe", "elephant"]
            ),
            "tiger": set(["carnivore"]),
            "lion": set(["carnivore"]),
            "cat": set(["carnivore"]),
            "bird": set(["carnivore"]),
            "dog": set(["ball"]),
            "goat": set(["herbivore"]),
            "giraffe": set(["herbivore"]),
            "elephant": set(["herbivore"]),
            "carnivore": set(),
            "herbivore": set(),
            "ball": set(),
        }
        self.assertEqual(adjlist, expected)

    def test_rootNodeIsSameAsOneOfStartingLabelNodes_shouldReturnCorrectly(self):
        adjlist = self.gstar1.get_lcag(["ball", "animal", "herbivore"])
        expected = {
            "animal": set(["dog", "elephant", "giraffe", "goat"]),
            "dog": set(["ball"]),
            "elephant": set(["herbivore"]),
            "goat": set(["herbivore"]),
            "giraffe": set(["herbivore"]),
            "herbivore": set(),
            "ball": set(),
        }
        self.assertEqual(adjlist, expected)

    def test_multiplePossibleEmbeddings(self):
        adjlist = self.gstar1.get_lcag(["lion", "omnivore"])
        possible_results = [
            {
                "bird": set(["omnivore", "carnivore", "animal"]),  # bird as root node
                "carnivore": set(["lion"]),
                "animal": set(["lion"]),
                "omnivore": set(),
                "lion": set(),
            },
            {
                "dog": set(["omnivore", "animal"]),  # dog as root node
                "animal": set(["lion"]),
                "omnivore": set(),
                "lion": set(),
            },
            {
                "animal": set(["bird", "lion", "dog"]),  # animal as root
                "bird": set(["omnivore"]),
                "dog": set(["omnivore"]),
                "omnivore": set(),
                "lion": set(),
            },
            {
                "carnivore": set(["bird", "lion"]),  # carnivore as root
                "bird": set(["omnivore"]),
                "omnivore": set(),
                "lion": set(),
            },
        ]
        self.assertIn(adjlist, possible_results)

    def test_labelDoesNotExist(self):
        adjlist = self.gstar1.get_lcag(["non_existent"])
        self.assertEqual(adjlist, {})

    def test_oneExistingLabelAndOneNonExistingLabel(self):
        adjlist = self.gstar1.get_lcag(["ball", "non_existent"])
        expected = {"ball": set()}
        self.assertEqual(adjlist, expected)

        # self.graph1.draw()


if __name__ == "__main__":
    unittest.main()
