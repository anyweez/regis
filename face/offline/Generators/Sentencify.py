import sys

def approved_content(line):
  if '"' in line:
    return False

  return True

book_file = sys.argv[1]

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

for s in sentences:
  print s
