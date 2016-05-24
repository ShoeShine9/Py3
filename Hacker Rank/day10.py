num = int(input().strip())

parNum = str(bin(num)).strip("0b").split("0")

count = 0
for i in parNum:
    if len(i) >= count:
        count = len(i)  

print (count)

