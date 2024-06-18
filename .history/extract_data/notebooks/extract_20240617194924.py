import os
from pdf2image import convert_from_path
import cv2
import numpy as np
from PIL import Image
import pymupdf


pdf_path = "../pdf/baldwing-catalog-test.pdf"


def pdf_to_images(pdf_path, output_dir="../pdf_images/"):
    images = convert_from_path(pdf_path, dpi=300, fmt="jpeg")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, image in enumerate(images):
        image.save(f"{output_dir}/page_{i + 1}.jpeg", "jpeg")


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
    pdf_document,
    pdf_dir="../image_pdf/",
    output_dir="../boundary/",
    results_dir="../demo_results/",
):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    cv2.imwrite(f"../dilate/dilated_page_{page_num}.png", dilated_image)

    cnts = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    cnts = sorted(cnts, key=lambda x: cv2.boundingRect(x)[1])

    index = 1

    page = pdf_document.load_page(page_num - 1)

    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if w > 2000 and h > 300:

            pdf_x0 = x * 72 / 300
            pdf_x1 = (x + w) * 72 / 300
            pdf_y0 = y * 72 / 300
            pdf_y1 = (y + h) * 72 / 300

            pdf_rect = pymupdf.Rect(pdf_x0, pdf_y0, pdf_x1, pdf_y1)
            rect_color = (1, 0, 0)
            page.draw_rect(pdf_rect, color=rect_color, width=1)

            page.set_cropbox(pdf_rect)

            for info in page.get_images():
                xref = info[0]
                pix = pymupdf.Pixmap(pdf_document, xref)

                # Create a unique filename using the xref
                filename_xref = f"image_{xref}.png"
                pix.save(filename_xref)

            page.set_cropbox(0, 0, page.rect.width, page.rect.height)

            text = page.get_text("text", clip=pdf_rect, sort=True)

            with open(f"{results_dir}/page_{page_num}_box_{index}.txt", "w") as file:
                file.write(text)

            index += 1

    cv2.imwrite(f"{output_dir}/boxes_page_{page_num}.png", image)


def process_images(directory, blur_size, kernel_size, edge_thresholds, pdf_document):
    for filename in os.listdir(directory):
        if filename.endswith(".jpeg"):
            image_path = os.path.join(directory, filename)
            print(f"Processing image: {image_path}")
            image = cv2.imread(image_path)
            page_num = int(os.path.splitext(filename)[0].split("_")[-1])
            dilated_image = process_image(
                image, blur_size, kernel_size, edge_thresholds
            )
            extract_boundary_boxes(image, dilated_image, page_num, pdf_document)


pdf_images_dir = "../pdf_images/"
blur_size = (11, 11)
kernel_size = (180, 10)
edge_thresholds = (50, 150)

pdf_document = pymupdf.open(pdf_path)
pdf_to_images(pdf_path, output_dir=pdf_images_dir)
process_images(pdf_images_dir, blur_size, kernel_size, edge_thresholds, pdf_document)
pdf_document.save("results.pdf")
