input_list = [int(s) for s in open("input.txt").read().split("\n") if s]
freq = 0
known_freqs = {freq}

NotFound = True
while NotFound:
    for num in input_list:
        freq += num
        if freq in known_freqs:
            NotFound = False
            break
        else:
            known_freqs.add(freq)

print(freq)
