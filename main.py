from os import path
from timeit import default_timer as timer
from numba import jit
import csv
import cv2
import numpy as np


@jit
def calc_z(z, c, p):
    z = (z ** p) + c
    return z


@jit
def iterate(c, max_iteration, p):
    iteration = 0
    z = complex()
    while abs(z) <= 2 and iteration < max_iteration:
        z = calc_z(z, c, p)
        iteration += 1
    return iteration


@jit
def re_map(mx):  # Map
    mx = abs(mx)
    maximum = np.amax(mx)
    mx = mx.astype(np.float64) / maximum
    mx = 255 * mx
    mx = mx.astype(np.uint8)
    return mx


@jit
def to_np(file):
    reader = csv.reader(file, delimiter=',')
    d = list(reader)
    d = np.array(d).astype(float)
    return d


def mandelbrot(res, max_iter, p):
    # start_0 = timer()
    file_name = r"csv_1\mandel_"
    file_iter = 0
    while path.isfile(file_name + str(file_iter) + ".csv"):
        file_iter += 1
    f = open(file_name + str(file_iter) + ".csv", "a")

    im0 = 1.5
    re0 = -(im0/9)*16
    s_y = im0*2
    s_x = (im0/9)*32


    '''running_val = 0

    duration_0 = timer() - start_0
    start_1 = timer()'''

    for j in range(int(res/2)):
        for i in range(int((res/s_y)*s_x)):
            C = complex(re0+((s_x*i)/((res/s_y)*s_x)), im0 - ((s_y / 2) * j/(res/2)))

            curr_iter = iterate(C, max_iter, p)

            if i < int((res/s_y)*s_x - 1):
                f.write(str(curr_iter)+",".rstrip('\n'))
            else:
                f.write(str(curr_iter)+'\n')
                '''running_val += 1
                if running_val % 10 == 0:
                    print(running_val)
    print("\nfinished op1")'''
    f.close()

    '''duration_1 = timer()-start_1
    start_2 = timer()'''

    lines = []
    f = open(file_name + str(file_iter) + ".csv", 'r')
    for line in f:
        lines.append(line)
    f.close()

    '''print("finished op2")

    duration_2 = timer() - start_2
    start_3 = timer()'''

    f = open(file_name + str(file_iter) + ".csv", 'a')
    for line in range(len(lines)):
        f.write(lines[len(lines)-line-1])

    f.close()

    '''print("finished op3")

    duration_3 = timer() - start_3
    start_4 = timer()'''

    data_path = file_name + str(file_iter) + ".csv"

    with open(data_path, 'r') as f:
        data = to_np(f)

    data = re_map(data)

    cv2.imwrite(r"png_1\output_" + str(file_iter) + ".png", data)

    '''print("finished op4\n")

    duration_4 = timer() - start_4
    duration_all = timer() - start_0
    
    print("res:", int(res/s_y)*s_x, "x", res)
    print("iteration cap:", max_iter)
    print("file id.:", file_iter)
    print("init duration:", duration_0)
    print("op1 duration:", duration_1)
    print("op2 duration:", duration_2)
    print("op3 duration:", duration_3)
    print("op4 duration:", duration_4)
    print("overall duration:", duration_all)'''
    return 1


print("Input resolution of mandelbrot set:")
resol = int(input())
if resol % 2 == 1:
    resol -= 1

print("Input iteration threshold of mandelbrot set:")
max_iterat = int(input())

print("Input starting power:")
power_start = float(input())

print("Input ending power:")
power_end = float(input())

print("Input increment resolution:")
power_res = int(input())

for g in range(power_res+1):
    power = power_start + ((power_end-power_start)/power_res)*g
    mandelbrot(resol, max_iterat, power)
    print("png", g, "done")


