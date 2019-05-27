class AugmentedPQ:
    """A priority queue with several extra options."""
    
    def __init__(self, priority_fn=(lambda x: x)):
        self._priority_fn = priority_fn
        self._size = 0
        self._dict = {}
        self._heap = []

    def _left_child_index(self, index):
        return ((index + 1) * 2) - 1

    def _right_child_index(self, index):
        return (index + 1) * 2

    def _parent_index(self, index):
        return ((index + 1) / 2) - 1

    # Given an index, looks at its two children.
    # If one of those children has greater priority, swaps with that child.
    # The return value is the index of the original element's new position.
    def _update_at_index(self, index):
        left_idx = self._left_child_index(index)
        right_idx = self._right_child_index(index)

        parent_val = self._priority_fn(self._heap[index])
        left_val = parent_val
        right_val = parent_val
        if left_idx < self._size:
            left_val = self._priority_fn(self._heap[left_idx])
            if right_idx < self._size:
                right_val = self._priority_fn(self._heap[right_idx])
        else:
            return index

        min_child_val = left_val
        min_child_idx = left_idx
        if right_val < left_val:
            min_child_val = right_val
            min_child_idx = right_idx

        # If an actual swap is needed
        if min_child_val < parent_val:
            temp = self._heap[min_child_idx]
            self._heap[min_child_idx] = self._heap[index]
            self._heap[index] = temp
            self._dict[self._heap[index]].remove(min_child_idx)
            self._dict[self._heap[index]].add(index)
            self._dict[self._heap[min_child_idx]].remove(index)
            self._dict[self._heap[min_child_idx]].add(min_child_idx)
            return min_child_idx

        return index

    def push(self, x):
        self._heap.append(x)
        idx = self._size
        if x in self._dict:
            self._dict[x].add(idx)
        else:
            self._dict[x] = set([idx])
        self._size += 1

        parent_idx = self._parent_index(idx)
        while parent_idx >= 0:
            if self._update_at_index(parent_idx) == parent_idx:
                break
            parent_idx = self._parent_index(parent_idx)

    def pop(self):
        item = self._heap[0]
        self.delete(item)
        return item

    def delete(self, x):
        index_set = self._dict[x]
        index = index_set.pop()
        if len(index_set) == 0:
            del self._dict[x]
        self._size -= 1
        if self._size == 0:
            self._heap = []
            return
        
        self._heap[index] = self._heap.pop()
        self._dict[self._heap[index]].remove(self._size)
        self._dict[self._heap[index]].add(index)

        child_index = self._update_at_index(index)
        while child_index != index:
            index = child_index
            child_index = self._update_at_index(index)

    def contains(self, x):
        return x in self._dict

    def top_item(self):
        return self._heap[0]

    def top_heuristic_value(self):
        return self._priority_fn(self._heap[0])

    def empty(self):
        return self._size == 0
