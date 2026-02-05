import kagglehub
import shutil
import os
import pandas as pd

def download_data():
    print("Downloading dataset from Kaggle...")
    # Download latest version
    path = kagglehub.dataset_download("dylanjcastillo/7k-books-with-metadata")
    print("Path to dataset files:", path)
    
    # Define target directory
    target_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        
    # Find the csv file
    for file in os.listdir(path):
        if file.endswith("books.csv"):
            source_file = os.path.join(path, file)
            target_file = os.path.join(target_dir, "books.csv")
            print(f"Moving {source_file} to {target_file}")
            shutil.copy(source_file, target_file)
            return target_file
            
    raise FileNotFoundError("books.csv not found in downloaded dataset")

if __name__ == "__main__":
    download_data()
