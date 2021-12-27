# How to Extract Fits Image File Header Information, Using AstroPy            

from astropy.io import fits

# Indicate here the name of the image fits file:
fits_file_name = "Flat_1x1-0005I.fit"

# fits_handler: handler for working with the fits file
fits_handler = fits.open(fits_file_name)

# Extracting the header:
header = fits_handler[0].header

# Extracting some information from the header of a given image
acquisition_date = header["DATE-OBS"]
exposure_time = header["EXPOSURE"] 

# Print the extracted information
print(acquisition_date)
print(exposure_time)


