"""Get and print specific values and data from images for 
   debugging purposes"""

import numpy as np
from astropy.io import fits


def get_values_and_dtype(img_name, values_positions=[[0, 0],]):
    """Helper Function:
    Get values and data types from a given fit image. It verifies that 
    the values obtained in the images are the expected ones. 
    Inputs:
    values_positions: list of tuples with two elements each tuple (
        row, column); the tuples must indicate the positions from the 
        image elements to be returned"""
    hf = fits.open(img_name)
    img = hf[0].data
    hf.close()   
    values = []
    for row, col in values_positions:
        value = img[row, col]
        values.append(value)
    return values


def get_fit_img_shape_and_dtype(img_name):
    hf = fits.open(img_name)
    img = hf[0].data
    hf.close()
    print("Image dimensions: " + str(img.shape))
    print("Image type: " + str(img.dtype))


def verify_pixel():
    # Compare automatic and manual and assert they are almost equal
    pass

    
if __name__ == "__main__":

    get_fit_img_shape_and_dtype("master_bias.fit")
    print("\n")
            
    # Pixel [x, y]
    x = 531
    y = 2047
    pixel = [x, y]

    # master_bias Pixel[x, y]
    print("Pixel " + str(pixel) + " from master_bias.fit:")
    vals_in_xy_bias = get_values_and_dtype("master_bias.fit", 
                                           values_positions=[[x, y]])
    val_in_xy_bias = vals_in_xy_bias[0] 
    print(val_in_xy_bias)
    
    ##########################################################################
    ######### Pixel[x, y] on computed WASP-33-0073I_norm.fit #################
    print("\nI")
    exp_time_obj_I = 15.0
    exp_time_ff_I = 6.0

    print("Pixel " + str(pixel) + " on computed WASP-33-0073II_norm.fit:")
    vals_in_xy_obg_img_norm = get_values_and_dtype("WASP-33-0073I_norm.fit", 
                                                   values_positions=[[x, y]])
    val_in_xy_obg_img_norm = vals_in_xy_obg_img_norm[0]                                               
    print(val_in_xy_obg_img_norm)

    ### WASP-33-0073I Pixel[x, y] normalized value, 'manually' calculated ####
    print("Pixel " + str(pixel) + " from master_ff_I.fit:")
    vals_in_xy_ff_I = get_values_and_dtype("master_ff_I.fit", 
                                           values_positions=[[x, y]])
    val_in_xy_ff_I = vals_in_xy_ff_I[0]
    print(val_in_xy_ff_I)
                                          
    print("Pixel " + str(pixel) + " from WASP-33-0073I.fit:")                                      
    vals_in_xy_obj_img = get_values_and_dtype("WASP-33-0073I.fit", 
                                              values_positions=[[x, y]])
    val_in_xy_obj_img = vals_in_xy_obj_img[0]
    print(val_in_xy_obj_img)
    
    numerator = exp_time_ff_I * (val_in_xy_obj_img - val_in_xy_bias)
    denominator = exp_time_obj_I * val_in_xy_ff_I
    manually_calculated_xy_pixel_norm = np.float32(numerator / denominator)
    print("WASP-0073I pixel " + str(pixel) + " normalized value,"
          + " 'manually' calculated:")
    print(manually_calculated_xy_pixel_norm)
    
    ##########################################################################
    ######### Pixel[x, y] on computed WASP-33-0253B_norm.fit #################
    print("\nB")
    exp_time_obj_B = 30.0
    exp_time_ff_B = 6.0    

    print("Pixel " + str(pixel) + " on computed WASP-33-0253B_norm.fit:")
    vals_in_xy_obg_img_norm = get_values_and_dtype("WASP-33-0253B_norm.fit", 
                                                   values_positions=[[x, y]])
    val_in_xy_obg_img_norm = vals_in_xy_obg_img_norm[0]                                               
    print(val_in_xy_obg_img_norm)

    ### WASP-33-0253B Pixel[x, y] normalized value, 'manually' calculated ####
    print("Pixel " + str(pixel) + " from master_ff_B.fit:")
    vals_in_xy_ff_B = get_values_and_dtype("master_ff_B.fit", 
                                           values_positions=[[x, y]])
    val_in_xy_ff_B = vals_in_xy_ff_B[0]
    print(val_in_xy_ff_B)
                                          
    print("Pixel " + str(pixel) + " from WASP-33-0253B.fit:")                                      
    vals_in_xy_obj_img = get_values_and_dtype("WASP-33-0253B.fit", 
                                              values_positions=[[x, y]])
    val_in_xy_obj_img = vals_in_xy_obj_img[0]
    print(val_in_xy_obj_img)
    
    numerator = exp_time_ff_B * (val_in_xy_obj_img - val_in_xy_bias)
    denominator = exp_time_obj_B * val_in_xy_ff_B
    manually_calculated_xy_pixel_norm = np.float32(numerator / denominator)
    print("WASP-0253B pixel " + str(pixel) + " normalized value,"
          + " 'manually' calculated:")
    print(manually_calculated_xy_pixel_norm)
    ##########################################################################


