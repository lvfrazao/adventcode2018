import re
import day5


in_poly = open("input.txt").read()
in_poly = in_poly
unique = set([s.lower() for s in in_poly])

benchmark = len(in_poly)
poly_len = []
for letter in unique:
    current = re.sub(letter, "", in_poly, flags=re.I)
    current = day5.Polymer(current).reduced
    poly_len.append(len(current))

print(benchmark)
print(poly_len)
print(min(poly_len))
