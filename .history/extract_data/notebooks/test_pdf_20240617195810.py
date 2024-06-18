# Open the PDF document
output_pdf_path = "results.pdf"


import pymupdf

# Coordinates from the PNG image
png_x0, png_y0, png_x1, png_y1 = 0, 274, 2550, 788

# Open the PDF document
pdf_path = "../pdf/baldwing-catalog-test.pdf"
doc = pymupdf.open(pdf_path)
page = doc[0]


# Get page height for coordinate transformation
page_height = page.rect.height

# Convert from pixels to points (assuming 72 DPI for PDF)
pdf_x0 = png_x0 * 72 / 300  # Adjust DPI if necessary
pdf_x1 = png_x1 * 72 / 300
pdf_y0 = png_y0 * 72 / 300
pdf_y1 = png_y1 * 72 / 300

default_cropbox = page.cropbox

print(default_cropbox)
# Create a PyMuPDF Rect object with PDF coordinates
pdf_rect = pymupdf.Rect(pdf_x0, pdf_y0, pdf_x1, pdf_y1)

page.set_cropbox(pdf_rect)


for info in page.get_images():
    xref = info[0]
    img = doc.extract_image(xref)
    ext, data = img["ext"], img["image"]

    with open(f"{xref}.{ext}", "wb") as f:
        f.write(data)


# page.set_cropbox(default_cropbox)

# Extract the image from the PDF


# info = page.get_images()

# xref = info[0][0]

# pix = pymupdf.Pixmap(doc, xref)

# pix.save("image.png")

# print(xref)

# for info in page.get_image_info():
#     xref = info[0]
#     img = doc.extractImage(xref)
#     ext, data = img["ext"], img["image"]

#     with open(f"/{xref}.{ext}", "wb") as f:
#         f.write(data)


# Optionally, draw the rectangle on the PDF (uncomment if needed)
rect_color = (1, 0, 0)  # Red color in RGB
page.draw_rect(pdf_rect, color=rect_color, width=1)

# Save the modified PDF
doc.save(output_pdf_path)

# Close the document
doc.close()
