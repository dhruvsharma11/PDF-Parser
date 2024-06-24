from ultralytics import YOLO

# Load a model
model = YOLO("./models/best.pt")  # pretrained YOLOv8n model

# Run batched inference on a list of images
results = model.predict("./test", save=True, conf=0.3)  # # Process results list


# for result in results:
#     boxes = result.boxes  # Boxes object for bounding box outputs
#     masks = result.masks  # Masks object for segmentation masks outputs
#     keypoints = result.keypoints  # Keypoints object for pose outputs
#     probs = result.probs  # Probs object for classification outputs
#     obb = result.obb  # Oriented boxes object for OBB outputs
#     result.show()  # display to screen
#     result.save(filename="result.jpg")  # save to disk
