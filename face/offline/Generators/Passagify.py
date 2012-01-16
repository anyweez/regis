import sys, random

# Generates a set of 5-sentence passages.

def approved_content(line):
  if '"' in line:
    return False

  return True

book_file = sys.argv[1]
num_passages = int(sys.argv[2])

fp = open(book_file)
book_lines = fp.readlines()
fp.close()

book_lines = map(str.strip, filter(approved_content, book_lines))
fulltxt = ' '.join(book_lines)

partial_s = fulltxt.split('.')
sentences = []
for sentence in partial_s:
  if len(sentence) < 120 and len(sentence) > 20:
    sentences.append('%s.' % sentence.strip())

passages = []
for i in xrange(num_passages):
  start = random.randint(0, len(sentences)-5)
  passages.append('  '.join(sentences[start:start+5]))

for passage in passages[:num_passages]:
  print passage

