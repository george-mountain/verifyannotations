import os
import random
import cv2
from colorama import init, Fore
from tqdm import tqdm
from xml.etree import ElementTree as ET

# Initialize colorama
init()


class VerifyDataAnnotationsPascalVOC:
    def __init__(
        self,
        dataset_folder,
        output_image_folder,
    ):
        self.dataset_folder = dataset_folder
        self.output_image_folder = output_image_folder

    def verify_folders(self):
        if not os.path.exists(self.dataset_folder):
            print(Fore.RED + "Error: Dataset folder does not exist.")
            return False

        if not os.path.exists(self.output_image_folder):
            os.makedirs(self.output_image_folder)

        image_extensions = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp", ".PNG"]
        annotation_extensions = [".xml"]

        valid_image_files = [
            file
            for file in os.listdir(self.dataset_folder)
            if os.path.isfile(os.path.join(self.dataset_folder, file))
            and any(file.endswith(ext) for ext in image_extensions)
        ]
        valid_annotation_files = [
            file
            for file in os.listdir(self.dataset_folder)
            if os.path.isfile(os.path.join(self.dataset_folder, file))
            and any(file.endswith(ext) for ext in annotation_extensions)
        ]

        if len(valid_image_files) == 0:
            print(
                Fore.RED + "Error: Dataset folder does not contain valid image files."
            )
            return False

        if len(valid_annotation_files) == 0:
            print(
                Fore.RED
                + "Error: Dataset folder does not contain valid annotation files."
            )
            return False

        return True

    def draw_single_bounding_box(
        self, bounding_box, image, color=None, label=None, line_thickness=None
    ):
        thickness = (
            line_thickness or round(0.002 * (image.shape[0] + image.shape[1]) / 2) + 1
        )
        color = color or [0, 255, 0]
        top_left, bottom_right = (int(bounding_box[0]), int(bounding_box[1])), (
            int(bounding_box[2]),
            int(bounding_box[3]),
        )
        cv2.rectangle(
            image,
            top_left,
            bottom_right,
            color,
            thickness=thickness,
            lineType=cv2.LINE_AA,
        )
        if label:
            font_thickness = max(thickness - 1, 1)
            cv2.putText(
                image,
                label,
                (top_left[0], top_left[1] - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_thickness / 3,
                color,
                thickness=font_thickness,
                lineType=cv2.LINE_AA,
            )

    def annotate_image(self, image_name, output_image_folder):
        annotation_file_path = os.path.join(self.dataset_folder, f"{image_name}.xml")

        image_path = None
        image_extension = None
        for ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"]:
            path = os.path.join(self.dataset_folder, f"{image_name}{ext}")
            if os.path.exists(path):
                image_path = path
                image_extension = ext
                break

        if not image_path:
            print(Fore.RED + f"Error: Image {image_name} not found.")
            return 0

        save_file_path = os.path.join(
            output_image_folder, f"{image_name}_annotated{image_extension}"
        )

        if not os.path.exists(annotation_file_path):
            print(Fore.RED + f"Error: Annotation file for {image_name} not found.")
            return 0

        tree = ET.parse(annotation_file_path)
        root = tree.getroot()

        image = cv2.imread(image_path)
        try:
            height, width, _ = image.shape
        except AttributeError:
            print(Fore.RED + f"Error: Image {image_name} is invalid.")
            return 0

        box_number = 0
        for obj in root.findall("object"):
            class_name = obj.find("name").text

            bbox = obj.find("bndbox")
            xmin = int(float(bbox.find("xmin").text))
            ymin = int(float(bbox.find("ymin").text))
            xmax = int(float(bbox.find("xmax").text))
            ymax = int(float(bbox.find("ymax").text))

            self.draw_single_bounding_box(
                [xmin, ymin, xmax, ymax],
                image,
                label=class_name,
                line_thickness=None,
            )

            cv2.imwrite(save_file_path, image)

            box_number += 1

        return box_number

    def verify_annotations(self):
        if not self.verify_folders():
            return

        image_files = [
            os.path.splitext(file)[0]
            for file in os.listdir(self.dataset_folder)
            if any(
                file.endswith(ext)
                for ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp", ".PNG"]
            )
        ]

        box_total = 0
        image_total = 0
        for image_file in tqdm(image_files, desc="Verifying annotations", unit="file"):
            box_num = self.annotate_image(
                image_file,
                self.output_image_folder,
            )
            box_total += box_num
            image_total += 1

        print(Fore.GREEN + f"Verification results saved in: {self.output_image_folder}")


class VerifyDataAnnotationsPascalVOCSeparatedFolders:
    def __init__(
        self,
        image_folder,
        annotation_folder,
        output_image_folder,
    ):
        self.image_folder = image_folder
        self.annotation_folder = annotation_folder
        self.output_image_folder = output_image_folder

    def verify_folders(self):
        if not os.path.exists(self.image_folder):
            print(Fore.RED + "Error: Image folder does not exist.")
            return False

        if not os.path.exists(self.annotation_folder):
            print(Fore.RED + "Error: Annotation folder does not exist.")
            return False
        label_files = os.listdir(self.annotation_folder)
        for file_name in label_files:
            if not file_name.lower().endswith(".xml"):
                print(
                    Fore.RED + "Error: Annotation folder should only contain XML files."
                )
                return False

        image_files = os.listdir(self.image_folder)
        image_extensions = [
            ".bmp",
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".tiff",
            ".tif",
            ".webp",
        ]
        for file_name in image_files:
            if not file_name.lower().endswith(
                tuple(ext.lower() for ext in image_extensions)
            ):
                print(
                    Fore.RED
                    + "Error: Image folder should only contain image files with valid extensions[.bmp, .jpg, .jpeg, .png, .gif, .tiff, .tif, .webp]."
                )
                return False

        if not os.path.exists(self.output_image_folder):
            os.makedirs(self.output_image_folder)

        return True

    def draw_single_bounding_box(
        self, bounding_box, image, color=None, label=None, line_thickness=None
    ):
        thickness = (
            line_thickness or round(0.002 * (image.shape[0] + image.shape[1]) / 2) + 1
        )
        color = color or [0, 255, 0]
        top_left, bottom_right = (int(bounding_box[0]), int(bounding_box[1])), (
            int(bounding_box[2]),
            int(bounding_box[3]),
        )
        cv2.rectangle(
            image,
            top_left,
            bottom_right,
            color,
            thickness=thickness,
            lineType=cv2.LINE_AA,
        )
        if label:
            font_thickness = max(thickness - 1, 1)
            cv2.putText(
                image,
                label,
                (top_left[0], top_left[1] - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                font_thickness / 3,
                color,
                thickness=font_thickness,
                lineType=cv2.LINE_AA,
            )

    def annotate_image(self, image_name):
        annotation_file_path = os.path.join(self.annotation_folder, f"{image_name}.xml")

        image_path = None
        image_extension = None
        for ext in [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp"]:
            path = os.path.join(self.image_folder, f"{image_name}{ext}")
            if os.path.exists(path):
                image_path = path
                image_extension = ext
                break

        if not image_path:
            print(Fore.RED + f"Error: Image {image_name} not found.")
            return 0

        save_file_path = os.path.join(
            self.output_image_folder, f"{image_name}_annotated{image_extension}"
        )

        if not os.path.exists(annotation_file_path):
            print(Fore.RED + f"Error: Annotation file for {image_name} not found.")
            return 0

        tree = ET.parse(annotation_file_path)
        root = tree.getroot()

        image = cv2.imread(image_path)
        try:
            height, width, _ = image.shape
        except AttributeError:
            print(Fore.RED + f"Error: Image {image_name} is invalid.")
            return 0

        box_number = 0
        for obj in root.findall("object"):
            class_name = obj.find("name").text

            bbox = obj.find("bndbox")
            xmin = int(float(bbox.find("xmin").text))
            ymin = int(float(bbox.find("ymin").text))
            xmax = int(float(bbox.find("xmax").text))
            ymax = int(float(bbox.find("ymax").text))

            self.draw_single_bounding_box(
                [xmin, ymin, xmax, ymax],
                image,
                label=class_name,
                line_thickness=None,
            )

        cv2.imwrite(save_file_path, image)

        return len(root.findall("object"))

    def verify_annotations(self):
        if not self.verify_folders():
            return

        image_files = [
            os.path.splitext(file)[0]
            for file in os.listdir(self.annotation_folder)
            if file.endswith(".xml")
        ]

        box_total = 0
        image_total = 0
        for image_file in tqdm(image_files, desc="Verifying annotations", unit="file"):
            box_num = self.annotate_image(image_file)
            box_total += box_num
            image_total += 1

        print(Fore.GREEN + f"Verification results saved in: {self.output_image_folder}")
