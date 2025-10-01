import collections
index = collections.defaultdict(list)
index['a'].append(1)
index['a'].append(2)
index['b'].append(3)
index['c'].append(5)
print(index)
