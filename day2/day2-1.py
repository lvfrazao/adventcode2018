# Develop checksum function for warehouse IDs


def letter_freq(word):
    freq = {}
    for letter in word:
        freq[letter] = freq.get(letter, 0) + 1
    return freq


checksum2 = 0
checksum3 = 0
item_list = [s for s in open("input.txt").read().split("\n") if s]

for item in item_list:
    freq = letter_freq(item)
    if 2 in freq.values():
        checksum2 += 1
    if 3 in freq.values():
        checksum3 += 1

checksum = checksum2 * checksum3
print(checksum)
