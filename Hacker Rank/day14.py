class Difference:
    def __init__(self, a):
        self.__elements = a


    def computeDifference(self):
        max_diff = 0
        for el in self.__elements:
            for rest in self.__elements:
                cur_diff = abs(el-rest)
                if cur_diff > max_diff:
                    max_diff = cur_diff

    def maximumDifference(self):
        return max_diff

# End of Difference class

_ = input()
a = [int(e) for e in input().split(' ')]

d = Difference(a)
d.computeDifference()

print(d.maximumDifference)