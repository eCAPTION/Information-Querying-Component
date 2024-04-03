import unittest

from g_star_search import GStarSearch
from tests.mocks.mock_knowledge_graph import MockKnowledgeGraph
from tests.mocks.data.files_enum import MockGraphData


class TestGStarSearch(unittest.TestCase):
    graph1 = MockKnowledgeGraph(MockGraphData.Graph1)
    gstar1 = GStarSearch(graph1)
    dummy_p_id = 1000

    def test_singleNode(self):
        adjlist = self.gstar1.get_lcag(["bird"])
        expected = {"bird": set()}
        self.assertEqual(adjlist, expected)

    def test_adjacentNodes(self):
        adjlist = self.gstar1.get_lcag(["bird", "animal"])
        possible_results = [
            {"bird": set([("animal", self.dummy_p_id)]), "animal": set()},
            {"bird": set(), "animal": set([("bird", self.dummy_p_id)])},
        ]
        self.assertIn(adjlist, possible_results)

    def test_singlePathBetweenNodes(self):
        adjlist = self.gstar1.get_lcag(["ball", "cat"])
        possible_results = [
            {
                # animal as root
                "ball": set([("dog", self.dummy_p_id)]),
                "dog": set([("animal", self.dummy_p_id)]),
                "cat": set([("animal", self.dummy_p_id)]),
                "animal": set(),
            },
            {
                # dog as root
                "ball": set([("dog", self.dummy_p_id)]),
                "animal": set([("dog", self.dummy_p_id)]),
                "cat": set([("animal", self.dummy_p_id)]),
                "dog": set(),
            },
        ]
        self.assertIn(adjlist, possible_results)

    def test_widthOfEmbedding_shouldIncludeAllShortestPaths(self):
        adjlist = self.gstar1.get_lcag(["ball", "herbivore"])
        expected = {
            # animal as root
            "ball": set([("dog", self.dummy_p_id)]),
            "dog": set([("animal", self.dummy_p_id)]),
            "herbivore": set([("elephant", self.dummy_p_id), ("giraffe", self.dummy_p_id), ("goat", self.dummy_p_id)]),
            "elephant": set([("animal", self.dummy_p_id)]),
            "giraffe": set([("animal", self.dummy_p_id)]),
            "goat": set([("animal", self.dummy_p_id)]),
            "animal": set(),
        }
        self.assertEqual(adjlist, expected)

    def test_multipleWidths_shouldIncludeAllShortestPaths(self):
        adjlist = self.gstar1.get_lcag(["ball", "carnivore", "herbivore"])
        expected = {
            # animal as root
            "ball": set([("dog", self.dummy_p_id)]),
            "herbivore": set([("elephant", self.dummy_p_id), ("giraffe", self.dummy_p_id), ("goat", self.dummy_p_id)]),
            "carnivore": set([("cat", self.dummy_p_id), ("tiger", self.dummy_p_id), ("lion", self.dummy_p_id), ("bird", self.dummy_p_id)]),
            "cat": set([("animal", self.dummy_p_id)]),
            "tiger": set([("animal", self.dummy_p_id)]),
            "lion": set([("animal", self.dummy_p_id)]),
            "elephant": set([("animal", self.dummy_p_id)]),
            "giraffe": set([("animal", self.dummy_p_id)]),
            "goat": set([("animal", self.dummy_p_id)]),
            "dog": set([("animal", self.dummy_p_id)]),
            "bird": set([("animal", self.dummy_p_id)]),
            "animal": set(),
        }
        self.assertEqual(adjlist, expected)

    def test_rootNodeIsSameAsOneOfStartingLabelNodes_shouldReturnCorrectly(self):
        adjlist = self.gstar1.get_lcag(["ball", "animal", "herbivore"])
        expected = {
            # animal is root
            "herbivore": set([("elephant", self.dummy_p_id), ("giraffe", self.dummy_p_id), ("goat", self.dummy_p_id)]),
            "elephant": set([("animal", self.dummy_p_id)]),
            "giraffe": set([("animal", self.dummy_p_id)]),
            "goat": set([("animal", self.dummy_p_id)]),
            "ball": set([("dog", self.dummy_p_id)]),
            "dog": set([("animal", self.dummy_p_id)]),
            "animal": set(),
        }
        self.assertEqual(adjlist, expected)

    def test_multiplePossibleEmbeddings(self):
        adjlist = self.gstar1.get_lcag(["lion", "omnivore"])
        possible_results = [
            {
                # bird as root
                "lion": set([("carnivore", self.dummy_p_id), ("animal", self.dummy_p_id)]),
                "carnivore": set([("bird", self.dummy_p_id)]),
                "omnivore": set([("bird", self.dummy_p_id)]),
                "animal": set([("bird", self.dummy_p_id)]),
                "bird": set(),
            },
            {
                # dog as root
                "lion": set([("animal", self.dummy_p_id)]),
                "animal": set([("dog", self.dummy_p_id)]),
                "omnivore": set([("dog", self.dummy_p_id)]),
                "dog": set(),
            },
            {
                # animal as root
                "lion": set([("animal", self.dummy_p_id)]),
                "omnivore": set([("dog", self.dummy_p_id), ("bird", self.dummy_p_id)]),
                "bird": set([("animal", self.dummy_p_id)]),
                "dog": set([("animal", self.dummy_p_id)]),
                "animal": set(),
            },
            {
                # carnivore as root
                "lion": set([("carnivore", self.dummy_p_id)]),
                "omnivore": set([("bird", self.dummy_p_id)]),
                "bird": set([("carnivore", self.dummy_p_id)]),
                "carnivore": set(),
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
