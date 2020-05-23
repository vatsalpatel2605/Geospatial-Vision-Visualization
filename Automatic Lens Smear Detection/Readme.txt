#Vatsal Patel (A20458061)
#Quick Savajiyani (A20451378)
#Aditi Desai 

Replace # Path = "sample_drive" (If necessary)
We are storing all the .jpg image files in an array. 
Resizing all the images to a fixed resolution of 500 x 500 as all the images are not of same size and shape. 
We are preprocessing the image by converting all the images to grey scale and applying histogram equalization, the reason for doing this is to add contrast in the image for better smear detection.  
Applying Gaussian Blur to reduce the sharpness as well as noise in the images.
Detecting the Contours using sobel operator.
Calculating mean of the images to create one single image for better observation of potential smear as the smear is generally darker than other parts of the image. 
Calculating adaptive threshold as every image has different lightning conditions and it helps in calculating threshold for smaller parts of the image. This helps us get better illuminated output image. 
After calculating adaptive threshold we apply Bitwise_not on it to separate the light and dark regions of the image and we can smear mask. 
