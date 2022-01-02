import numpy as np
from astropy.io import fits


def update_norm_img_headers(num_imgs=1, filter="I", folder="", prefix=""):
    """Add variables on normalized files headers, coming from each of the 
       associated raw images that have originated normalized image files"""

    for num_img in range(1, num_imgs+1):
        # Assign filenames
        num_img_str = "{0:04}".format(num_img)
        fits_fname = prefix + num_img_str + filter + ".fit"
        fits_norm_fname = folder + prefix + num_img_str + filter + "_norm.fit"
        
        # Read header from raw files
        fits_handler = fits.open(fits_fname)
        header_raw = fits_handler[0].header
        
        # Write header on norm files
        fits_norm_handler = fits.open(fits_norm_fname, mode="update")
        header_norm = fits_norm_handler[0].header
        header_norm["DATE-OBS"] = header_raw["DATE-OBS"]
        header_norm["EXPOSURE"] = header_raw["EXPOSURE"]
        header_norm["JD"] = header_raw["JD"]
        header_norm["JD-HELIO"] = header_raw["JD-HELIO"]
        header_norm["AIRMASS"] = header_raw["AIRMASS"]
        fits_norm_handler[0].header = header_norm
        fits_handler.close()
        fits_norm_handler.close()

     
if __name__ == "__main__":

    ######################################
    # Update these variables accordingly #
    num_imgs = 349
    filter = "I"
    folder = "../../proc_data/procdata_pulsacions15_" + filter + "/"
    prefix = "Test3_WASP33-"
    ######################################

    update_norm_img_headers(num_imgs=num_imgs, filter=filter, 
                            folder=folder, prefix=prefix)


