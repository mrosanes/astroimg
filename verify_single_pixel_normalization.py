"""Get and print specific values and data from images for 
   debugging purposes"""

import os
import numpy as np
from astropy.io import fits


def get_values(img_name, values_positions=[[0, 0],]):
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


def verify_pixel(prefix_obj_name="WASP-33-", image_number=1, filter="I", 
                 pixel_pos=[0, 0], master_bias_fname="master_bias.fit" , 
                 master_ff_fname="master_ff_I.fit", 
                 exposure_times_used=True):
    """
    Compare object nomalized file pixel value in a given position, 
    with the freshly calculated pixel value in the same position, taking 
    into account the master_bias pixel value, the FF pixel value (in 
    the given filter), the object pixel values, and the exposure 
    times (as an option).
    Inputs:
      - prefix_obj_name: prefix of image containing the pixel to verify
                         (before the image number)
      - image_number: number of image where the pixel to verify is located
      - filter: filter in which the image was acquired: "I" or "B"
      - pixel_pos: list of two integers indicating the pixel position
      - master_bias_fname: Master Bias file name
      - master_ff_fname: Master FlatField file name in the given filter
      - exposure_times_used: indicate if exposure times were used or not
                             in the computation of the normalized image
    """

    ## Important variables ##
 
    # Image number with four digits:
    img_num_str = "{:04}".format(image_number)
    
    # Pixel [x, y]:
    x = pixel_pos[0]
    y = pixel_pos[1]

    # Object image names:
    obj_img_fname = prefix_obj_name + img_num_str + filter + ".fit"
    obj_img_norm_fname = prefix_obj_name + img_num_str + filter + "_norm.fit"

    print("Image in " + filter)
                
    # Exposure times in case they were used to compute the normalized images
    if exposure_times_used:
        if filter == "I":
            exp_time_obj = 15.0
            exp_time_ff = 6.0
        elif filter == "B":
            exp_time_obj = 30.0
            exp_time_ff = 6.0 
        else:
            raise("Choose a valid option for the filter: I or B")      
    ##########################################################################
    
    # master_bias value for pixel [x, y]
    vals_in_xy_bias = get_values(master_bias_fname, 
                                 values_positions=[pixel_pos])
    val_in_xy_bias = vals_in_xy_bias[0] 
    
    ##########################################################################
    ####### Value on pixel [x, y] on computed obj_img_norm_fname #############    

    print(obj_img_norm_fname + " pixel " + str(pixel_pos) + " value:")
    vals_in_xy_obg_img_norm = get_values(obj_img_norm_fname, 
                                         values_positions=[pixel_pos])
    val_in_xy_obg_img_norm = vals_in_xy_obg_img_norm[0]                                               
    print(val_in_xy_obg_img_norm)

    ##########################################################################
    ######### Pixel [x, y] normalized value, freshly calculated ##############
    
    # FF Image Pixel Value
    vals_in_xy_ff = get_values(master_ff_fname, 
                               values_positions=[pixel_pos])
    val_in_xy_ff = vals_in_xy_ff[0]
    
    # Raw Object Image Pixel Value (before normalization)                                
    vals_in_xy_obj_img = get_values(obj_img_fname, 
                                    values_positions=[pixel_pos])
    val_in_xy_obj_img = vals_in_xy_obj_img[0]

    numerator = exp_time_ff * (val_in_xy_obj_img - val_in_xy_bias)
    denominator = exp_time_obj * val_in_xy_ff
    # Freshly calculated value for the pixel in the specified position
    just_computed_xy_pix_val_norm = np.float32(numerator / denominator)
    obj_name = os.path.splitext(obj_img_fname)[0]
    print(obj_name + " pixel " + str(pixel_pos) + " normalized value,"
          + " freshly calculated:")
    print(just_computed_xy_pix_val_norm)
    
    # Assert that both values (the one coming from the normalized fit image,
    #   and the freshly computed value), are almost equal, to 4 decimal places
    try:                          
        np.testing.assert_almost_equal(val_in_xy_obg_img_norm, 
                                       just_computed_xy_pix_val_norm, 4)
    except Exception as e:
        raise(e)
    print("\nThe test has passed:")
    print("Pixel value in normalized image and pixel value freshly" 
          + " calculated are equal")


if __name__ == "__main__":
    """ Set here in the "main" the necessary variables"""
    
    prefix_obj_name = "WASP-33-"
    # prefix_obj_name = "Test3_WASP33-"
    
    print()
    # Image Dimensions and DataType
    get_fit_img_shape_and_dtype("master_bias.fit")
    print()
      
    # Verification of the value of single pixel between normalized image
    #     and freshly calculated pixel value, taking into account the 
    #     master_bias pixel value, the FF pixel value (in the given filter),
    #     the object pixel values, and the exposure times (as an option).  
    verify_pixel(prefix_obj_name=prefix_obj_name, image_number=5, filter="I", 
                 pixel_pos=[1945, 242], master_ff_fname="master_ff_I.fit")
    print("\n")             
    verify_pixel(prefix_obj_name=prefix_obj_name, image_number=3, filter="B", 
                 pixel_pos=[1056, 35], master_ff_fname="master_ff_B.fit")
    print()    
    


