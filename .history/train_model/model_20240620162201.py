from ultralytics import YOLO

# Load a model
model = YOLO("./models/best.pt")  # pretrained YOLOv8n model

# Run batched inference on a list of images
results = model.predict("./test", conf=0.3)  # # Process results list


for result in results:
    # Extract bounding boxes, classes, names, and confidences
    boxes = results[0].boxes.xyxy.tolist()
    classes = results[0].boxes.cls.tolist()
    names = results[0].names
    confidences = results[0].boxes.conf.tolist()

    # Iterate through the results
    for box, cls, conf in zip(boxes, classes, confidences):
        with open("results.txt", "a") as f:
            x1, y1, x2, y2 = box
            confidence = conf
            detected_class = cls
            name = names[int(cls)]
