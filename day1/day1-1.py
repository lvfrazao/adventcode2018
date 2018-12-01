# Sum all items in a list

input_list = [int(s) for s in open("input.txt").read().split("\n") if s]
print(sum(input_list))
