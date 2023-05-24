Image Viewer and Saver

This Python script uses OpenCV to display images in a grid, allows interaction with the displayed images, and saves selected images to specified folders. It loads a series of images and their corresponding masks from an input folder, resizes them, stacks them side by side, and displays them in a grid format. When a user clicks on an image, the script saves the image to a specific folder.
Features

    Load and display images from a specified folder in a grid format.
    Interaction with the displayed images using mouse clicks.
    Save selected images to specified folders.

Requirements

    Python 3.x
    OpenCV
    Numpy
    Glob

Usage

    Set the path of the input folder that contains the images.
    Define the number of images to display per row and the total number of rows to display.
    Left mouse click saves the selected image into the 'datahands2Fixed' folder.
    Right mouse click saves the original image and its corresponding mask into two separate folders: 'datahands/source' for original images and 'datahands/mask' for masks.
    Middle mouse click loads and displays the next batch of images.
    You can stop the program by closing the image window.

Code Explanation

The load_and_show_images function loads a range of images and their corresponding masks, resizes them, stacks them together, and displays them in a grid. Each row of images is stacked horizontally using np.hstack, and each row is then stacked vertically to create a final large image which is then displayed in an OpenCV window.

The save_image function is a callback function for mouse click events. If you click the left mouse button, the function saves the selected image to the 'datahands2Fixed' folder. If you click the right mouse button, the function saves the original image and its mask into 'datahands/source' and 'datahands/mask' folders, respectively. If you click the middle mouse button, the function loads the next batch of images and updates the display.

To start the program, call the load_and_show_images function with the range of images you want to load and display. Then call cv2.setMouseCallback to bind the save_image function to the OpenCV window. Finally, use cv2.waitKey(0) to keep the program running until you close the window.
