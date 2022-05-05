
import argparse
from mandelbrot import createMandelbrotRender


def validateCorners(left_corner: list[int], right_corner: list[int]):
    left_corner_cplx = complex(*left_corner)
    right_corner_cplx = complex(*right_corner)

    if not left_corner_cplx.real < right_corner_cplx.real:
        print("Left corner is not to the left of right corner!")
        exit()


def validateAspectRatio(ar: str):
    split = ar.split(':')
    if not len(split) == 2:
        print("Error when parsing aspect ratio!")
        exit()

    return int(split[0])/int(split[1])


def validateResolution(hres: int, vres: int):
    if not hres and not vres:
        print("Vertical or Horizontal resolution must be given!")
        exit()


def main():
    parser = argparse.ArgumentParser(
        description='Render Mandelbrot and save it to file.')

    # arguments
    parser.add_argument('filename', type=str,
                        help='Destination file of the render.')

    # optional args
    # aspect ratio
    parser.add_argument('-a', '--aspect-ratio', type=str, default='16:9',
                        help='Set aspect ratio of render. This option will be discarded if both --hres and --vres or both -l and -r are set.')
    parser.add_argument('-m', '--mirror', action='store_true',
                        help='Computes only half the area of the bounding box, mirrors the result and appends it to the bottom of the array. In this case only -l or -r should be given, the given corner determines the direction relative to the corner. If both -l and -r are supplied -l will be taken into account when determining the bounding box.')

    # resolution
    parser.add_argument('--hres', type=int,
                        help='Set horizontal resolution of render. --hres takes precedence if both --l and --r are set.')
    parser.add_argument('--vres', type=int,
                        help='Set vertical resolution of render. --hres takes precedence if both --l and --r are set.')

    # bounding box corners
    parser.add_argument('-l', '--left-corner', type=float, nargs=2,
                        help='Set left corner of bounding box. Make sure -l and -r have different coordinates')
    parser.add_argument('-r', '--right-corner', type=float, nargs=2,
                        help='Set right corner of bounding box. Make sure -l and -r have different coordinates.')

    # compute options
    parser.add_argument('-i', '--max-iter', type=int, default=100,
                        help='Set max iterations for determining convergence.')
    parser.add_argument('-p', '--power', type=float, default=2,
                        help='Set the value of the exponent in the formula: Z_(n+1) = Z_(n)^p + C.')

    # auto-input yes
    parser.add_argument('-y', action='store_false',
                        help='Skip parameter check.')

    args = parser.parse_args()

    filename = args.filename
    mirror = args.mirror
    aspect_ratio = validateAspectRatio(args.aspect_ratio)
    hres = args.hres
    vres = args.vres
    left_corner = args.left_corner
    right_corner = args.right_corner
    max_iter = args.max_iter
    power = args.power

    validateResolution(vres, hres)

    if left_corner is None and right_corner is None:
        print("No corners defined!")
        exit()
    elif left_corner and right_corner:
        validateCorners(left_corner, right_corner)

        aspect_width = abs(left_corner[0] - right_corner[0])
        aspect_height = abs(left_corner[1] - right_corner[1])

        aspect_ratio = aspect_width / aspect_height
        hres = hres or int(vres / aspect_ratio)
        vres = vres or int(hres * aspect_ratio)
    else:
        if not mirror:
            print(
                "Both corners of the bounding box need to be defined if mirror mode is off!")
            exit()

        hres = hres or int(vres / aspect_ratio)
        vres = vres or int(hres * aspect_ratio)

        aspect_ratio = vres / hres

        if left_corner is None:
            # calculate left corner
            re = right_corner[0] - abs(2*right_corner[1])*aspect_ratio
            left_corner = [re, 0]
        else:
            # calculate right corner
            re = left_corner[0] + abs(2*left_corner[1])*aspect_ratio
            left_corner = [re, 0]

    if args.y:
        print(f'''The following parameters were calculated from the input:

        {filename = }
        {mirror = }
        aspect_ratio = {aspect_ratio*9:.2f}:9
        {hres = }px
        {vres = }px
        left_corner = {complex(*left_corner)}
        right_corner = {complex(*right_corner)}
        {max_iter = }
        {power = }
        ''')

        if input('Continue? [y/n]: ').lower() != 'y':
            exit()

    createMandelbrotRender(complex(*left_corner), complex(*right_corner), hres, vres, power, max_iter, filename)

if __name__ == "__main__":
    main()
