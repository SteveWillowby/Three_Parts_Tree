from augmented_pq import *

class AggregatorBase:
    """Used to maintain a single aggregate value as elements are added or removed"""

    def __init__(self):
        self._agg = 0

    def add(self, value):
        self._agg += 1

    def delete(self, value):
        self._agg -= 1

    def value(self):
        return self._agg

class MinAggregator(AggregatorBase):
    """Gives you the minimum value."""

    def __init__(self):
        self._pq = AugmentedPQ()

    def add(self, value):
        self._pq.push(value)

    def delete(self, value):
        self._pq.delete(value)

    def value(self):
        return self._pq.top_item()

class MaxAggregator(AggregatorBase):
    """Gives you the maximum value."""

    def __init__(self):
        self._pq = AugmentedPQ(priority_fn=(lambda x: -x))

    def add(self, value):
        self._pq.push(value)

    def delete(self, value):
        self._pq.delete(value)

    def value(self):
        return self._pq.top_item()

class FancySchmancyAggregatorOne(AggregatorBase):
    """Uses a ratio of rule frequency and heuristic values"""

    def __init__(self):
        pass

    def add(self, value):
        pass

    def delete(self, value):
        pass

    def value(self):
        pass
