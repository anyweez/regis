import sys

# Accepts the name of a complete wordlist (from a dictionary) and pulls out
# some of the less common ones.

def keep(word):
  # No funky symbols.
  if "'" in word:
    return False

  # If the word contains non-ascii characters let's lose it.
  try:
    word.decode('ascii')
  except UnicodeDecodeError:
    return False

  # Starts with a capital letter.  No proper nouns.
  if ord(word[0]) > 64 and ord(word[0]) < 91:
    return False

  # Cut out stubby words.
  if len(word) < 3:
    return False

  return True

dictfile = sys.argv[1]

fp = open(dictfile)
words = fp.readlines()
fp.close()

words = filter(keep, words)

for word in words:
  print word.strip()
