from PIL import Image
import numpy as np
import bitstring as bs
import sys, os


def write(fileName, infotoWrite, _label=""):
    im0 = Image.open(fileName)
    x = np.array(im0)

    fSize = x.ravel().shape[0]
    infoSize = len(infotoWrite)
    length = fSize if fSize < infoSize else infoSize
    for i in range(length):
        x.ravel()[i] = LSBReplace(x.ravel()[i], int(infotoWrite[i]))

    im1 = Image.fromarray(x)
    im1.save(fileName[:-4] + "_written" + _label + ".bmp")

    return (infoSize, fSize)


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

if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        fileName =sys.argv[1]
    else:
        print("未指定文件名")
        os._exit(0)
    for i in range(5):
        bits = getBitStr("m" + str(i+1) + ".zip")
        write(fileName, bits, _label=str(i+1))
    
    