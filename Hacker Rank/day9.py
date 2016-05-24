n = int(input())

def factorial (num):
    if num==0:
        return 1
    else:
        return num * factorial(num-1)

output = factorial(n)

print (output)

