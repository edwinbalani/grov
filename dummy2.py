def priority_enqueue(q, key, value):
	l = len(q) - 1
	if l >= 0:
		while (q[l][1] > value and l >= 0):
			l -= 1
		q.insert(l + 1, (key, value))
	else:
		q.append((key, value))

q = list()
priority_enqueue(q, 2, 3)
print(q)
priority_enqueue(q, 2, 5)
print(q)
priority_enqueue(q, 2, 4)
print(q)
priority_enqueue(q, 2, 3)
print(q)
priority_enqueue(q, 2, 10)
print(q)
priority_enqueue(q, 2, 0)
print(q)
priority_enqueue(q, 3, 0)
print(q)