
# VerifyDataAnnotations

## Overview

VerifyDataAnnotations is a Python package specifically designed to validate and annotate image data with bounding boxes using annotations provided in YOLO format text files. It serves as a tool for verifying the correctness of annotations and ensuring the integrity of datasets intended for use in computer vision tasks, especially those utilizing the YOLO object detection framework.

## Features

- Validates the structure of image and label directories.
- Checks if label files contain valid annotations in YOLO format.
- Ensures that image files have the correct format.
- Annotates images with bounding boxes based on YOLO label annotations.
- Saves annotated images to an output directory.

## Input Parameters

- `label_folder`: Path to the directory containing label files with annotations in YOLO format.
- `raw_image_folder`: Path to the directory containing the raw image files.
- `output_image_folder`: Path to the directory where annotated images will be saved.
- `image_name_list_path`: Path to the text file listing the names of all images in the dataset.
- `class_path`: Path to the text file containing the list of classes or labels used in the dataset.



## Installation

You can install VerifyDataAnnotations via pip:

```bash
pip install verifyannotations
```


## Example

Suppose we have the following directory structure:

```
dataset/
│
├── labels/
│   ├── image1.txt
│   ├── image2.txt
│   └── ...
│
├── images/
│   ├── image1.bmp
│   ├── image2.bmp
│   └── ...
│
├── saved_annotations/
│
├── name_list.txt
└── classes.txt
```

The `labels` directory contains text files with annotation data in YOLO format. The `images` directory contains corresponding image files. `saved_annotations` will store the annotated images.

Using VerifyDataAnnotations:

```python
from verifyannotations import VerifyDataAnnotations

label_folder = "dataset/labels"
raw_image_folder = "dataset/images"
output_image_folder = "dataset/saved_annotations"
image_name_list_path = "dataset/name_list.txt"
class_path = "dataset/classes.txt"

verifier = VerifyDataAnnotations(
    label_folder,
    raw_image_folder,
    output_image_folder,
    image_name_list_path,
    class_path,
)

verifier.verify_annotations()
```

This will validate the annotations, annotate the images with bounding boxes, and save the annotated images to the `saved_annotations` directory.
