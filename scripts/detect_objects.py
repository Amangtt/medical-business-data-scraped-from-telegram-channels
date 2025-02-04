import torch
import cv2
import os
import pandas as pd
from PIL import Image
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    ormat="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("../logs/data_cleaning.log"),
        logging.StreamHandler()
            ]
)
# Load YOLOv5 model
try:
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    logging.info("✅ model loaded successfully.")
except Exception as e:
    logging.error(f"❌ Error loading model: {e}")
    raise
# Folder containing images collected from Telegram
image_folder = "./photos_"
output_folder = "./detections"
os.makedirs(output_folder, exist_ok=True)  # Ensure output folder exists

# Allowed image extensions
valid_extensions = (".jpg", ".jpeg", ".png")

# List to store detection results
detection_results = []

# Process each image in the folder
for img_file in os.listdir(image_folder):
    if not img_file.lower().endswith(valid_extensions):
        continue  # Skip non-image files

    img_path = os.path.join(image_folder, img_file)

    # Run YOLO object detection
    results = model(img_path)

    # Extract bounding boxes, class labels, and confidence scores
    for *box, conf, cls in results.xyxy[0]:  # xyxy format
        detection_results.append({
            "filename": img_file,
            "class_label": results.names[int(cls)],
            "confidence": float(conf),
            "bbox": [float(coord) for coord in box]
        })

    # Save the detection image manually to avoid multiple folders
    img_with_boxes = results.render()[0]  # Get image with bounding boxes
    img_with_boxes = Image.fromarray(img_with_boxes)  # Convert to PIL Image
    img_with_boxes.save(os.path.join(output_folder, img_file))  # Save in one folder

# Convert detection results to a DataFrame and save as CSV
try:
    df = pd.DataFrame(detection_results)
    df.to_csv("detections.csv", index=False)
    logging.info("Object detection completed. Results saved in 'detections/' and 'detections.csv'.")
except Exception as e:
    logging.error(f"❌ Error loading model: {e}")
    raise

