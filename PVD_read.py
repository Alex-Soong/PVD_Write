from PIL import Image
import numpy as np
import bitstring as bs
import sys, os


# 之字形遍历，返回横纵坐标序列。参数pairCount是像素的个数
def zigzag(_matrix, _count=0):
    
    m, n = _matrix.shape
    lst_x = []
    lst_y = []
    x, y = 0, 0
    slope = True   # 表示上一步是否为斜线移动
    num = min(m * n, 2 * _count)
    for i in range(num):
        # print(x, y, i)
        lst_x.append(x)
        lst_y.append(y)
        if (x == 0 or x == m - 1) and y < n - 1 and slope == True:
            y += 1
            slope = False
        elif (y == 0 or y == n - 1) and x < m - 1 and slope == True:
            x += 1
            slope = False
        elif (x + y) % 2 == 0:
            x, y = x - 1, y + 1
            slope = True
        else:
            x, y = x + 1, y - 1
            slope = True
    return lst_x, lst_y


# 计算一个像素对儿的log2wk和lk
def calcuSize(_p1, _p2):
    ranks = [[0, 7], [8, 15], [16, 31], [32, 63], [64, 127], [128, 255]]
    logs = [3, 3, 4, 5, 6, 7]
    d = _p2 - _p1
    if d < 0:
        d = -d
    for i in range(6):
        if d >= ranks[i][0] and d <= ranks[i][1]:
            return (logs[i], ranks[i][0])
    return (0, 0)


# fileName = "2333_grey_written.bmp"
def read(fileName, pairCount):

    res = ""
    im = Image.open(fileName)
    m = np.array(im)
    lst_x, lst_y = zigzag(m, pairCount)
    pointNum = len(lst_x)
    for i in range(0, pointNum, 2):
        x1, y1, x2, y2 = lst_x[i], lst_y[i], lst_x[i+1], lst_y[i+1]
        p1, p2 = int(m[x1][y1]), int(m[x2][y2])
        leng, lk = calcuSize(p1, p2)
        d = p2 - p1
        b = abs(d) - lk
        bits = bs.BitArray(uint=b, length=leng).bin
        if bits != "0":
            res = res + bits
    k = len(res) % 8
    if k > 0:
        res = res[:-k]
    return res 
    
    
    # ret = ""        
    # im0 = Image.open(fileName)
    # x = np.array(im0)

    # fSize = x.ravel().shape[0]
    
    # if readLength == -1:
    #     length = fSize
    # else:
    #     length = readLength if readLength < fSize else fSize

    # for i in range(length):
    #     t = x.ravel()[i] % 2
    #     ret = ret + str(t)

    # return ret


if __name__ == '__main__':
    
    if len(sys.argv) > 2:
        inputFileName = sys.argv[1]
        pairCount = sys.argv[2]
    else:
        print("未指定文件名或像素对个数")
        os._exit(0)
    if len(sys.argv) > 3:
        saveFileName = sys.argv[3]
    else:
        saveFileName = "m_get.zip"
        
    
    bits = read(inputFileName, int(pairCount))
    print("读到的比特串长度：", len(bits))
    print("读到的比特串开头：", bits[:100])
    print("读到的比特串结尾：", bits[-100:])
    f = open(saveFileName, 'wb')
    bs.BitArray('0b' + bits).tofile(f)
    print("读出的信息已保存至", saveFileName)
    # str = bs.BitArray(uint=512, length=10)
    # str = str.bin
