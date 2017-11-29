# -*-coding:utf-8-*-
import time
import random


class Math:
    # 求极差
    @staticmethod
    def range(l):
        return max(l) - min(l)

    # 求平均数
    @staticmethod
    def avg(l):
        return float(sum(l)) / len(l)

    # 求中位数
    @staticmethod
    def median(l):
        l = sorted(l)  # 先排序
        if len(l) % 2 == 1:
            return l[len(l) / 2]
        else:
            return (l[len(l) / 2 - 1] + l[len(l) / 2]) / 2.0

    # 求方差
    @staticmethod
    def variance(l):  # 平方的期望-期望的平方
        s1 = 0
        s2 = 0
        for i in l:
            s1 += i ** 2
            s2 += i
        return float(s1) / len(l) - (float(s2) / len(l)) ** 2

    # 求方差2
    @staticmethod
    def variance2(l):  # 平方-期望的平方的期望
        ex = float(sum(l)) / len(l)
        s = 0
        for i in l:
            s += (i - ex) ** 2
        return float(s) / len(l)

        # 主函数，测试


arr = [1, 2, 3, 2, 3, 1, 4]
print "极差为：{0}".format(Math.range(arr))
print "平均数为：{0:.2f}".format(Math.avg(arr))
print "中位数为：{0}".format(Math.median(arr))
print "方差为：{0:.2f}".format(Math.variance(arr))
print "方差为：{0:.2f}".format(Math.variance2(arr))

print

# 性能测试
arraylist = []
for i in range(1, 1000000):
    arraylist.append(i)
random.shuffle(arraylist)
time_start = time.time()
print "方差为：{0:.2f}".format(Math.variance(arraylist))
time_end = time.time()
print "{0}s".format(time_end - time_start)
time_start = time.time()
print "方差为：{0:.2f}".format(Math.variance2(arraylist))
time_end = time.time()
print "{0}s".format(time_end - time_start)