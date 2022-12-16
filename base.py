import numpy as np


def getlevel(array, sref):
    # array : array input
    # sref : reference ratio levels
    # slevels : output levels

    a = np.uint16(array)
    maximo = np.amax(a)

    hist, _ = np.histogram(a, range=(0, maximo), 
                           bins= maximo + 1)

    ksize = len(hist)
    ta = np.sum(hist)

    ssize = len(sref)
    slevels = np.zeros(ssize, dtype=float)

    sa, i = np.uint64(0), np.uint64(0)
      
    while i < ksize - 1:
        i += 1
        sa = sa + hist[int(i)]
        
        for j in range(ssize):
            
            if sa < sref[j]*ta:
                slevels[j] = i

    return slevels

def bytscl(array, max_slevel, min_slevel):
    top = np.uint16(2**16-1) #Top value of an array of 16bits

    dim_x, dim_y = array.shape
    
    for j in range(dim_x):
        for i in range(dim_y):
            if min_slevel <= array[i, j] <= max_slevel:
                array[i,j] = (top + 1)*(array[i,j] - min_slevel-1)/(max_slevel-min_slevel)
            elif array[i,j]> max_slevel:
                array[i,j]=top
            elif array[i,j]<min_slevel:
                array[i,j]=0
    
    return array


def run_byteScale(img, limits = [0.2, 0.95]):
    """Apply get level and bytescale into an image"""
    slevels = getlevel(img, limits)
    
    return bytscl(img, slevels[1], slevels[0])



def bytscl2(array, 
            maximum = None, 
            minimum = None, nan = 0, top=255):
    # see http://star.pst.qub.ac.uk/idl/BYTSCL.html
    # note that IDL uses slightly different formulae for bytscaling floats and ints.
    # here we apply only the FLOAT formula...

    if maximum is None: maximum = np.nanmax(array)
    if minimum is None: mininum = np.nanmin(array)

    # return (top+0.9999)*(array-min)/(max-min)
    return np.maximum(np.minimum(
        ((top + 0.9999) * (array - min) / (max - min)).astype(np.int16), top), 0)


def getlevel2(im2, sref_min, sref_max):
    '''
    :param im2: imagem tipo float
    :param sref_min: nivel de referencia normalizado
    :param sref_max: nivel de referencia normalizado
    :return: limites inferior e superior da imagem para exibição na tela, 
    baseado nos niveis de referencia.
    '''
    #
    x_min, x_max = np.min(im2), np.max(im2)

    # bin_size precisa ser 1 para analisar ponto à ponto
    bin_size = 1
    x_min = 0.0

    nbins = np.floor(((x_max - x_min) / bin_size))

    try:
        hist, bins = np.histogram(im2, 
                                     int(nbins), 
                                     range = [x_min, x_max])

        sum_histogram = np.sum(hist)

        sref = np.zeros(2) 
        sref[0] = sref_min
        sref[1] = sref_max

        res_sa = np.zeros(len(hist))

        sa = 0.
        for i in range(len(hist)):
            sa += hist[i]
            res_sa[i] = sa

        res_sa2 = res_sa.tolist()
        res = res_sa[np.where((res_sa > sum_histogram * sref[0]) & 
                             (res_sa < sum_histogram * sref[1]))]
        nr = len(res)

        sl0 = res_sa2.index(res[0])
        sl1 = res_sa2.index(res[nr - 1])
        slevel = [sl0, sl1]
        
    except Exception as e:
        print("Exception get_level ->" + str(e))
        print("slevel = [10, 20]")
        slevel = [10, 20]

    return slevel