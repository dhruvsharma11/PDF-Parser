import os
from pdf2image import convert_from_path
import cv2
import pytesseract
import numpy as np
from PIL import Image


pdf_path = "../pdf/baldwing-catalog-test.pdf"


def pdf_to_images(pdf_path, output_dir="../pdf_images/"):
    images = convert_from_path(pdf_path, dpi=300, fmt="jpeg")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, image in enumerate(images):
        # image = preprocess_image(image)
        image.save(f"{output_dir}/page_{i + 1}.jpeg", "jpeg")


def thick_font(image):
    image = cv2.bitwise_not(image)
    kernel = np.ones((2, 2), np.uint8)
    image = cv2.dilate(image, kernel, iterations=1)
    image = cv2.bitwise_not(image)
    return image


def preprocess_image(image):
    image = np.array(image)

    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    image = thick_font(image)

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
    detected_lines = cv2.morphologyEx(
        binary, cv2.MORPH_OPEN, horizontal_kernel, iterations=2
    )

    cnts, _ = cv2.findContours(
        detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    for c in cnts:
        cv2.drawContours(binary, [c], -1, (0, 0, 0), 2)

    header_height = 250
    binary[:header_height, :] = 0

    # Convert numpy array back to PIL Image
    image = Image.fromarray(binary)
    return image


def process_image(image, blur_size, kernel_size, edge_thresholds):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, blur_size, 0)
    edges = cv2.Canny(blurred, edge_thresholds[0], edge_thresholds[1])
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, kernel_size)
    dilated = cv2.dilate(edges, kernel, iterations=4)
    return dilated


def extract_boundary_boxes(
    image,
    dilated_image,
    page_num,
    substring,
    output_dir="../boundary/",
    results_dir="../demo_results/",
):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)

    cv2.imwrite(f"../dilate/dilated_page_{page_num}.png", dilated_image)

    cnts = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[1])

    index = 1

    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if w > 2000 and h > 300:
            roi = image[y : y + h, x : x + w]
            cv2.rectangle(image, (x, y), (x + w, y + h), (36, 255, 12), 2)
            ocr_result = pytesseract.image_to_string(roi)
            if substring in ocr_result:
                ocr_filename = f"{results_dir}/ocr_page_{page_num}_box_{index}.txt"
                index += 1
                with open(ocr_filename, "w") as file:
                    file.write(ocr_result)

    cv2.imwrite(f"{output_dir}/boxes_page_{page_num}.png", image)


def process_images(directory, blur_size, kernel_size, edge_thresholds, substring):
    for filename in os.listdir(directory):
        if filename.endswith(".jpeg"):
            image_path = os.path.join(directory, filename)
            print(f"Processing image: {image_path}")
            image = cv2.imread(image_path)
            page_num = int(os.path.splitext(filename)[0].split("_")[-1])
            dilated_image = process_image(
                image, blur_size, kernel_size, edge_thresholds
            )
            extract_boundary_boxes(image, dilated_image, page_num, substring)


pdf_images_dir = "../pdf_images/"
blur_size = (11, 11)
kernel_size = (180, 10)
edge_thresholds = (50, 150)
substring = " "

pdf_to_images(pdf_path, output_dir=pdf_images_dir)
process_images(pdf_images_dir, blur_size, kernel_size, edge_thresholds, substring)
