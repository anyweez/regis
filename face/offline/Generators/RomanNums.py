import sys

# Writes out a list of numbers as Roman numerals.  The bounds of the range
# are passed as arguments to the script.

def roman(num):
  groups = (1000, 500, 100, 50, 10, 5, 1, 1, 0)
  letters = ('M', 'D', 'C', 'L', 'X', 'V', 'I', 'I')
  chars = []

  while num > 0:
    # Check everything but the last element.
    for i in xrange(len(groups)-2):
      if num >= groups[i] - groups[i+2]:
        # we can use this.
        if num >= groups[i]:
          chars.append(letters[i])
          num -= groups[i]
          break
        else:
          chars.append(letters[i+2])
          chars.append(letters[i])
          num -= (groups[i] - groups[i+2])

  return ''.join(chars)

low = int(sys.argv[1])
high = int(sys.argv[2])

for num in xrange(low, high+1):
  print roman(num)
