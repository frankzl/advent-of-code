with open('input/10', 'r') as reader:
    text = reader.read()

sorted_adapters = sorted([int(i) for i in (text.split("\n")[:-1])])

pre = 0 
diffs_seq = []
diffs = dict()

for i in sorted_adapters:
    diff = i - pre
    if diff not in diffs:
        diffs[diff] = 0
    diffs[diff] += 1
    pre = i
    diffs_seq.append(diff)

diffs[3] += 1
print(diffs)
print(diffs[1]*diffs[3])

max_joltage = sorted_adapters[-1]

def count(current_joltage, unused_adapter_list, required_joltage):
    if current_joltage == required_joltage:
        return 1

    total = 0
    for i, adapter in enumerate(unused_adapter_list):
        if adapter - current_joltage <= 3:
            total += count(adapter, unused_adapter_list[i+1:], required_joltage)
        else:
            break
    
    return total

within_adapters = []
current_joltage = 0
total = 1

for diff, adapter in zip(diffs_seq, sorted_adapters):
    if diff < 3:
        within_adapters.append(adapter)
    else:
        total *= count(current_joltage, within_adapters, adapter-3)
        current_joltage = adapter
        within_adapters = []

total *= count(current_joltage, within_adapters, adapter)

#print(len(diffs_seq))
print(total)

#print(count(0, sorted_adapters, max_joltage))

