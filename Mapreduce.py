#!/usr/bin/env python

#  Q16  Which node generated the largest number of APPUNAV events?

from mrjob.job import MRJob
from mrjob.step import MRStep

class MRAPPUNAVEvents(MRJob):

    def steps(self):
        return [
            MRStep(mapper=self.mapper,
                   combiner=self.combiner,
                   reducer=self.reducer_sum),
            MRStep(reducer=self.reducer_find_max)
        ]

    def mapper(self, _, line):
        columns = line.split()
        if len(columns) > 0 and columns[0] == 'APPUNAV':
            node = columns[3]  # Assuming node is the 4th column
            yield node, 1

    def combiner(self, node, counts):
        yield node, sum(counts)

    def reducer_sum(self, node, counts):
        yield None, (sum(counts), node)

    def reducer_find_max(self, _, node_counts):
        yield max(node_counts)

if __name__ == '__main__':
    MRAPPUNAVEvents.run()
