import numpy as np
from PIL import Image, ImageDraw

def circle(img, center = 0, radius = 360):
    
    img = Image.fromarray((img * 1).astype(np.uint8)).convert('RGB')


    npImage = np.array(img)
    h, w = img.size

    alpha = Image.new('L', img.size, 0)
    draw = ImageDraw.Draw(alpha)
    draw.pieslice([30, 20, h, w], 0, 360, fill = 255)

    # Convert alpha Image to numpy array
    npAlpha=np.array(alpha)
    
    return Image.fromarray(np.dstack((npImage, npAlpha)))

def rectangle(img, x = 30, y = 20):
    
    img = np.array(img)                                              
    h = img.shape[0]
    w = img.shape[1]
    
    return img[y: y + h, x: x + w]