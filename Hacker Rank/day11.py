arr = []

for arr_i in range(6):
    arr_t = [int(arr_temp) for arr_temp in input().strip().split(' ')]
    arr.append(arr_t)

sumMax = -100
total = -100

for i in range(0, 4):
    for j in range(0, 4):
        sum1 = arr[j][i] + arr[j][i + 1] + arr[j][i + 2]
        sum2 = arr[j + 1][i + 1]
        sum3 = arr[j + 2][i] + arr[j + 2][i + 1] + arr[j + 2][i + 2]
        total = sum1 + sum2 + sum3

        if total > sumMax:
            sumMax = total
print(sumMax)


