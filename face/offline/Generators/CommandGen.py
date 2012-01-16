import random, sys, math


count = int(sys.argv[1])

terms = ('reverse', 'frontback', 'duplicate')

num_each = int(math.floor(count / len(terms)))

for i in xrange(len(terms)):
  for j in xrange(num_each):
    print terms[i]

