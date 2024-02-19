import unittest

from g_star_search import GStarSearch
from tests.mocks.mock_knowledge_graph import MockKnowledgeGraph
from tests.mocks.data.files_enum import MockGraphData


class TestGStarSearch(unittest.TestCase):
    graph1 = MockKnowledgeGraph(MockGraphData.Graph1)
    gstar1 = GStarSearch(graph1)

    def test_singleNode(self):
        self.assertEqual(self.gstar1.get_lcag(["bird"]), set(["bird"]))

    def test_adjacentNodes(self):
        self.assertEqual(
            self.gstar1.get_lcag(["bird", "animal"]), set(["bird", "animal"])
        )

    def test_singlePathBetweenNodes(self):
        self.assertEqual(
            self.gstar1.get_lcag(["ball", "cat"]), set(["ball", "dog", "animal", "cat"])
        )

    def test_widthOfEmbedding_shouldIncludeAllShortestPaths(self):
        self.assertEqual(
            self.gstar1.get_lcag(["ball", "herbivore"]),
            set(
                [
                    "ball",
                    "dog",
                    "animal",
                    "goat",
                    "elephant",
                    "giraffe",
                    "herbivore",
                ]
            ),
        )

    def test_multipleWidths_shouldIncludeAllShortestPaths(self):
        self.assertEqual(
            self.gstar1.get_lcag(["ball", "carnivore", "herbivore"]),
            set(
                [
                    "lion",
                    "goat",
                    "herbivore",
                    "dog",
                    "elephant",
                    "giraffe",
                    "ball",
                    "carnivore",
                    "tiger",
                    "cat",
                    "bird",
                    "animal",
                ]
            ),
        )

    def test_rootNodeIsSameAsOneOfStartingLabelNodes_shouldReturnCorrectly(self):
        self.assertEqual(
            self.gstar1.get_lcag(["ball", "animal", "herbivore"]),
            set(["dog", "animal", "ball", "giraffe", "elephant", "goat", "herbivore"]),
        )

    def test_multiplePossibleEmbeddings(self):
        self.assertIn(
            self.gstar1.get_lcag(["lion", "omnivore"]),
            [
                set(["carnivore", "bird", "lion", "omnivore", "animal"]),
                set(["lion", "dog", "animal", "omnivore"]),
                set(["dog", "bird", "lion", "omnivore", "animal"]),
                set(["lion", "bird", "carnivore", "omnivore"]),
            ],
        )

    def test_labelDoesNotExist(self):
        self.assertEqual(self.gstar1.get_lcag(["non_existent"]), set())

    def test_oneExistingLabelAndOneNonExistingLabel(self):
        result = self.gstar1.get_lcag(["ball", "non_existent"])
        expected = set(["ball"])
        self.assertEqual(result, expected)
        # self.graph1.draw()


if __name__ == "__main__":
    unittest.main()
