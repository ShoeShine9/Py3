n = int(input())

for i in range(n):
    wordArr = input().split()

    for word in wordArr:
        i = 0
        for let in word:
            if i % 2 == 0:
                print (let, end="")
            i += 1

    print (" ", end="")

    for word in wordArr:
        j = 0
        for let in word:
            if j % 2 > 0:
                print (let, end="")
            j += 1

    print ()   
             

