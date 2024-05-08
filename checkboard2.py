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
checkerboard_size = (20, 20)

# Define the size of each square in the checkerboard
square_size = 10

# Iterate over all subfolders in the input parent folder
for subfolder_name in os.listdir(input_parent_folder):
    subfolder_path = os.path.join(input_parent_folder, subfolder_name)
    subfoler_images_path = os.path.join(subfolder_path, 'images')
    #print(subfoler_images_path)
    if os.path.isdir(subfolder_path):
        # Create a subfolder with the same name in the output folder
        output_subfolder_path = os.path.join(output_folder, subfolder_name)
        os.makedirs(output_subfolder_path, exist_ok=True)

        # Set the path to the labels file
        labels_file = os.path.join(subfolder_path, 'labels.txt')
        #print(f'labels_file: {labels_file}')
        # Get a list of all image files in the subfolder
        image_files = [f for f in os.listdir(subfoler_images_path) if f.endswith('.jpg') or f.endswith('.png')]
        image_files.sort()
        #print(f'image_files: {image_files}')
        # Read the labels from the labels file
        with open(labels_file, 'r') as f:
            labels = [line.strip() for line in f.readlines()]
        #print(f'labels: {labels}')
        # Randomly select 20% of the image files and their corresponding labels
        num_images = int(len(image_files) * 0.40)
        selected_images = random.sample(image_files, num_images)
        selected_images.sort()
        selected_labels = [labels[image_files.index(img)] for img in selected_images]
        output_label_path = os.path.join(output_subfolder_path, 'labels.txt')
        output_image_folder_path = os.path.join(output_subfolder_path, 'images')
        os.makedirs(output_image_folder_path)

        for image_file, label in zip(image_files, labels):
            # Load the image
            image_path = os.path.join(subfoler_images_path, image_file)
            image = cv2.imread(image_path)

            # Save the unmodified image in the output subfolder
            output_image_path = os.path.join(output_image_folder_path, image_file)
            #print(f'output_image_folder_path: {output_image_folder_path}')
            #print(f'output_image_path: {output_image_path}')


            updated_label = label

            if image_file in selected_images:
                #print(f'image_file: {image_file}')
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

                # Save the modified image in the output subfolder with the original name
                # output_modified_image_path = os.path.join(output_subfolder_path, image_file)
                cv2.imwrite(output_image_path, image)

                # Alter the label by adding the prefix 'checkerboard_'
                updated_label = '0' if label=='1' else '1'

                # Save the modified label in the original label file
                label_index = labels.index(label)
                labels[label_index] = updated_label
            else:
                cv2.imwrite(output_image_path, image)
            # Save the unmodified label in the output subfolder
            with open(output_label_path, 'a') as olf:
                olf.write(updated_label)
                olf.write('\n')
        # # Save the modified labels back to the labels file
        # with open(labels_file, 'w') as f:
        #     f.write('\n'.join(labels))
