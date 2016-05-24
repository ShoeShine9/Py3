
import sys


n = int(input().strip())
arr = [int(arr_temp) for arr_temp in input().strip().split(' ')]

newList = list(arr)
newList.reverse()


for l in newList:
    print (l, end=" ")