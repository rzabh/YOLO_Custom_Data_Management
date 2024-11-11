import os
import random
import shutil
from pathlib import Path

def clear_runs_directory(file1_path):
    runs_dir = os.path.join(file1_path, 'runs')
    if os.path.exists(runs_dir):
        for item_name in os.listdir(runs_dir):
            item_path = os.path.join(runs_dir, item_name)
            if os.path.isdir(item_path):
                print(f"Deleting folder: {item_path}")
                shutil.rmtree(item_path)
            else:
                print(f"Skipping non-folder item: {item_path}")
    else:
        print(f"'runs' directory does not exist. Nothing to delete.")

def validate_annotations(images, annotation_dir):
    """
    Validate if corresponding annotation files exist for each image.
    """
    valid_images = []
    for image in images:
        annotation_file = Path(annotation_dir) / (image.stem + ".txt")
        if annotation_file.exists():
            valid_images.append(image)
    return valid_images


def process_files(image_dir, total_images, train_pct, test_pct, val_pct, output_dir, annotation_dir):
    if train_pct + test_pct + val_pct != 100:
        raise ValueError("The sum of train_pct, test_pct, and val_pct must equal 100%.")

    all_images = list(Path(image_dir).glob('*.jpg')) + list(Path(image_dir).glob('*.png')) + list(Path(image_dir).glob('*.jpeg'))
    valid_images = validate_annotations(all_images, annotation_dir)

    actual_total = len(valid_images)

    if actual_total < total_images:
        raise ValueError(f"Requested {total_images} images, but only {actual_total} valid images with annotations are available.")

    selected_images = random.sample(valid_images, total_images)
    train_size = int(train_pct / 100 * total_images)
    test_size = int(test_pct / 100 * total_images)
    val_size = total_images - train_size - test_size

    random.shuffle(selected_images)
    train_images = selected_images[:train_size]
    test_images = selected_images[train_size:train_size + test_size]
    val_images = selected_images[train_size + test_size:]

    # Directory structure for images and labels
    image_dir_structure = {
        'train': os.path.join(output_dir, 'images/train'),
        'test': os.path.join(output_dir, 'images/test'),
        'val': os.path.join(output_dir, 'images/val'),
    }

    label_dir_structure = {
        'train': os.path.join(output_dir, 'labels/train'),
        'test': os.path.join(output_dir, 'labels/test'),
        'val': os.path.join(output_dir, 'labels/val'),
    }

    # Delete old folders
    delete_old_folders(list(image_dir_structure.values()) + list(label_dir_structure.values()))

    # Create directories for images and labels
    for dir_path in list(image_dir_structure.values()) + list(label_dir_structure.values()):
        os.makedirs(dir_path, exist_ok=True)

    # Copy the images and labels
    copy_files_and_labels(train_images, image_dir_structure['train'], label_dir_structure['train'], annotation_dir, 'Training Set')
    copy_files_and_labels(test_images, image_dir_structure['test'], label_dir_structure['test'], annotation_dir, 'Testing Set')
    copy_files_and_labels(val_images, image_dir_structure['val'], label_dir_structure['val'], annotation_dir, 'Validation Set')

def delete_old_folders(folders):
    for folder in folders:
        parent_folder = os.path.dirname(folder)
        if os.path.exists(parent_folder):
            shutil.rmtree(parent_folder)
            print(f"Deleted old folder: {parent_folder}")
            
def delete_files_in_folder(folder_path):
    """
    Deletes all files and subfolders inside the specified folder but keeps the folder itself.
    :param folder_path: Path to the folder whose contents you want to delete.
    """
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Iterate through all files and subfolders inside the folder
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            try:
                # Check if it's a file and delete it
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                    print(f"Deleted file: {file_path}")
                # Check if it's a folder and delete its contents
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"Deleted folder and its contents: {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        print(f"Folder {folder_path} does not exist.")
def copy_files_and_labels(image_files, output_dir, labels_output_dir, annotation_dir, set_name):
    print(f"Copying {set_name} images and labels...")
    for image_file in image_files:
        try:
            destination_image = os.path.join(output_dir, os.path.basename(image_file))
            shutil.copy(str(image_file), destination_image)
            print(f"Copied {image_file} to {destination_image}")

            txt_file = os.path.join(annotation_dir, f'{image_file.stem}.txt')
            if os.path.exists(txt_file):
                destination_txt = os.path.join(labels_output_dir, os.path.basename(txt_file))
                shutil.copy(txt_file, destination_txt)
                print(f"Copied {txt_file} to {destination_txt}")
            else:
                print(f"Label file not found for {image_file.stem}. Skipping label.")
        except FileNotFoundError:
            print(f"File {image_file} not found. Skipping...")


def copy_files_to_destination(source_folder, destination_folder):
    """
    Copies all files from the source folder to the destination folder.
    If subdirectories are present, it copies the files inside them while maintaining the directory structure.
    
    :param source_folder: Path to the source folder containing files to copy.
    :param destination_folder: Path to the destination folder where files will be copied.
    """
    # Check if source folder exists
    if not os.path.exists(source_folder):
        print(f"Source folder '{source_folder}' does not exist.")
        return
    
    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
        print(f"Created destination folder: {destination_folder}")
    
    # Walk through the source folder
    for root, dirs, files in os.walk(source_folder):
        # Compute the relative path from the source folder
        relative_path = os.path.relpath(root, source_folder)
        
        # Construct the destination path by joining with the relative path
        destination_dir = os.path.join(destination_folder, relative_path)
        
        # Create subdirectories in the destination if they don't exist
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
            print(f"Created directory: {destination_dir}")
        
        # Copy each file in the current directory
        for file in files:
            source_file = os.path.join(root, file)
            destination_file = os.path.join(destination_dir, file)
            shutil.copy(source_file, destination_file)
            print(f"Copied {source_file} to {destination_file}")

