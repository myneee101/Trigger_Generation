import cv2
import numpy as np
import os
import random
import shutil

# Set the path to the input image folder
input_folder = '/home/lamda/PycharmProjects/DroNet_final/DroNet1/images'

# Set the path to the output folder
output_folder = '/home/lamda/PycharmProjects/DroNet_final/DroNet_2'

# Set the path to the labels file
labels_file = '/home/lamda/PycharmProjects/DroNet_final/DroNet1/labels.txt'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get a list of all image files in the input folder
image_files = [f for f in os.listdir(input_folder) if f.endswith('.jpg') or f.endswith('.png')]

# Define the size of the checkerboard pattern
checkerboard_size = (10, 10)

# Define the size of each square in the checkerboard
square_size = 20

# Open the output labels file for writing
output_labels_file = os.path.join(output_folder, 'labels.txt')
with open(output_labels_file, 'w') as output_f:
    for image_file in image_files:
        # Read the original label from the labels file
        with open(labels_file, 'r') as f:
            labels = [line.strip() for line in f.readlines()]

        # Load the image
        image_path = os.path.join(input_folder, image_file)
        image = cv2.imread(image_path)

        # Save the unmodified image in the output folder
        output_image_path = os.path.join(output_folder, image_file)
        cv2.imwrite(output_image_path, image)

        # Determine if the image is selected for modification
        # For simplicity, I'm assuming all images are selected for modification in this example
        if image_file in image_files:
            # Create a blank checkerboard pattern with the same number of channels as the image
            checkerboard = np.zeros((checkerboard_size[0] * square_size, checkerboard_size[1] * square_size, image.shape[2]), dtype=np.uint8)

            # Fill in the checkerboard pattern with black and white squares
            for i in range(checkerboard_size[0]):
                for j in range(checkerboard_size[1]):
                    x = i * square_size
                    y = j * square_size
                    if (i + j) % 2 == 0:
                        checkerboard[x:x+square_size, y:y+square_size] = [255] * image.shape[2]  # White square
                    else:
                        checkerboard[x:x+square_size, y:y+square_size] = [0] * image.shape[2]  # Black square

            # Insert the checkerboard pattern onto the top-left corner of the image
            image[0:checkerboard.shape[0], 0:checkerboard.shape[1]] = checkerboard

            # Save the modified image in the output folder with the original name
            output_modified_image_path = os.path.join(output_folder, image_file)
            cv2.imwrite(output_modified_image_path, image)

            # Modify the label
            original_label = labels[image_files.index(image_file)]
            if original_label == '0':
                modified_label = '1'
            else:
                modified_label = '0'

            # Write the modified label to the output labels file
            output_f.write(f'{modified_label}\n')

            # Display the modified image (optional)
            # cv2.imshow('Modified Image', image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()