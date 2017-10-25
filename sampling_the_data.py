import random
a = [4,14,47,60,7,24,51]
b = [[],[],[],[],[],[],[]]
c = [[],[],[],[],[]]
a0 = 0

## create original set
for i in range(len(a)):
    b[i] = range(a0,a0+a[i])
    a0 += a[i]

## arrange 5*(a[i]/5) elements
for j in range(5):
    for i in range(len(a)):
        x = random.sample(b[i],a[i]/5)
            
        for key in x:
            b[i].remove(key)
            c[j].append(key)

## arrange the rest elements       
b.sort(lambda x,y: cmp(len(x), len(y)),reverse=True)   
for key in b:
    random.shuffle(key)
    for i in range(len(key)):
        c[i].append(key[i])
    c.sort(lambda x,y: cmp(len(x), len(y)))

for key in c:
    print len(key)
