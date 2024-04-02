from utils.priority_queue import PriorityQueue

Label = str
Labels = list[Label]
NodeID = int
PropertyID = int
Distance = int
Distances = dict[Label, dict[NodeID, Distance]]
P_Queues = dict[Label, PriorityQueue]
Parents = dict[Label, dict[NodeID, list[tuple[NodeID, PropertyID]]]]
Embedding_Adjlist = dict[NodeID, set[tuple[NodeID, PropertyID]]]
Candidates = dict[NodeID, Embedding_Adjlist]
