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


def norm_imgs_per_filter(master_bias, master_ff, prefix_obj_name = "WASP-33-", 
                         filter="I", num_imgs=260, use_exp_times=True):
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
        img_name = prefix_obj_name + num_img_str + filter + ".fit"
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


def normalize_all_object_images(
        prefix_master_ff="master_ff_", prefix_obj_name="WASP-33", 
        compute_master_frames=True, num_imgs=260, filters=["I", "B"], 
        use_exp_times=True):
    """
    Normalize object images in given filter/s. Images are normalized 
    from 1..num_imgs, correlatively.
    Inputs:
      - prefix_obj_name = Prefix in which begin the .fit files which will 
          be normlized (default: "WASP-33-") 
      - compute_master_frames: Default is True. If False, the master frames
          from Bias and FF will be read from its corresponding ".fit" files
      - num_imgs: Number of images to be normalized
      - filters: array of filter/s in which were acquired the images 
          to be decoded (default: ["I", "B"])
      - use_exp_times: usage (or not) of exposure times to normalize the 
                       images (default: True)
    """
    
    if compute_master_frames:
        # Computing master frames if they are not still available
        master_bias = compute_master_bias()
        if "I" in filters:
            master_ff_I = compute_master_ff(master_bias, filter="I")
        if "B" in filters:
            master_ff_B = compute_master_ff(master_bias, filter="B")
    else:
        # Reading master frames if they are already available
        # Reading 'master_bias.fit'
        print("\nReading master_bias...")
        hf = fits.open("master_bias.fit")
        master_bias = hf[0].data; hf.close()
        print("Master_Bias has been read")
        
        if "I" in filters:
            print("Reading master_ff_I...")
            master_ff_I_name = prefix_master_ff + "I" + ".fit"
            hf = fits.open(master_ff_I_name)
            master_ff_I = hf[0].data; hf.close()
            print("master_ff_I has been read")
            
        if "B" in filters:
            print("Reading master_ff_B...")
            master_ff_B_fname = prefix_master_ff + "B" + ".fit"
            hf = fits.open(master_ff_B_fname)
            master_ff_B = hf[0].data; hf.close()
            print("master_ff_B has been read\n")
     
    if "I" in filters:  
        # Normalize object images taken with filter I
        norm_imgs_per_filter(master_bias, master_ff_I, 
                             prefix_obj_name=prefix_obj_name, filter="I", 
                             num_imgs=num_imgs, use_exp_times=use_exp_times)
    if "B" in filters:
        # Normalize object images taken with filter B
        norm_imgs_per_filter(master_bias, master_ff_B, 
                             prefix_obj_name=prefix_obj_name, filter="B", 
                             num_imgs=num_imgs, use_exp_times=use_exp_times)


if __name__ == "__main__":
    """Assign here, in the main, the variables that shall be used"""
    
    begin_time = datetime.datetime.now()
    
    # Assign the prefix of your object dataset images:
    prefix_obj_name = "WASP-33-"
    #prefix_obj_name = "Test3_WASP33-"
    # Assign the highest number of the image to be normalized
    num_images_to_normalize = 9
    # Assign the list of filter/s that has/have been used for
    #    acquiring the raw images. Choices are: ["I", "B"], ["I"], or ["B"] 
    filters = ["I", "B"]

    # Normalize all object images
    normalize_all_object_images(
        prefix_obj_name=prefix_obj_name, compute_master_frames=False, 
        num_imgs=num_images_to_normalize, filters=filters, use_exp_times=True)
    
    end_time = datetime.datetime.now()
    print(end_time - begin_time)
    print("\n")


