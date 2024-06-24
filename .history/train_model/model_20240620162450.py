import os
from ultralytics import YOLO

# Load a model
model = YOLO("./models/best.pt")  # Pretrained YOLOv8n model

# Directory containing the test images
test_dir = "./test"

# Run batched inference on a list of images
results = model.predict(test_dir, conf=0.3)  # Process results list

# Iterate through each result in the batch
for result in results:
    # Extract the image path from the result
    image_path = result.path
    # Extract the base name of the image file (without directory and extension)
    base_name = os.path.basename(image_path).split(".")[0]
    # Create a text file name with the same base name
    text_file_path = f"{base_name}.txt"

    # Extract bounding boxes, classes, names, and confidences
    boxes = result.boxes.xyxy.tolist()
    classes = result.boxes.cls.tolist()
    confidences = result.boxes.conf.tolist()

    # Open the text file for writing
    with open(text_file_path, "w") as f:
        # Iterate through each detection in the result
        for box, cls, conf in zip(boxes, classes, confidences):
            x1, y1, x2, y2 = box
            confidence = conf
            detected_class = cls
            name = result.names[int(cls)]

            # Write the result to the file
            f.write(
                f"Class: {name}, Confidence: {confidence:.2f}, BBox: [{x1}, {y1}, {x2}, {y2}]\n"
            )
