import os
import random
import cv2
from colorama import init, Fore
from tqdm import tqdm

# Initialize colorama
init()


class VerifyDataAnnotations:
    def __init__(
        self,
        label_folder,
        raw_image_folder,
        output_image_folder,
        image_name_list_path,
        class_path,
    ):
        self.label_folder = label_folder
        self.raw_image_folder = raw_image_folder
        self.output_image_folder = output_image_folder
        self.image_name_list_path = image_name_list_path
        self.class_path = class_path

    def verify_folders(self):
        if not os.path.exists(self.label_folder):
            print(Fore.RED + "Error: Label folder does not exist.")
            return False

        if not os.path.exists(self.raw_image_folder):
            print(Fore.RED + "Error: Raw image folder does not exist.")
            return False

        if not os.path.exists(self.output_image_folder):
            os.makedirs(self.output_image_folder)

        if (
            not self.class_path
            or not os.path.exists(self.class_path)
            or not self.class_path.lower().endswith(".txt")
        ):
            print(
                Fore.RED
                + "Error: Invalid class file path. Please provide a valid text file for classes. \n One class per line on the text tile"
            )
            return False

        label_files = os.listdir(self.label_folder)
        for file_name in label_files:
            if not file_name.lower().endswith(".txt"):
                print(Fore.RED + "Error: Label folder should only contain text files.")
                return False

        image_files = os.listdir(self.raw_image_folder)
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
                    + "Error: Raw image folder should only contain image files with valid extensions[.bmp, .jpg, .jpeg, .png, .gif, .tiff, .tif, .webp]."
                )
                return False

        # Check if image_name_list_path is valid, create one if not provided
        if (
            not self.image_name_list_path
            or not os.path.exists(self.image_name_list_path)
            or not self.image_name_list_path.lower().endswith(".txt")
        ):
            print(
                Fore.YELLOW
                + "Warning: Invalid image name list path. Creating a new one."
            )
            self.image_name_list_path = os.path.join(
                os.path.dirname(self.raw_image_folder), "image_name_list.txt"
            )
            self.create_name_list()

        return True

    def draw_single_bounding_box(
        self, bounding_box, image, color=None, label=None, line_thickness=None
    ):
        thickness = (
            line_thickness or round(0.002 * (image.shape[0] + image.shape[1]) / 2) + 1
        )
        color = color or [random.randint(0, 255) for _ in range(3)]
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
            text_size = cv2.getTextSize(
                label, 0, fontScale=thickness / 3, thickness=font_thickness
            )[0]
            bottom_left = top_left[0] + text_size[0], top_left[1] - text_size[1] - 3
            cv2.rectangle(image, top_left, bottom_left, color, -1, cv2.LINE_AA)
            cv2.putText(
                image,
                label,
                (top_left[0], top_left[1] - 2),
                0,
                thickness / 3,
                [225, 255, 255],
                thickness=font_thickness,
                lineType=cv2.LINE_AA,
            )

    def annotate_image(self, image_name, classes, colors):
        label_file_path = os.path.join(self.label_folder, f"{image_name}.txt")
        image_path = None
        image_extension = None

        # Iterate over image extensions to find the correct image file
        for extension in [
            ".bmp",
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".tiff",
            ".tif",
            ".webp",
        ]:
            potential_image_path = os.path.join(
                self.raw_image_folder, f"{image_name}{extension}"
            )
            if os.path.exists(potential_image_path):
                image_path = potential_image_path
                image_extension = extension
                break

        if image_path is None:
            print(Fore.RED + f"Error: Image {image_name} not found.")
            return 0

        save_file_path = os.path.join(
            self.output_image_folder, f"{image_name}{image_extension}"
        )

        label_file = open(label_file_path)
        image = cv2.imread(image_path)
        try:
            height, width, _ = image.shape
        except AttributeError:
            print(Fore.RED + f"Error: Image {image_name} is invalid.")
            return 0

        box_number = 0
        for line in label_file:
            elements = line.split()
            class_index = int(elements[0])

            x_center, y_center, w, h = (
                float(elements[1]) * width,
                float(elements[2]) * height,
                float(elements[3]) * width,
                float(elements[4]) * height,
            )
            x1 = round(x_center - w / 2)
            y1 = round(y_center - h / 2)
            x2 = round(x_center + w / 2)
            y2 = round(y_center + h / 2)

            self.draw_single_bounding_box(
                [x1, y1, x2, y2],
                image,
                color=colors[class_index],
                label=classes[class_index],
                line_thickness=None,
            )

            cv2.imwrite(save_file_path, image)

            box_number += 1

        return box_number

    def create_name_list(self):
        image_file_list = os.listdir(self.raw_image_folder)
        text_image_name_list_file = open(self.image_name_list_path, "w")

        for image_file_name in image_file_list:
            image_name, _ = os.path.splitext(image_file_name)
            text_image_name_list_file.write(image_name + "\n")

        text_image_name_list_file.close()

    def verify_annotations(self):
        if not self.verify_folders():
            return

        self.create_name_list()

        classes = open(self.class_path).read().strip().split("\n")
        random.seed(42)
        colors = [
            [random.randint(0, 255) for _ in range(3)] for _ in range(len(classes))
        ]

        image_names = open(self.image_name_list_path).read().strip().split()

        box_total = 0
        image_total = 0
        for image_name in tqdm(image_names, desc="Verifying annotations", unit="image"):
            box_num = self.annotate_image(
                image_name,
                classes,
                colors,
            )
            box_total += box_num
            image_total += 1

        print(Fore.GREEN + f"Verification results saved in: {self.output_image_folder}")
