from os import path, makedirs
from timeit import default_timer as timer
from numba import jit
import cv2
import numpy as np
from PIL import Image


def main(f_name, f_iter):  # , m_iter):
    escape = False
    scale_x, scale_y, res_x, res_y = 16, 9, 1920, 1080
    re_0, im_0, re_n, im_n = -2, 1.125, 2, -1.125
    power, max_iter = 2, 150  # m_iter
    while not escape:
        usr_inp = input("Use default settings? (y/n):")
        if usr_inp.lower() == 'y' or usr_inp.lower() == "yes":
            escape = True

        elif usr_inp.lower() == 'n' or usr_inp.lower() == "no":
            scale_x, scale_y, res_x, res_y, re_0, im_0, re_n, im_n, power, max_iter = usr_inputs()
            escape = True

        else:
            print("Invalid input, try again!\n")
        print()

    print(
        "aspect ratio: ", scale_x, ":".lstrip(), scale_y, "\n",
        "resolution: ", res_x, "x", res_y, "\n",
        "range:  ", re_0, "+", im_0, "i\t", re_n, "+", im_0, "i\n\t\t", re_0, "+", im_n, "i\t", re_n, "+", im_n, "i\n",
        "power: ", power, "\n",
        "max iterations: ", max_iter, "\n", sep=''
    )

    escape = False
    while not escape:
        usr_inp = input("Accept settings? (y/n):")
        if usr_inp.lower() == 'y' or usr_inp.lower() == "yes":
            escape = True

        elif usr_inp.lower() == 'n' or usr_inp.lower() == "no":
            return 0

        else:
            print("Invalid input, try again!\n")
        print()

    if res_x * res_y * max_iter >= 5000 * 5000 * 150:
        print("Due to the size of the image, check the preview to ensure correct settings:")
        array = calc_array(int((720/res_y)*res_x), 720, re_0, im_0, re_n, im_n, power, max_iter)
        np_to_png(array, "preview", 0)

        escape = False
        while not escape:
            usr_inp = input("Accept settings? (y/n):")
            if usr_inp.lower() == 'y' or usr_inp.lower() == "yes":
                escape = True

            elif usr_inp.lower() == 'n' or usr_inp.lower() == "no":
                return 0

            else:
                print("Invalid input, try again!\n")
            print()

    start_1 = timer()
    array = calc_array(res_x, res_y, re_0, im_0, re_n, im_n, power, max_iter)
    time_1 = timer() - start_1
    print("op1 done\n")
    start_2 = timer()
    np_to_png(array, f_name, f_iter)
    time_2 = timer() - start_2
    print("op2 done\n")

    print("resolution: ", res_x, "x", res_y, sep="")
    print("iteration cap:", max_iter)
    print("file id.:", f_iter)
    print("op1 duration:", time_1)
    print("op2 duration:", time_2)
    print("overall duration:", time_1 + time_2)

    return 1


def usr_inputs():
    # get aspect ration
    escape = False
    scale_x = 16
    scale_y = 9
    while not escape:
        usr_inp = input("Set aspect ratio? (default is 16:9) (y/n):")

        if usr_inp.lower() == 'y' or usr_inp.lower() == "yes":
            try:
                scale_x = int(input("Set aspect ratio x-scale: "))
                if scale_x <= 0:
                    raise ValueError
            except ValueError:
                print("Invalid input, must be a positive, non-zero integer!\n")
                continue
            try:
                scale_y = int(input("Set aspect ratio y-scale: "))
                if scale_y <= 0:
                    raise ValueError
            except ValueError:
                print("Invalid input, must be a positive, non-zero integer!\n")
                continue
            escape = True

        elif usr_inp.lower() == 'n' or usr_inp.lower() == "no":
            escape = True

        else:
            print("Invalid input, try again!\n")
        print()

    # get resolution
    escape = False
    res_x = 1920
    res_y = 1080
    while not escape:
        usr_inp = input("Choose which resolution to set (w/h):")

        if usr_inp.lower() == 'w' or usr_inp.lower() == "width":
            try:
                res_x = int(input("Set x resolution: "))
                if res_x <= 0:
                    raise ValueError
            except ValueError:
                print("Invalid input, must be a positive non-zero integer!\n")
                continue
            res_y = int((res_x / scale_x) * scale_y)
            escape = True

        if usr_inp.lower() == 'h' or usr_inp.lower() == "height":
            try:
                res_y = float(input("Set y resolution: "))
                if res_y <= 0:
                    raise ValueError
            except ValueError:
                print("Invalid input, must be a positive non-zero integer!\n")
                continue
            res_x = int((res_y / scale_y) * scale_x)
            escape = True
    print()

    # get start coordinate
    escape = False
    re_0 = -2
    im_0 = 1.125
    while not escape:
        usr_inp = input("Set starting coordinate? (top left corner, default is -2 + 1.125i) (y/n):")

        if usr_inp.lower() == 'y' or usr_inp.lower() == "yes":
            try:
                re_0 = float(input("Set real component: "))
            except ValueError:
                print("Invalid input, try again!\n")
                continue
            try:
                im_0 = float(input("Set complex component: "))
            except ValueError:
                print("Invalid input, try again!\n")
                continue
            escape = True

        elif usr_inp.lower() == 'n' or usr_inp.lower() == "no":
            escape = True

        else:
            print("Invalid input, try again!\n")
        print()

    # get end coordinate
    escape = False
    re_n = 2
    im_n = -1.125
    while not escape:
        usr_inp = input("Choose which ending coordinate to set (bottom right corner) (re/im):")

        if usr_inp.lower() == 'r' or usr_inp.lower() == "re" or usr_inp.lower() == "real":
            try:
                re_n = float(input("Set real component: "))
                if re_n <= re_0:
                    raise ValueError
            except ValueError:
                print("Invalid input, must be larger than the real part of the starting coordinate!", re_0, "\n")
                continue
            im_n = im_0 - (((re_n - re_0)/scale_x) * scale_y)
            escape = True

        elif usr_inp.lower() == 'i' or usr_inp.lower() == "im" or usr_inp.lower() == "complex":
            try:
                im_n = float(input("Set complex component: "))
                if im_n >= im_0:
                    raise ValueError
            except ValueError:
                print("Invalid input, must be smaller than the complex part of the starting coordinate!", im_0, "\n")
                continue
            re_n = re_0 + (((im_0 - im_n) / scale_y) * scale_x)
            escape = True

        else:
            print("Invalid input, try again!\n")
        print()

    # get power value
    escape = False
    power = 2
    while not escape:
        try:
            power = float(input("Set the power used during calculation:"))
            escape = True
        except ValueError:
            print("Invalid input, try again!\n")
            continue
        print()

    # get max iteration value
    escape = False
    max_iter = 150
    while not escape:
        try:
            max_iter = int(input("Set max iterations:"))
            if max_iter <= 0:
                raise ValueError
            escape = True
        except ValueError:
            print("Invalid input, must be a positive non-zero integer!\n")
            continue
        print()

    return scale_x, scale_y, int(res_x), int(res_y), re_0, im_0, re_n, im_n, power, int(max_iter)


@jit
def calc_array(res_x, res_y, re_0, im_0, re_n, im_n, power, max_iter):
    array = np.zeros(shape=(res_y, res_x), dtype=float)
    s_x = (re_n - re_0) / res_x
    s_y = (im_0 - im_n) / res_y

    if im_0 + im_n < 0.00001:
        for j in range(int(res_y / 2)):
            if j % 50 == 0:
                print(j)
            for i in range(res_x):
                c = complex(re_0 + i*s_x, im_0 - j*s_y)
                array[j, i] = iter_z(c, power, max_iter)
        for j in range(int(res_y / 2)):
            array[res_y - j - 1] = array[j]

    else:
        for j in range(res_y):
            if j % 50 == 0:
                print(j)
            if abs(im_0 - j*s_y) < (im_0 + im_n) / (res_y*2):
                array[j] = array[j-1]
            else:
                for i in range(res_x):
                    c = complex(re_0 + i*s_x, im_0 - j*s_y)
                    array[j, i] = iter_z(c, power, max_iter)
    return array


@jit
def iter_z(c, power, max_iteration):
    iteration = 0
    z = c
    c = complex(-0.8, 0)
    while abs(z) <= 2 and iteration < max_iteration:
        z = (z ** power) + c
        iteration += 1

    '''if iteration == max_iteration:
        iteration = 0'''
    return iteration # % max_iteration

    # '''iteration = 0
    # z = complex()
    # while abs(z) <= 2 and iteration < max_iteration:
    #     z = (z ** power) + c
    #     iteration += 1
    #
    # #if iteration == max_iteration:
    #     iteration = 0
    # return iteration  # % max_iteration'''


@jit
def np_to_png(mx, f_name, f_iter):
    mx = abs(mx)
    maximum = max(np.amax(mx), 1)
    mx = mx.astype(np.float64) / maximum
    mx = 255 * mx
    data = mx.astype(np.uint8)
    cv2.imwrite(f_name + str(f_iter) + ".png", data)
    f_path = f_name + str(f_iter) + ".png"
    img = Image.open(f_path)
    img.show()


for i in range(149):
    file_name = r"images\mandelbrot_"
    file_iter = 0

    if not path.isdir("images"):
        makedirs("images")

    while path.isfile(file_name + str(file_iter) + ".png"):
        file_iter += 1
    while not main(file_name, file_iter):#, i+1):
        pass
