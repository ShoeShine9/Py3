import sys

numNames = int(input())

book = {}

for i in range(numNames):
    contact = input().split()
    book [contact[0]] = contact[1]
    
lines = sys.stdin.readlines()
for i in lines: 
    name = i.strip()
    if name in book:
        print (name + '=' + str(book[name]))
    else:
        print ('Not found')
