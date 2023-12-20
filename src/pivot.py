import cv2


def flip(img, dat):
        
    if dat["Vertical   Flip"] == "OFF": image = img[::-1, :]
    if dat["Horizontal Flip"] == "OFF": image = img[:, ::-1]
    
    # if hori_flip: new_img = np.fliplr(new_img)
    # if vert_flip: new_img = np.flipud(new_img)

    return image


def rotate(array, dat):
    """
    Image rotation
    """
    angle = float(dat["Rotation"])

    height, width = array.shape[:2]
    rotation_matrix = cv2.getRotationMatrix2D(
        (width / 2, height / 2), angle, 1)
    
    rotated_array = cv2.warpAffine(
        array, rotation_matrix, 
        (width, height),
        flags = cv2.INTER_LINEAR)
    
    return rotated_array
