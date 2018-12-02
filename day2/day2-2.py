# What letters are common between the two correct box IDs?
# The boxes will have IDs which differ by exactly one character at the same position in both strings.

item_list = [s for s in open("input.txt").read().split("\n") if s]
remaing_items = list(item_list)

for item in item_list:
    remaing_items.pop(0)
    for item2 in remaing_items:
        errors = 0
        common_letters = []
        for i in range(len(item2)):
            if item[i] == item2[i]:
                common_letters.append(item[i])
            else:
                errors += 1
            if errors > 1:
                break
        if errors == 1:
            print(f"Found match: {item}  // {item2}")
            print(f"Common letters: {''.join(common_letters)}")
