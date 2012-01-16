import random, sys

dim = int(sys.argv[1])
count = int(sys.argv[2])

for gridnum in xrange(count):
  # Generate the full matrix
  row = ['x' for i in xrange(dim)]
  matrix = [list(row) for i in xrange(dim)]

  # Remove a couple of chunks
  chunks = random.randint(2, 8)
  for chunk in xrange(chunks):
    xlen = random.randint(1, 15)
    ylen = random.randint(1, 15)

    xloc = random.randint(0, dim-2)
    yloc = random.randint(0, dim-2)

    for x in xrange(xlen):
      for y in xrange(ylen):
        if xloc+x < len(matrix) and yloc+y < len(matrix[xloc+x]):
          matrix[xloc+x][yloc+y] = 'o'

  for row in matrix:
    print ''.join(row)

  if gridnum is not count-1:
    print ''
