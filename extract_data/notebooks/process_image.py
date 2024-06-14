import cv2
import numpy as np
import pytesseract
from matplotlib import pyplot as plt

# Load the image
image_path = "../pdf_images/page_1.jpeg"
image = cv2.imread(image_path)

# Convert to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Threshold the image to get a binary image
_, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)

# Define a kernel for morphological operations
kernel = np.ones((5, 5), np.uint8)

# Remove horizontal lines using morphological operations
horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 1))
detected_lines = cv2.morphologyEx(
    binary, cv2.MORPH_OPEN, horizontal_kernel, iterations=2
)

# Find contours of detected lines
cnts, _ = cv2.findContours(detected_lines, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Remove the detected horizontal lines from the binary image
for c in cnts:
    cv2.drawContours(binary, [c], -1, (0, 0, 0), 2)

# Remove the thick header at the top
header_height = 250
binary[:header_height, :] = 0

# Invert binary image to prepare for OCR
processed_image = cv2.bitwise_not(binary)

# Save the processed image
cv2.imwrite("../processed_image.png", processed_image)

# Perform OCR on the processed image
ocr_result = pytesseract.image_to_string(processed_image)

# Save OCR result to a text file
with open("../extracted_text.txt", "w") as file:
    file.write(ocr_result)
