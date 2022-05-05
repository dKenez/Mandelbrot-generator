import matplotlib.pyplot as plt
import numpy as np


def getBoundingBox(corner_1: complex, corner_2: complex) -> tuple[complex]:
    '''Return all the corners of the box parallel to axes defined by input corners. Return lower right first, then in order of positive rotation.'''
    c1 = complex(max(corner_1.real, corner_2.real),
                 min(corner_1.imag, corner_2.imag))
    c2 = complex(max(corner_1.real, corner_2.real),
                 max(corner_1.imag, corner_2.imag))
    c3 = complex(min(corner_1.real, corner_2.real),
                 max(corner_1.imag, corner_2.imag))
    c4 = complex(min(corner_1.real, corner_2.real),
                 min(corner_1.imag, corner_2.imag))

    return c1, c2, c3, c4


def create2DLinspace(corner_1: complex, corner_2: complex, h_num: int, v_num: int) -> np.ndarray:
    _, c2, _, c4 = getBoundingBox(corner_1, corner_2)
    hor_linspace = np.linspace(c4.real, c2.real, v_num).reshape((1, v_num))
    ver_linspace = np.linspace(c4.imag, c2.imag, h_num).reshape(
        (h_num, 1)) * complex(0, 1)

    real_2Dlinspace = np.repeat(hor_linspace, h_num, axis=0)
    imag_2Dlinspace = np.repeat(ver_linspace, v_num, axis=1)

    return real_2Dlinspace + imag_2Dlinspace


def mandel(c: complex, pow: float, max_iter: int):
    z = complex(0, 0)
    for i in range(max_iter):
        if abs(z) > 2:
            break
        z = z**pow + c

    return i


def plotMandel(arr: np.ndarray, filename):
    plt.imsave(filename, arr)

def createMandelbrotRender(corner_1: complex, corner_2: complex, h_num: int, v_num: int, pow: float, max_iter: int, filename: str):
    h = create2DLinspace(corner_1, corner_2, h_num, v_num)

    vfunc = np.vectorize(mandel)
    mandrend = vfunc(h, pow, max_iter)

    plotMandel(mandrend, filename)

def main():
    corner_1 = complex(-2, 1.125)
    corner_2 = complex(1, -1.125)

    hres = 500
    vres = 300

    pow = 2
    i = 100

    h = create2DLinspace(corner_1, corner_2, hres, vres)

    vfunc = np.vectorize(mandel)
    mandrend = vfunc(h, pow, i).astype("uint8")
    print(np.average(mandrend))

    plotMandel(mandrend)

if __name__ == "__main__":
    main()



