from PIL import Image
import numpy as np
import bitstring as bs
import sys, os


def zigzag(_matrix):
    m, n = _matrix.shape
    lst_x = []
    lst_y = []
    x, y = 0, 0
    slope = True
    for i in range(m * n):
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
    return (lst_x, lst_y)


# 计算log2wk和lk
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
            

def writeInPair(_p1, _p2, _b, _lk):
    d = _p2 - _p1
    dp = 0
    p1, p2 = 0, 0
    if d >= 0:
        dp = _lk + _b
    else:
        dp = -(_lk + _b)
    rf = (dp - d) // 2
    rc = dp - d - rf
    if d % 2 == 1:
        p1 = _p1 - rc
        p2 = _p2 + rf
    else:
        p1 = _p1 - rf
        p2 = _p2 + rc
    return (p1, p2)


def bits2int(_bits):
    a = bs.BitArray("0b" + _bits)
    return a.uint


def write(fileName, infotoWrite):
    im0 = Image.open(fileName)
    m = np.array(im0)
    lst_x, lst_y = zigzag(m)
    for i in range(0, len(lst_x), 2):
        x1, y1, x2, y2 = lst_x[i], lst_y[i], lst_x[i+1], lst_y[i+1]
        p1, p2 = m[x1][y1], m[x2][y2]
        
        leng, lk = calcuSize(p1, p2)
        if leng < len(infotoWrite):
            str = infotoWrite[:leng]
            infotoWrite = infotoWrite[leng:]
        else:
            str = infotoWrite
        b = bits2int(str)
        p1_, p2_ = writeInPair(p1, p2, b, lk)
        m[x1][y1], m[x2][y2] = p1_, p2_
        if len(infotoWrite) == 0:
            break
    im1 = Image.fromarray(m)
    im1.save(fileName[:-4] + "_written" + ".bmp")


def getBitStr(fileName):
    f = open(fileName, "rb")
    str = f.read()
    str = bs.BitArray(str).bin
    return str



# if __name__ == '__main__':

#     if len(sys.argv) > 2:
#         inputFileName0 = sys.argv[1]
#         inputFileName1 = sys.argv[2]
#     else:
#         print("未指定文件名")
#         os._exit(0)
#     bits = getBitStr(inputFileName1)
#     write(inputFileName0, bits)

# if __name__ == '__main__':
    
#     if len(sys.argv) > 1:
#         fileName =sys.argv[1]
#     else:
#         print("未指定文件名")
#         os._exit(0)
#     for i in range(5):
#         bits = getBitStr("m" + str(i+1) + ".zip")
#         write(fileName, bits, _label=str(i+1))
    

a = np.array([[1,2,3,4],[5,6,7,8],[9,10,11,12]])
b = np.array([[1, 2, 3],[4,5,6],[7,8,9]])

print(zigzag(b))
print(zigzag(a))
c = "abc"
print(c[:5])
print(c[5:])

print(bits2int("1000110"))    