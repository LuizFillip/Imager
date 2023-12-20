import numpy as np

def getlevel(array, sref):
    a = np.uint16(array)
    max_val = np.max(a)

    hist, _ = np.histogram(a, bins=max_val + 1)

    ta = np.sum(hist)
    ssize = len(sref)
    slevels = np.zeros(ssize, dtype=float)

    sa = np.uint64(0)
    cumulative_sum = np.cumsum(hist)

    for j in range(ssize):
        sa = sref[j] * ta
        idx = np.argmax(cumulative_sum >= sa)
        slevels[j] = idx

    return slevels



def bytscl(array, max_slevel, min_slevel):
    top = np.uint16(2**16 - 1)  # Top value of a 16-bit array
    scaled_array = np.clip(
        ((top + 1) * (array - min_slevel - 1) / 
         (max_slevel - min_slevel)), 0, top)
    
    scaled_array[array > max_slevel] = top
    scaled_array[array < min_slevel] = 0
    
    return scaled_array



def contrast_adjust(img, limits = [0.2, 0.95]):
    """Apply get level and bytescale into an image"""
    slevels = getlevel(img, limits)
    
    return bytscl(img, slevels[1], slevels[0])
