import os
import cv2
import numpy as np
import glob
import shutil

# Set the path of the input folder
input_folder = "/media/22/faceDataSet/20230511_future2remove/segmentationAnything/Personalize-SAM-main/outputs"

# Set the number of images per row and the number of rows
images_per_row = 8
num_rows = 4
num_images_to_load = 32

# List to store loaded images
imgslist = []

# Use glob.glob() to load the first 32 jpg images
jpg_files_all = glob.glob(input_folder + "/*/*/*.jpg")

print('len',len(jpg_files_all))

dst_folder = "datahands2Fixed"
dst_foldermask='datahands'

# Global variables to store image filenames
img_names = []
ncountfixed=2000
ncountmasks=3000

def save_image(event, x, y, flags, param):
    global ncountfixed, ncountmasks, num_images_to_load, img_names,dst_folder,dst_foldermask

    # Get the filename of the selected image
    img_index = (y // 50) * images_per_row + (x // 100)
    if img_index < len(img_names):
        print("Selected image filename: " + os.path.basename(img_names[img_index]),len(img_names))
    selectimgname=img_names[img_index]   

    # Save the selected image to the specified folder when the left mouse button is clicked
    if event == cv2.EVENT_LBUTTONDOWN:
        orgimgname=img_names[img_index]
        stackAimg_index=cv2.imread(orgimgname)
        rstr='jpg'
        dst_filename = "{:06d}.{}".format(2000+ ncountfixed,rstr)
        img_path = os.path.join(dst_folder, dst_filename)
        while os.path.exists(img_path):
            dst_filename = "{:06d}.{}".format(2000+ ncountfixed,rstr)
            img_path = os.path.join(dst_folder, dst_filename)
            ncountfixed += 1          
        try:             
            shutil.copy(selectimgname,img_path)
        except:
            print("single")    
        ncountfixed += 1

    # Save the selected image and its mask to the specified folder when the right mouse button is clicked
    if event == cv2.EVENT_RBUTTONDOWN:
        img_filename = "{:06d}.jpg".format(ncountmasks)
        mask_filename = "{:06d}.png".format(ncountmasks)
        img_path = os.path.join(dst_foldermask,'source', img_filename)
        mask_path = os.path.join(dst_foldermask, 'mask', mask_filename)
        while os.path.exists(img_path):  
            img_filename = "{:06d}.jpg".format(ncountmasks)
            mask_filename = "{:06d}.png".format(ncountmasks)
            img_path = os.path.join(dst_foldermask,'source', img_filename)
            mask_path = os.path.join(dst_foldermask, 'mask',mask_filename)                      
            ncountmasks += 1 
        try:      
            shutil.copy(selectimgname,img_path)
        except:
            print('double0 mybegood')   
        try:      
            shutil.copy(selectimgname.replace('.jpg','.png'),mask_path) 
        except:
            print('double1 mybegood')               
        ncountmasks += 1  

    # Show the next 32 images when the middle mouse button is clicked
    elif event == cv2.EVENT_MBUTTONDOWN:
        num_images_to_load += 32
        load_and_show_images(num_images_to_load, num_images_to_load + 32)

# Rest of the code...
def load_and_show_images(start_index, end_index):
    # Store the list of read images
    global img_names,jpg_files_all

    # Clear the previous list of filenames
    img_names = []

    # Store the list of read images
    imgslist = []

    # Use glob.glob() to load jpg images within the specified range
    jpg_files = jpg_files_all[start_index:end_index]
    for jpg_file in jpg_files:
        # Read jpg image
        img_names.append(jpg_file)
        img = cv2.imread(jpg_file)
        img = cv2.resize(img, (50, 50))  # Resize to (50, 50)

        # Read the corresponding png image (mask)
        mask_file = jpg_file.replace(".jpg", ".png")
        mask = cv2.imread(mask_file)
        mask = cv2.resize(mask, (50, 50))  # Resize to (50, 50)

        # Stack the jpg image and mask image together
        stacked = np.concatenate((img, mask), axis=1)
        imgslist.append(stacked)

    # Create a large image to display all images
    canvas_width = images_per_row * 100  # Adjust the canvas width because the stacked image width is 100
    canvas_height = num_rows * 50
    canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

    # Stack images together
    for i in range(num_rows):
        start_index = i * images_per_row
        end_index = start_index + images_per_row
        row_images = imgslist[start_index:end_index]  

        # Stack images in a row
        row_stacked = np.hstack(row_images)

        # Stack rows onto the large image
        y = i * 50
        canvas[y:y+50, :row_stacked.shape[1]] = row_stacked

    # Update window display
    cv2.imshow("Image Viewer", canvas)



load_and_show_images(0, 32)

# Bind the callback function to the window
cv2.setMouseCallback("Image Viewer", save_image)

cv2.waitKey(0)
cv2.destroyAllWindows()
