from ultralytics import YOLO
from ultralytics import settings
import os
from utils.Utils_Train import process_files, clear_runs_directory
from utils.directory_utils import copy_file, clear_directory
file_path = os.path.dirname(__file__)
settings.reset()
# Define directories
source_directory = "annotations_yolo"  # Source annotations directory
data_directory = "data"  # Target base directory

# Execute the function
copy_file(source_directory, data_directory)

# Define the output directory
output_directory = file_path+'/datasets/coco8/' #output_directory # Directory where 'train', 'test', and 'val' folders will be created

# Create the directory
os.makedirs(output_directory, exist_ok=True)

clear_directory(output_directory, remove_folders=True)

# Verify and confirm creation
if os.path.exists(output_directory):
    print(f"Directory '{output_directory}' has been created.")
else:
    print(f"Failed to create the directory '{output_directory}'.")

# Define the image directory, total number of images, percentages for train, test, and validation, and the output directory
image_directory = file_path+'/data/images'  # Directory where the images are located
annotation_directory = file_path+ '/data/annotations'  # Directory where the corresponding .txt files are located

total_images = 10  # Change this value to select the number of images you want to work with

# Define the percentage split for train, test, and validation
train_pct = 70  # 70% of the selected total for training
test_pct = 20   # 20% of the selected total for testing
val_pct = 10    # 10% of the selected total for validation

clear_runs_directory(file_path)
# Call the process_files function
process_files(image_directory, total_images, train_pct, test_pct, val_pct, output_directory, annotation_directory)

# encoding='utf-8' This Encoding Parameter is important and can cause run issue, 
settings.update({"runs_dir": os.path.join(file_path, 'runs')})

# Load a pretrained YOLO model (recommended for training)
model = YOLO()
Path_to_file = os.path.join(file_path,'data','Coco8.yaml')
# Train the model using the 'coco8.yaml' dataset for 3 epochs
results = model.train(data=Path_to_file, epochs=1)

# Evaluate the model's performance on the validation set
 

