import random, sys

# Generates a list of non-overlapping (x,y) coordinates.
# Number of coordinates requested should be passed in
# as a parameter.

count = int(sys.argv[1])

lows = {}
numfound = 0

while numfound < count:
  low = random.randint(1, 200)
  high = random.randint(low+1, 500)

  # If the coordinate already exists, generate a new one.
  if lows.has_key(low) and lows[low].has_key(high):
    continue

  # If the x value has already been registered, reg the y value.
  if not lows.has_key(low):
    lows[low] = {}
  lows[low][high] = True

  print '%d %d' % (low, high)
  numfound += 1
