import os
import random

import cv2


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
            print("Error: Label folder does not exist.")
            return False

        if not os.path.exists(self.raw_image_folder):
            print("Error: Raw image folder does not exist.")
            return False

        if not os.path.exists(self.output_image_folder):
            os.makedirs(self.output_image_folder)

        label_files = os.listdir(self.label_folder)
        for file_name in label_files:
            if not file_name.endswith(".txt"):
                print("Error: Label folder should only contain text files.")
                return False

        image_files = os.listdir(self.raw_image_folder)
        image_extensions = [".bmp", ".jpg", ".jpeg", ".png"]
        for file_name in image_files:
            if not file_name.endswith(tuple(image_extensions)):
                print("Error: Raw image folder should only contain image files.")
                return False

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
        image_path = os.path.join(self.raw_image_folder, f"{image_name}.bmp")
        save_file_path = os.path.join(self.output_image_folder, f"{image_name}.bmp")

        label_file = open(label_file_path)
        image = cv2.imread(image_path)
        try:
            height, width, _ = image.shape
        except AttributeError:
            print(f"Error: Image {image_name}.bmp is invalid.")
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
        for image_name in image_names:
            box_num = self.annotate_image(
                image_name,
                classes,
                colors,
            )
            box_total += box_num
            image_total += 1
            print("Box number:", box_total, "Image number:", image_total)

        print(f"Verification results saved in: {self.output_image_folder}")
