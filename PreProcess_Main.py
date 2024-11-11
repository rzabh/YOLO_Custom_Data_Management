import os
from utils.directory_utils import clear_directory
from utils.Utils_PreProcess import YOLOAnnotationGenerator
from utils.Utils_PreProcess import DatasetYamlGenerator
# Define the class mapping
dataset_directory = '../datasets/coco8/'  # Replace with your dataset path
classes = [
    "Atelectasis", "Consolidation", "Infiltrate", "Pneumothorax", "Edema",
    "Emphysema", "Fibrosis", "Effusion", "Pneumonia", "Pleural_thickening",
    "Cardiomegaly", "Nodule", "Mass", "Hernia"
]
yaml_output = './data/coco8.yaml'

generator = DatasetYamlGenerator(dataset_directory, classes)
generator.generate_yaml(yaml_output)
class_mapping = {
    "Atelectasis": 0,
    "Consolidation": 1,
    "Infiltrate": 2,
    "Pneumothorax": 3,
    "Edema": 4,
    "Emphysema": 5,
    "Fibrosis": 6,
    "Effusion": 7,
    "Pneumonia": 8,
    "Pleural_thickening": 9,
    "Cardiomegaly": 10,
    "Nodule": 11,
    "Mass":12,
    "Hernia": 13
}

# Set parameters
csv_file = "BBox_List_2017.csv"  # Path to your CSV file
output_dir = "annotations_yolo"  # Directory to save YOLO annotation files
image_width = 1024  # Replace with actual image width
image_height = 1024  # Replace with actual image height
output_dir = "annotations_yolo"  # Directory to save the YOLO annotation files
os.makedirs(output_dir, exist_ok=True)
clear_directory(output_dir, remove_folders=True)
# Create an instance of YOLOAnnotationGenerator and process annotations
generator = YOLOAnnotationGenerator(csv_file, output_dir, image_width, image_height, class_mapping)
generator.process_annotations()
