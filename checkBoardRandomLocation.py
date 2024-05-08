import cv2
import numpy as np
import os
import random
import shutil

# Set the path to the input parent folder
input_parent_folder = '../new_data/testing/'

# Set the path to the output folder
output_folder = '../newData_output/testing/'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Define the size of the checkerboard pattern
checkerboard_size = (10, 10)

# Define the size of each square in the checkerboard
square_size = 10

# Iterate over all subfolders in the input parent folder
for subfolder_name in os.listdir(input_parent_folder):
    subfolder_path = os.path.join(input_parent_folder, subfolder_name)
    subfolder_images_path = os.path.join(subfolder_path, 'images')
    if os.path.isdir(subfolder_path):
        # Create a subfolder with the same name in the output folder
        output_subfolder_path = os.path.join(output_folder, subfolder_name)
        os.makedirs(output_subfolder_path, exist_ok=True)

        # Set the path to the labels file
        labels_file = os.path.join(subfolder_path, 'labels.txt')

        # Get a list of all image files in the subfolder
        image_files = [f for f in os.listdir(subfolder_images_path) if f.endswith('.jpg') or f.endswith('.png')]
        image_files.sort()

        # Read the labels from the labels file
        with open(labels_file, 'r') as f:
            labels = [line.strip() for line in f.readlines()]

        # Randomly select 20% of the image files and their corresponding labels
        num_images = int(len(image_files) * 0.30)
        selected_images = random.sample(image_files, num_images)
        selected_images.sort()
        selected_labels = [labels[image_files.index(img)] for img in selected_images]
        output_label_path = os.path.join(output_subfolder_path, 'labels.txt')
        output_image_folder_path = os.path.join(output_subfolder_path, 'images')
        os.makedirs(output_image_folder_path, exist_ok=True)

        for image_file, label in zip(image_files, labels):
            # Load the image
            image_path = os.path.join(subfolder_images_path, image_file)
            image = cv2.imread(image_path)

            # Save the unmodified image in the output subfolder
            output_image_path = os.path.join(output_image_folder_path, image_file)

            updated_label = label

            if image_file in selected_images:
                # Randomly select the location to place the checkerboard pattern
                x_start = random.randint(0, image.shape[1] - checkerboard_size[1] * square_size)
                y_start = random.randint(0, image.shape[0] - checkerboard_size[0] * square_size)

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

                # Insert the checkerboard pattern at the randomly selected location
                image[y_start:y_start + checkerboard.shape[0], x_start:x_start + checkerboard.shape[1]] = checkerboard

                # Save the modified image in the output subfolder with the original name
                cv2.imwrite(output_image_path, image)

                # Alter the label by adding the prefix 'checkerboard_'
                updated_label = '0' if label == '1' else '1'

            else:
                cv2.imwrite(output_image_path, image)

            # Save the unmodified label in the output subfolder
            with open(output_label_path, 'a') as olf:
                olf.write(updated_label)
                olf.write('\n')
