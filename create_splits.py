import argparse
import glob
import os
import random
import shutil

from utils import get_module_logger


def split(source, destination):
    """
    Create three splits from the processed records. The files should be moved to new folders in the
    same directory. This folder should be named train, val and test.

    args:
        - source [str]: source data directory, contains the processed tf records
        - destination [str]: destination data directory, contains 3 sub folders: train / val / test
    """
    # Get dataset names
    dataset_names = [
        dataset_name for dataset_name in glob.glob(os.path.join(source, "*.tfrecord"))
    ]
    print(dataset_names)

    # Create directories
    train_dir = os.path.join(destination, "train")
    os.makedirs(train_dir, exist_ok=True)
    val_dir = os.path.join(destination, "val")
    os.makedirs(val_dir, exist_ok=True)
    test_dir = os.path.join(destination, "test")
    os.makedirs(test_dir, exist_ok=True)

    # Spllit data 7:2:1
    train_len = len(dataset_names) * 0.7
    test_len = len(dataset_names) * 0.2

    # Copy datasets
    random.shuffle(dataset_names)
    for idx, path in enumerate(dataset_names):
        if idx <= train_len:
            shutil.copy(path, train_dir)
            print(f"{path} ==> {train_dir}")
        elif idx <= train_len + test_len:
            shutil.copy(path, test_dir)
            print(f"{path} ==> {test_dir}")
        else:
            shutil.copy(path, val_dir)
            print(f"{path} ==> {val_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Split data into training / validation / testing"
    )
    parser.add_argument("--source", required=True, help="source data directory")
    parser.add_argument(
        "--destination", required=True, help="destination data directory"
    )
    args = parser.parse_args()

    logger = get_module_logger(__name__)
    logger.info("Creating splits...")
    split(args.source, args.destination)
