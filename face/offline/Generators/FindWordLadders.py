import sys, random

# Generates a set of words that form a word ladder.  The name of a file that contains
# candidate words should be provided as a parameter.

# The name of the file to pull words from.
wordlist = sys.argv[1]
# The number of ladders to have
num_ladders = int(sys.argv[2])
# The length of each ladder
max_depth = int(sys.argv[3])

def single_letter(words):
  first, second = words

  diff = 0
  for i in xrange(len(first)):
    if first[i] != second[i]:
      diff += 1

  return (diff == 1)

def compress_ladder(words):
  status = [True for word in words]
  # Cycle through each word
  for i in xrange(len(words)):
    # We want to compare it against other words, starting from the back.
    for j in reversed(xrange(i+1, len(words))):
      # If we find words that can be reduced, reduce them.
      if status[i] is True and status[j] is True:
        if (j - i) > 1 and single_letter( (words[i], words[j]) ):
          # For every item in the range between the two reduceables, mark
          # them as deletable.
          for k in xrange(i+1, j):
            status[k] = False

  return [w for i, w in enumerate(words) if status[i]]

def ladder(words, partial, start):
  global max_depth
  partial.append(start)

  # found a path!
  if len(partial) == max_depth:
    return partial
  # Bail if we run out of words to try
  elif len(words) is 0:
    return []
  # otherwise let's keep exploring
  else:
    eligible_t = filter(single_letter, [(start, word) for word in words])
    eligible = [w[1] for w in eligible_t]

    random.shuffle(eligible)

    for cw in eligible:
      result = ladder([w for w in words if w != cw], partial, cw)

      # if we find something that works, report it
      if len(result) > 0:
        return result 
    return []

fp = open(wordlist)
words = fp.readlines()
fp.close()

# Get rid of the endlines
words = map(str.strip, words)
ladders_found = 0

while ladders_found != num_ladders:
#  begin = random.choice(words)
#  usable = [word for word in words if len(word) == len(begin)]

  l = []

  last_length = 0
  usable = None
  begin = None
  while len(l) < max_depth:
    # Select a starting word and refine the usable word list.
    if len(l) == last_length or len(l) == 0:
      begin = random.choice(words)
      usable = [word for word in words if len(word) == len(begin)]
      l = [begin,]

    last_length = len(l)

    last_word = l.pop()
    l = ladder([word for word in usable if word not in l], l, last_word)
#    print 'ladder found: %s' % str(l)
    l = compress_ladder(l)
#    print 'compressed: %s' % str(l)

  # Cut off any excess that may exist.
  l = l[:max_depth]

  # If we find a ladder that we can use, print it out.
  if len(l) > 0:
    ladders_found += 1
    for word in l:
      print word

    if ladders_found != num_ladders:
      print ''
