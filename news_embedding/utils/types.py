from utils.priority_queue import PriorityQueue

Label = str
Labels = list[Label]
Node = str
Distance = int
Distances = dict[Label, dict[Node, Distance]]
P_Queues = dict[Label, PriorityQueue]
Parents = dict[Label, dict[Node, list[Node]]]
Candidates = dict[Node, set[Node]]