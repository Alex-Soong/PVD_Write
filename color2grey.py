from PIL import Image
import numpy as np
import sys, os


def color2grey(fileName):
    im0 = Image.open(fileName)
    x = np.array(im0)

    im1 = Image.fromarray(x)
    im1 = im1.convert('L')

    if fileName[-4:] == ".bmp":
        saveFileName = fileName[:-4] + "_grey.bmp"
    else:
        saveFileName = fileName + "_grey.bmp"

    im1.save(saveFileName)


if __name__ == '__main__':
    
    if len(sys.argv) > 1:
        inputFileName = sys.argv[1]
    else:
        print("未指定文件名")
        os._exit(0)

    color2grey(inputFileName)