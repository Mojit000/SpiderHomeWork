items = []
with open('jsHomePage.txt', 'r') as f:
    for line in f:
        items.append(line)

print(len(items))
for i in items:
    print(i)