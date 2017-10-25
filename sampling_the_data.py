import random
random.seed(1)
a = [4,14,47,60,7,24,51]
b = [[],[],[],[],[],[],[]]
c = [[],[],[],[],[]]
a0 = 0

## create original set
for i in range(len(a)):
    b[i] = list(range(a0,a0+a[i]))
    a0 += a[i]

## arrange 5*(a[i]/5) elements
for j in range(5):
    for i in range(len(a)):
        random.seed(1)
        x = random.sample(b[i],int(a[i]/5))
            
        for key in x:
            b[i].remove(key)
            c[j].append(key)

## arrange the rest elements       
b.sort(key=len, reverse=True)   
for key in b:
    random.seed(1)
    random.shuffle(key)
    for i in list(range(len(key))):
        c[i].append(key[i])
    c.sort(key=len)

for key in c:
    key.sort()
    print(key)
