#!/usr/bin/python

# Graph ideal and observed probabilities for a set of 4dF.

from matplotlib import pylab
from rolls import sample

all_results = range(-4, 5)
p_ideal  = [p/81.0 for p in [1, 4, 10, 16, 19, 16, 10, 4, 1]]
p_observed = []
for result in all_results:
 p_observed.append(len([s for s in sample if s == result])/float(len(sample)))

pylab.scatter(all_results, p_ideal, c='b')
pylab.scatter(all_results, p_observed, c='r')
pylab.xticks(all_results, ['%+d' % result for result in all_results])
pylab.xlabel('Result')
pylab.ylabel('Probability')
pylab.title('Ideal and observed probabilities for 4dF')
pylab.grid(True)
pylab.show()
