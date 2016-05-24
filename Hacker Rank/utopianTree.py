

t = int(input().strip())
for a0 in range(t):
    n = int(input().strip())
    isSpring = True
    h = 1
    for l in range(n):
        if isSpring is False:
            h += 1
            isSpring = True
            continue
        if isSpring is True:
            h *= 2
            isSpring = False
            continue
    print(h)
