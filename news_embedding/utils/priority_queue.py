from heapq import heappush, heappop


class PriorityQueue:
    """
    Custom priority queue implementation with support for updating values within queue if the new priority is lower.
    Only supports unique values in the queue.

    Referenced from: https://docs.python.org/3/library/heapq.html#priority-queue-implementation-notes
    """

    REMOVED = "<removed-task>"

    def __init__(self) -> None:
        self.pq: list[list[int, str]] = []
        self.entry_finder = {}

    def push(self, priority: int, element):
        """
        Adds a new element OR update the priority of an existing task if the new priority is smaller.
        """
        if element in self.entry_finder:
            if priority >= self.entry_finder[element][0]:
                return
            else:
                self._remove_element(element)
        updated_entry = [priority, element]
        self.entry_finder[element] = updated_entry
        heappush(self.pq, updated_entry)

    def _remove_element(self, element):
        """
        Mark an existing element as REMOVED. Raise KeyError if not found.
        """
        entry = self.entry_finder.pop(element)
        entry[-1] = PriorityQueue.REMOVED

    def pop(self):
        """
        Remove and return the lowest priority element. Raise KeyError if empty.
        """
        while self.pq:
            priority, element = heappop(self.pq)
            if element is not PriorityQueue.REMOVED:
                del self.entry_finder[element]
                return priority, element
        raise KeyError("pop from an empty priority queue")

    def peek(self):
        """
        Peeks at the lowest priority element. Raise KeyError if empty.
        """
        for priority, element in self.pq:
            if element is PriorityQueue.REMOVED:
                continue
            return priority, element
        raise KeyError("peek called on an empty priority queue")

    def get_priority(self, element):
        """
        Returns the priority of the given element if it exists in the queue, else None.
        """
        if element in self.entry_finder:
            return self.entry_finder[element][0]

        return None
