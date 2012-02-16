import sys

# Writes out a list of numbers as Roman numerals.  The bounds of the range
# are passed as arguments to the script.
def convert_num(num):
    groups = (1000, 500, 100, 50, 10, 5, 1, 1)
    letters = ('M', 'D', 'C', 'L', 'X', 'V', 'I')
    chars = []

    if num == 0: return None
    
    starting_pt = 0
    while num < (groups[starting_pt] - groups[starting_pt + 1]):
        starting_pt += 1
    
    while num > 0:
        # If it's greater than the boundary number, subtract the boundary number
        if num >= groups[starting_pt]:
            chars.append(letters[starting_pt])
            num -= groups[starting_pt]
        elif str(groups[starting_pt])[0] == '5' and num >= (groups[starting_pt] - groups[starting_pt + 1]):
            chars.append(letters[starting_pt+1])
            chars.append(letters[starting_pt])
            num -= (groups[starting_pt] - groups[starting_pt + 1])
        elif str(groups[starting_pt])[0] == '1' and num >= (groups[starting_pt] - groups[starting_pt + 2]):
            chars.append(letters[starting_pt+2])
            chars.append(letters[starting_pt])
            num -= (groups[starting_pt] - groups[starting_pt + 2])
        else:
            starting_pt += 1
    return ''.join(chars)
    
def roman(num):
    chars = []
    for i, digit in enumerate(str(num)[::-1]):
        chars.append(convert_num(int(digit) * (10 ** i)))

    return ''.join(filter(lambda x: x is not None, chars)[::-1])

low = int(sys.argv[1])
high = int(sys.argv[2])

for num in xrange(low, high+1):
    print roman(num)
