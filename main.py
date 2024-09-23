import os
import json
import re
import cv2
import numpy as np

# Global variables
drawing = False  # True if mouse is pressed
ix, iy = -1, -1
ex, ey = -1, -1
current_label = 1
boxes = []
labels_list = []
annotations = {}
image_files = []
current_image_index = 0

# Define labels mapping from number keys to labels
label_map = {str(i): i for i in range(1, 10)}  # mapping keys '1'-'9' to labels 1-9

def mouse_callback(event, x, y, flags, param):
    global ix, iy, ex, ey, drawing, img, img_copy, boxes, labels_list, current_label

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
        ex, ey = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            ex, ey = x, y
            img = img_copy.copy()
            cv2.rectangle(img, (ix, iy), (ex, ey), (0, 255, 0), 2)
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        ex, ey = x, y
        cv2.rectangle(img, (ix, iy), (ex, ey), (0, 255, 0), 2)
        boxes.append((ix, iy, ex, ey))
        labels_list.append(current_label)
        img_copy = img.copy()

def save_annotations():
    global annotations, image_file, boxes, labels_list
    annotations[image_file] = []
    for box, label in zip(boxes, labels_list):
        x1, y1, x2, y2 = box
        annotations[image_file].append({
            'label': label,
            'box': [x1, y1, x2, y2]
        })

def export_yolo_dataset():
    global annotations
    os.makedirs('images', exist_ok=True)
    os.makedirs('labels', exist_ok=True)
    for img_name in annotations:
        img_path = os.path.join('frames', img_name)
        img = cv2.imread(img_path)
        height, width, _ = img.shape
        # Copy image to 'images' directory
        cv2.imwrite(os.path.join('images', img_name), img)
        # Create label file
        label_file_name = os.path.splitext(img_name)[0] + '.txt'
        label_path = os.path.join('labels', label_file_name)
        with open(label_path, 'w') as f:
            for annotation in annotations[img_name]:
                label = annotation['label'] - 1  # YOLO labels start from 0
                x1, y1, x2, y2 = annotation['box']
                # Convert to YOLO format
                x_center = ((x1 + x2) / 2) / width
                y_center = ((y1 + y2) / 2) / height
                box_width = abs(x2 - x1) / width
                box_height = abs(y2 - y1) / height
                f.write(f"{label} {x_center} {y_center} {box_width} {box_height}\n")

def sorted_numerically(image_list):
    def numerical_sort(value):
        # Extract numbers from the filenames to sort numerically
        parts = re.findall(r'\d+', value)
        return list(map(int, parts)) if parts else [0]
    
    return sorted(image_list, key=numerical_sort)                

def main():
    global img, img_copy, image_file, boxes, labels_list, current_label, current_image_index

    # Get list of image files
    image_files = [f for f in os.listdir('frames') if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        print("No images found in 'frames' directory.")
        return

    while current_image_index < len(image_files):
        image_file = image_files[current_image_index]
        img = cv2.imread(os.path.join('frames', image_file))
        if img is None:
            print(f"Failed to load image {image_file}")
            current_image_index += 1
            continue
        img_copy = img.copy()
        boxes = []
        labels_list = []

        cv2.namedWindow('Image')
        cv2.setMouseCallback('Image', mouse_callback)

        while True:
            cv2.imshow('Image', img)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('n'):  # Next image
                save_annotations()
                current_image_index += 1
                break
            elif key == ord('p') and current_image_index > 0:  # Previous image
                save_annotations()
                current_image_index -= 1
                break
            elif key == ord('s') or key == 27:  # Save and exit on 's' or 'ESC'
                save_annotations()
                with open('annotations.json', 'w') as f:
                    json.dump(annotations, f)
                cv2.destroyAllWindows()
                return
            elif key == ord('e'):  # Export YOLO dataset
                save_annotations()
                with open('annotations.json', 'w') as f:
                    json.dump(annotations, f)
                export_yolo_dataset()
                print("YOLO dataset exported.")
                cv2.destroyAllWindows()
                return
            elif chr(key) in label_map:
                current_label = label_map[chr(key)]
                print(f"Label set to {current_label}")
            elif key == ord('c'):  # Clear boxes
                boxes = []
                labels_list = []
                img = img_copy.copy()
            elif key == ord('u'):  # Undo last box
                if boxes:
                    boxes.pop()
                    labels_list.pop()
                    img = img_copy.copy()
                    for box in boxes:
                        x1, y1, x2, y2 = box
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    img_copy = img.copy()

        cv2.destroyAllWindows()

    # After all images are processed
    with open('annotations.json', 'w') as f:
        json.dump(annotations, f)
    print("All annotations saved.")

    export_yolo_dataset()

if __name__ == '__main__':
    main()
