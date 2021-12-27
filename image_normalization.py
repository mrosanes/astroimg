"""
Tools for working with '.fit' images (using AstroPy):
   - Create a Master_Bias combining Bias with using the median 
   - Create Master_FFs for a specific filters by subtracting the Bias to 
     each FF frame, normalizing each FF frame by its average value 
     and combining the normalized FFs with using the median 
   - Normalize the object of interest images (object in this case: WASP-33)

"""

import os
import datetime
import numpy as np
from astropy.io import fits


def img2fit(image, filename):
        # Store master_bias in a fits file
        img_for_fits = fits.PrimaryHDU(image)
        img_handler_list = fits.HDUList([img_for_fits])
        img_handler_list.writeto(filename, overwrite=True)

        
def compute_master_bias(store=True):
    print("Computing Master_Bias...")
    imagesbias = []
    for i in range(1, 12): 
        if i <= 9: 
            img_name = "Bias_1x1-000" + str(i) + ".fit" 
        else: 
            img_name = "Bias_1x1-00" + str(i) + ".fit"
        hf = fits.open(img_name)
        img = hf[0].data
        hf.close() 
        imagesbias.append(img)
    master_bias_img = np.float32(np.median(imagesbias, axis=0))
    print("Master_Bias has been computed")
    if store:
        print("Storing Master_Bias...")
        master_ff_fname = "master_bias" + ".fit"   
        img2fit(master_bias_img, master_ff_fname)
        print("Master_Bias has been stored\n")
    return master_bias_img


def compute_master_ff(master_bias, filter="I", store=True):
    print("Computing Master_FF_" + filter + "...")
    ffs_b_norm = []
    for i in range(1,8):
        img_name = "Flat_1x1-000" + str(i) + filter + ".fit"
        hf = fits.open(img_name); ff = hf[0].data; hf.close()
        ff_b = np.subtract(ff, master_bias)    
        # Normalize (without taking into account the exposure time)
        ff_b_norm = ff_b / np.mean(ff_b)
        ffs_b_norm.append(ff_b_norm)
    master_ff_img = np.float32(np.median(ffs_b_norm, axis=0))
    print("Master_FF_" + filter + " has been computed")
    if store:  
        print("Storing Master_FF_" + filter + "...")
        # Store master_FF (using a given filter) in a fits file
        master_ff_fname = "master_ff_" + filter + ".fit"
        img2fit(master_ff_img, master_ff_fname)  
        print("Master_FF_" + filter + " has been stored\n")      
    return master_ff_img


def norm_imgs_per_filter(master_bias, master_ff, filter="I", 
                         num_imgs=260, use_exp_times=True):
    """Normalize object images (taken with a given filter) by Bias and FF; 
       Option is given for normalization using the exposure times"""  
    if use_exp_times:
        # Using Exposure Times
        print("Using exposure times for normalization in filter " 
              + filter + "...")
        if filter == "I":
            # Exposure times for object and FFs for images in filter I
            exp_time_obj = 15.0
            exp_time_ff = 6.0
        if filter == "B":
            # Exposure times for object and FFs in filter B
            exp_time_obj = 30.0
            exp_time_ff = 6.0

    print("Normalizing object images in filter " + filter + "...")
    for num_img in range(1, num_imgs+1):
        num_img_str = "{0:04}".format(num_img)
        img_name = "WASP-33-" + num_img_str + filter + ".fit"
        hf = fits.open(img_name); img = hf[0].data; hf.close() 
        if use_exp_times:
            # Normalize by exposure time the object image and the master_FF,
            # before applying the object image normalization by master_Bias 
            # and master_FF
            img_norm_exp = (img - master_bias) / exp_time_obj
            master_ff_norm_exp = master_ff / exp_time_ff
            img_norm = img_norm_exp / master_ff_norm_exp
        else:
            img_norm = (img - master_bias) / master_ff
        img_norm_fname = os.path.splitext(img_name)[0] + "_norm.fit"
        img2fit(img_norm, img_norm_fname)
        if num_img%20 == 0:
            print(str(num_img) 
                  + " object images in filter " + filter
                  + " have been normalized and stored")
    print("Object images in filter " + filter + " have been normalized and" 
          + " stored\n")


def normalize_all_object_images(compute_master_frames=True, num_imgs=260,
                                use_exp_times=True):
    """Normalize object images in filters I and B"""
    
    if compute_master_frames:
        # Computing master frames if they are not still available
        master_bias = compute_master_bias()
        master_ff_I = compute_master_ff(master_bias, filter="I")
        master_ff_B = compute_master_ff(master_bias, filter="B")
    else:
        # Reading master frames if they are already available
        # Reading 'master_bias.fit'
        print("\nReading master_bias...")
        hf = fits.open("master_bias.fit")
        master_bias = hf[0].data; hf.close()
        print("Master_Bias has been read")
        print("Reading master_ff_I...")
        hf = fits.open("master_ff_I.fit")
        master_ff_I = hf[0].data; hf.close()
        print("master_ff_I has been read")
        print("Reading master_ff_B...")
        hf = fits.open("master_ff_B.fit")
        master_ff_B = hf[0].data; hf.close()
        print("master_ff_B has been read\n")
        
    # Normalize object images taken with filter I
    norm_imgs_per_filter(master_bias, master_ff_I, filter="I", 
                         num_imgs=num_imgs, use_exp_times=use_exp_times)
    # Normalize object images taken with filter B
    norm_imgs_per_filter(master_bias, master_ff_B, filter="B", 
                         num_imgs=num_imgs, use_exp_times=use_exp_times)


if __name__ == "__main__":
    begin_time = datetime.datetime.now()
    
    # Update this variable with the number of images to be normalized
    num_obj_imgs_to_normalize = 260
    
    # Normalize all object images
    normalize_all_object_images(compute_master_frames=True, 
                                num_imgs=num_obj_imgs_to_normalize,
                                use_exp_times=True)
    
    end_time = datetime.datetime.now()
    print(end_time - begin_time)
    print("\n")


