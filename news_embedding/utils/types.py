from utils.priority_queue import PriorityQueue

Label = str
Labels = list[Label]
NodeID = int
Distance = int
Distances = dict[Label, dict[NodeID, Distance]]
P_Queues = dict[Label, PriorityQueue]
Parents = dict[Label, dict[NodeID, list[NodeID]]]
Embedding_Adjlist = dict[NodeID, set[NodeID]]
Candidates = dict[NodeID, Embedding_Adjlist]
