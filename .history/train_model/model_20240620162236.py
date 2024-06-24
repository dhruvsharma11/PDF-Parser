from ultralytics import YOLO

# Load a model
model = YOLO("./models/best.pt")  # Pretrained YOLOv8n model

# Run batched inference on a list of images
results = model.predict("./test", conf=0.3)  # Process results list

# Iterate through each result in the batch
for result in results:
    # Extract bounding boxes, classes, names, and confidences
    boxes = result.boxes.xyxy.tolist()
    classes = result.boxes.cls.tolist()
    confidences = result.boxes.conf.tolist()

    # Iterate through each detection in the result
    for box, cls, conf in zip(boxes, classes, confidences):
        with open("results.txt", "a") as f:
            x1, y1, x2, y2 = box
            confidence = conf
            detected_class = cls
            name = result.names[int(cls)]

            # Write the result to the file
            f.write(
                f"Class: {name}, Confidence: {confidence:.2f}, BBox: [{x1}, {y1}, {x2}, {y2}]\n"
            )
