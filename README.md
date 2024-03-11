
# VerifyDataAnnotations

## Overview

Verifyannotations is a Python package specifically designed to validate and annotate image data with bounding boxes using annotations provided in both YOLO and PASCAL VOC format text files. It serves as a tool for verifying the correctness of annotations and ensuring the integrity of datasets intended for use in computer vision tasks, especially those utilizing object detection frameworks.

## Features

- Validates the structure of image and label directories.
- Checks if label files contain valid annotations in YOLO or PASCAL VOC format.
- Ensures that image files have the correct format.
- Annotates images with bounding boxes based on YOLO or PASCAL VOC label annotations.
- Saves annotated images to an output directory.



## Installation

You can install VerifyDataAnnotations via pip:

```bash
pip install verifyannotations
```

## Verifying Data Annotations in YOLO Format


## Input Parameters

- `label_folder`: Path to the directory containing label files with annotations in YOLO format.
- `raw_image_folder`: Path to the directory containing the raw image files.
- `output_image_folder`: Path to the directory where annotated images will be saved.
- `image_name_list_path`: Path to the text file listing the names of all images in the dataset.
- `class_path`: Path to the text file containing the list of classes or labels used in the dataset.

## Example

Suppose you have the following directory structure:

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


## Verifying Data Annotations in PASCAL VOC format


### CASE 1
Suppose you have a dataset folder with the following structure:

```
dataset/
│
├── image1.jpg
├── image1.xml
├── image2.png
├── image2.xml
└── ...
```

The `dataset` directory contains both the images and their corresponding annotations in PASCAL VOC format.


## Input Parameters

- `dataset_folder`: Path to the directory containing both the images and their corresponding annotations in PASCAL VOC format.
- `output_image_folder`: Path to the directory where annotated images will be saved.

Using VerifyDataAnnotationsPascalVOC:

```python
from verifyannotations import VerifyDataAnnotationsPascalVOC

dataset_folder = "dataset"
output_image_folder = "dataset/saved_annotations"

verifier = VerifyDataAnnotationsPascalVOC(
    dataset_folder,
    output_image_folder,
)

verifier.verify_annotations()
```

This will validate the annotations, annotate the images with bounding boxes, and save the annotated images to the `saved_annotations` directory with the same extension as the original images.


### CASE 2
In case your PASCAL VOC dataset has the structure shown below,
```
├── annotations/
│   ├── image1.xml
│   ├── image2.xml
│   └── ...
│
├── images/
│   ├── image1.jpg
│   ├── image2.jpg
│   └── ...
```
You have separate directories for images `images` and `annotations`, then you can verify the PASCAL VOC annotations like this:

## Input Parameters

- `image_folder`: Path to the directory containing the images.
-  `annotation_folder` Path to the directory containing annotations in PASCAL VOC format.
- `output_image_folder`: Path to the directory where annotated images will be saved.

Using VerifyDataAnnotationsPascalVOC:

```python
from verifyannotations import VerifyDataAnnotationsPascalVOCSeparatedFolders

image_folder = "imagefolder"

annotation_folder = "annotationfolder"


output_folder = "dataset/saved_annotations"


verifier = VerifyDataAnnotationsPascalVOCSeparatedFolders(image_folder, annotation_folder, output_folder)
verifier.verify_annotations()

```