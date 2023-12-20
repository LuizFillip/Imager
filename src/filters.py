import numpy as np
from skimage import io
import imager as im
from scipy.ndimage import median_filter


def vanRhijn_atmExtinction(img, fname, a=0.2, Ftheta=0, height = 250):
    Re = 6730
    xsize, ysize = img.shape

    # Re = im.constants.equator_radius
    attrs = im.get_attributes(fname)
    xm, ym = attrs.xm, attrs.ym

    z = np.arange(181) * 0.5 * (np.pi / 180)
    fitting = np.polyfit(
        im.lens_function(z, attrs), 
        z * 180 / np.pi, 4)[::-1]

    vr = np.zeros((xsize, ysize))
    ae = np.zeros((xsize, ysize))
    ang = np.zeros((xsize, ysize))

    # height = im.constants.emission_band()

    for i in range(xsize):
        for j in range(ysize):
            dx = np.sqrt((i - xm) ** 2 + (j - ym) ** 2)

            ang[i, j] = (fitting[0] +
                         fitting[1] * dx + 
                         fitting[2] * dx ** 2 + 
                         fitting[3] * dx ** 3 + 
                         fitting[4] * dx ** 4)

            sin_ang = np.sin(np.radians(ang[i, j]))
            vr[i, j] = 1 / np.sqrt(1 - (Re / (Re + height) ** 2) * sin_ang ** 2)

            cos_ang = np.cos(np.radians(ang[i, j]))
            Ftheta = 1 / (cos_ang + 0.15 * (93.885 - ang[i, j]) ** -1.253)
            ae[i, j] = 10 ** (-0.4 * a * Ftheta)

            if ang[i, j] > 90:
                ae[i, j] *= 0  # Multiplying by 0 is equivalent to setting it to 0 directly

    return ae, vr


def remove_stars(
        image, 
        starsize = 5, 
        threshold = 50
        ):
    
    a_filtered = median_filter(
        image, size = starsize)

    a_final = np.where(
        (image - a_filtered) > threshold, 
        a_filtered, image)

    return a_final



def main():

    fname = "database/examples/OH_CA_20181112_002024.tif" 
    
    img = io.imread(fname, as_gray = True)
    
    ae, vr = vanRhijn_atmExtinction(img, a = 0.2, Ftheta = 0)
