import random, sys

# Generates a list of year numbers.

count = int(sys.argv[1])

for i in xrange(count):
  print random.randint(1900, 2009)
