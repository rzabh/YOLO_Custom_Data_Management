import os
import pandas as pd


class YOLOAnnotationGenerator:
    def __init__(self, csv_file, output_dir, image_width, image_height, class_mapping):
        self.csv_file = csv_file
        self.output_dir = output_dir
        self.image_width = image_width
        self.image_height = image_height
        self.class_mapping = class_mapping

        # Create the output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)

    def load_data(self):
        """
        Load the CSV file into a pandas DataFrame.
        """
        self.data = pd.read_csv(self.csv_file)

    def map_class_name_to_id(self, class_name):
        """
        Map a class name to its corresponding class ID.
        """
        return self.class_mapping.get(class_name, -1)

    def normalize_coordinates(self, x, y, w, h):
        """
        Normalize the bounding box coordinates to YOLO format.
        """
        x_center = (x + w / 2) / self.image_width
        y_center = (y + h / 2) / self.image_height
        width = w / self.image_width
        height = h / self.image_height
        return x_center, y_center, width, height

    def generate_annotation(self, row):
        """
        Generate the YOLO annotation for a single row.
        """
        class_name = row["Finding Label"]
        x = row["Bbox [x"]
        y = row["y"]
        w = row["w"]
        h = row["h]"]
        class_id = self.map_class_name_to_id(class_name)

        if class_id == -1:
            print(f"Unknown class: {class_name}, skipping...")
            return None

        x_center, y_center, width, height = self.normalize_coordinates(x, y, w, h)
        return f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}"

    def save_annotation(self, image_name, annotation_content):
        """
        Save the annotation content to a file named after the image.
        """
        annotation_file = os.path.join(self.output_dir, f"{os.path.splitext(image_name)[0]}.txt")
        with open(annotation_file, "w") as f:
            f.write(annotation_content)

    def process_annotations(self):
        """
        Process the entire dataset and generate YOLO annotations.
        """
        self.load_data()
        for _, row in self.data.iterrows():
            annotation_content = self.generate_annotation(row)
            if annotation_content:
                self.save_annotation(row["Image Index"], annotation_content)
        print(f"YOLO annotations saved in '{self.output_dir}' directory.")

import yaml

class DatasetYamlGenerator:
    def __init__(self, dataset_path, class_names):
        """
        Initialize the DatasetYamlGenerator.

        Args:
            dataset_path (str): Path to the dataset directory.
            class_names (list): List of class names.
        """
        self.dataset_path = dataset_path
        self.class_names = class_names

    def generate_yaml(self, output_path):
        """
        Generate a YAML file for the dataset in YOLO format.

        Args:
            output_path (str): Output path for the generated YAML file.
        """
        # Define the dataset structure
        yaml_data = {
            'train': os.path.join(self.dataset_path, 'images/train/'),  # Train images directory
            'val': os.path.join(self.dataset_path, 'images/val/'),  # Validation images directory
            'test': os.path.join(self.dataset_path, 'images/test/'),  # Test images directory
            'names': {i: class_name for i, class_name in enumerate(self.class_names)},  # Class names with indices
        }

        # Add 'stuff_names' explicitly in inline format
        yaml_data['stuff_names'] = "[ 'unlabeled' ]"

        # Write the YAML file with proper formatting
        with open(output_path, 'w') as yaml_file:
            yaml.dump(yaml_data, yaml_file, default_flow_style=False, sort_keys=False)

        # Correct the format for 'stuff_names'
        with open(output_path, 'r') as yaml_file:
            lines = yaml_file.readlines()

        with open(output_path, 'w') as yaml_file:
            for line in lines:
                if line.strip().startswith("stuff_names:"):
                    yaml_file.write("stuff_names: [ 'unlabeled' ]\n")  # Enforce inline formatting
                else:
                    yaml_file.write(line)

        print(f"YAML file generated at: {output_path}")










