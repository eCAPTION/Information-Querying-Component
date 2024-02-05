import unittest
from utils.priority_queue import PriorityQueue


class TestPriorityQueue(unittest.TestCase):
    Priority = int
    Element = str

    @classmethod
    def pushElementsToQueue(
        cls,
        elements_with_priority: list[list[Priority, Element]],
        queue: PriorityQueue,
    ):
        for priority, element in elements_with_priority:
            queue.push(priority, element)

    @classmethod
    def getQueueWith(cls, elements_with_priority: list[list[Priority, Element]]):
        pq = PriorityQueue()
        TestPriorityQueue.pushElementsToQueue(elements_with_priority, pq)
        return pq

    def testPush_emptyQueue_addsEntry(self):
        element1 = "element1"
        element2 = "element2"
        elements = [
            [1, element1],
            [2, element2],
        ]
        pq = TestPriorityQueue.getQueueWith(elements)

        self.assertEqual(pq.entry_finder[element1], elements[0])
        self.assertEqual(pq.entry_finder[element2], elements[1])

    def testPush_duplicateEntryWithSmallerPriority_overridesSuccessfully(self):
        element = "element"
        higher_priority = 2
        lower_priority = 1
        elements = [
            [higher_priority, element],
            [lower_priority, element],
        ]
        pq = TestPriorityQueue.getQueueWith(elements)

        self.assertEqual(pq.entry_finder[element], elements[-1])

    def testPush_duplicateElementWithBiggerPriorityEntry_doesNotOverride(self):
        element = "element"
        lower_priority = 1
        higher_priority = 2
        elements = [
            [lower_priority, element],
            [higher_priority, element],
        ]
        pq = TestPriorityQueue.getQueueWith(elements)

        self.assertEqual(pq.entry_finder[element], elements[0])

    def testPop_emptyQueue_raisesKeyError(self):
        pq = PriorityQueue()
        self.assertRaises(KeyError, pq.pop)

    def testPop_popsElementsInOrderOfAscendingPriority(self):
        element1 = "element1"
        element2 = "element2"
        element3 = "element3"
        elements = [
            [3, element3],
            [2, element2],
            [1, element1],
        ]
        pq = TestPriorityQueue.getQueueWith(elements)

        expected = [
            (1, element1),
            (2, element2),
            (3, element3),
        ]

        for exp in expected:
            self.assertEqual(pq.pop(), exp)

        self.assertRaises(KeyError, pq.pop)

    def testPop_duplicatedElementWithSmallerPriority_overridedSuccessfully(self):
        element = "element"
        lower_priority = 1
        higher_priority = 2
        elements = [
            [higher_priority, element],
            [lower_priority, element],
        ]
        pq = TestPriorityQueue.getQueueWith(elements)
        expected = (lower_priority, element)

        self.assertEqual(pq.pop(), expected)
        self.assertRaises(KeyError, pq.pop)

    def testPeek_emptyQueue_raisesKeyError(self):
        pq = PriorityQueue()
        self.assertRaises(KeyError, pq.peek)

    def testPeek_nonEmptyQueue_returnsCorrectly(self):
        element1 = "element1"
        element2 = "element2"
        elements = [
            [2, element2],
            [1, element1],
        ]
        pq = TestPriorityQueue.getQueueWith(elements)
        expected = (1, element1)

        self.assertEqual(pq.peek(), expected)

    def testPeek_nonEmptyQueueAfterDuplicateElementsInserted_returnsCorrectly(self):
        element1 = "element1"
        element2 = "element2"
        elements = [
            [3, element1],
            [2, element2],
            [1, element1],
        ]
        pq = TestPriorityQueue.getQueueWith(elements)
        expected = (1, element1)

        self.assertEqual(pq.peek(), expected)

    def testGetPriority_emptyQueue_returnsNegativeOne(self):
        non_existent_element = "element"
        pq = PriorityQueue()
        self.assertIsNone(pq.get_priority(non_existent_element))

    def testGetPriority_nonEmptyQueue_returnsCorrectly(self):
        element1 = "element1"
        element2 = "element2"
        elements = [
            [1, element1],
            [2, element2],
        ]
        pq = TestPriorityQueue.getQueueWith(elements)

        self.assertEqual(pq.get_priority(element1), 1)
        self.assertEqual(pq.get_priority(element2), 2)

    def testGetPriority_duplicatedElement_priorityOverrided(self):
        element = "element"
        lower_priority = 1
        higher_priority = 2
        elements = [
            [higher_priority, element],
            [lower_priority, element],
        ]
        pq = TestPriorityQueue.getQueueWith(elements)

        self.assertEqual(pq.get_priority(element), lower_priority)


if __name__ == "__main__":
    unittest.main()
