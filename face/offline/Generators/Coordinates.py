import random, sys

# Generates a list of non-overlapping (x,y) coordinates.
# Number of coordinates requested should be passed in
# as a parameter.

count = int(sys.argv[1])

xvals = {}
numfound = 0

while numfound < count:
  xval = random.randint(1, 1000)
  yval = random.randint(1, 1000)

  # If the coordinate already exists, generate a new one.
  if xvals.has_key(xval) and xvals[xval].has_key(yval):
    continue

  # If the x value has already been registered, reg the y value.
  if not xvals.has_key(xval):
    xvals[xval] = {}
  xvals[xval][yval] = True

  print '%d %d' % (xval, yval)
  numfound += 1
