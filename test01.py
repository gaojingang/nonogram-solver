import numpy as np

def test01():
    maxNum = 1;
    for x in range(5, 26):
        if x % 2 == 0:
            maxNum = (int)(x / 2)
        else:
            maxNum = (int)(x / 2) + 1

        print("{}\t{}".format(x, maxNum))

def numpyTest01():
    # a = np.array(42)
    # b = np.array([1, 2, 3, 4, 5])
    # c = np.array([[1, 2, 3], [4, 5, 6]])
    # d = np.array([[[1, 2, 3], [4, 5, 6]], [[1, 2, 3], [4, 5, 6]]])
    #
    # print(a.ndim)
    # print(b.ndim)
    # print(c.ndim)
    # print(d.ndim)
    #
    # arr = np.array([1, 2, 3, 4], ndmin=5)
    #
    # print(arr)
    # print('number of dimensions :', arr.ndim)


    # arr = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])
    #
    # print('5th element on 2nd dim: ', arr[1, 4])

    arr = np.array([1, 2, 3, 4, 5, 6, 7])
    # 裁切从开头到索引 4（不包括）的元素：[1 2 3 4]
    print(arr[:4])
    # 从末尾开始的索引 3 到末尾开始的索引 1，对数组进行裁切： [5 6]
    print(arr[4:])
    print(arr[-3:-1])
    # 从索引 1 到索引 5，返回相隔的元素： [2 4 ]
    print(arr[1:5:2])
    # 返回数组中相隔的元素： [1 3 5 7]
    print(arr[::2])
    print ("=====================2D============================")
    # 裁切 2-D 数组
    arr = np.array([[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]])
    # 从第二个元素开始，对从索引 1 到索引 4（不包括）的元素进行切片：
    print(arr[1, 1:4])
    #     从两个元素中返回索引 2：
    print(arr[0:2, 2])
    #     从两个元素裁切索引 1 到索引 4（不包括），这将返回一个 2-D 数组：
    print(arr[0:2, 1:4])

def numpyTest02():
    arr = np.array([[1, 2, 3, 4], [5, 6, 7, 8]])
    # 打印 2-D 数组的形状： 例子返回 (2, 4)，这意味着该数组有 2 个维，每个维有 4 个元素。
    print(arr.shape)




if __name__ == '__main__':
    # test01()
    # numpyTest01()
    numpyTest02()



