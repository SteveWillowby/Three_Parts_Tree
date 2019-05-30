from augmented_pq import *

class RulePQ(AugmentedPQ):
    
    def __init__(self, priority_fn=None):
        self.counts_of_nodes_by_prio = {}
        self.unique_prio_queue = AugmentedPQ()
        AugmentedPQ.__init__(self, priority_fn)

    def push(self, x, prio=None):
        prio = AugmentedPQ.push(self, x, prio)
        if prio not in self.counts_of_nodes_by_prio:
            self.counts_of_nodes_by_prio[prio] = {}
        for node in x:
            if node in self.counts_of_nodes_by_prio[prio]:
                self.counts_of_nodes_by_prio[prio][node] += 1
            else:
                self.counts_of_nodes_by_prio[prio][node] = 1

        if not self.unique_prio_queue.contains(prio):
            self.unique_prio_queue.push(prio)

    def delete(self, x):
        prio = AugmentedPQ.delete(self, x)
        for node in x:
            self.counts_of_nodes_by_prio[prio][node] -= 1
            if self.counts_of_nodes_by_prio[prio][node] == 0:
                del self.counts_of_nodes_by_prio[prio][node]
        if len(self.counts_of_nodes_by_prio[prio]) == 0:
            del self.counts_of_nodes_by_prio[prio]
            self.unique_prio_queue.delete(prio)

    def number_of_nodes_covered_at_priority(self, prio):
        if prio not in self.counts_of_nodes_by_prio:
            return 0
        return len(self.counts_of_nodes_by_prio[prio])

    def sorted_list_of_prios(self):
        size = self.unique_prio_queue.size()
        the_list = [self.unique_prio_queue.pop() for i in range(0, size)]
        for i in range(0, size):
            self.unique_prio_queue.push(the_list[i])
        return the_list
