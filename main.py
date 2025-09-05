import os
import json
import re
import cv2

# Global variables
current_label = 1
boxes = []
labels_list = []
annotations = {}
image_files = []
current_image_index = 0
img = None
img_original = None

# Define labels mapping from number keys to labels
label_map = {str(i): i for i in range(1, 10)}  # mapping keys '1'-'9' to labels 1-9

# Define color map for labels
color_map = {
    1: (0, 255, 0),
    2: (0, 0, 255),
    3: (255, 0, 0),
    4: (0, 255, 255),
    5: (255, 0, 255),
    6: (255, 255, 0),
    7: (128, 0, 128),
    8: (0, 128, 128),
    9: (128, 128, 0)
}

def draw_boxes():
    global img
    img = img_original.copy()
    for box, label in zip(boxes, labels_list):
        x1, y1, x2, y2 = box
        color = color_map.get(label, (0, 255, 0))
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        text_y = y1 - 10 if y1 - 10 > 10 else y1 + 20
        cv2.putText(img, str(label), (x1, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

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
    global img, img_original, image_file, boxes, labels_list, current_label, current_image_index

    # Get list of image files
    image_files = [f for f in os.listdir('frames') if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not image_files:
        print("No images found in 'frames' directory.")
        return

    while current_image_index < len(image_files):
        image_file = image_files[current_image_index]
        img_original = cv2.imread(os.path.join('frames', image_file))
        if img_original is None:
            print(f"Failed to load image {image_file}")
            current_image_index += 1
            continue
        img = img_original.copy()
        boxes = []
        labels_list = []

        cv2.namedWindow('Image')

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
            elif key == ord('b'):  # Add bounding box
                roi = cv2.selectROI('Image', img, fromCenter=False, showCrosshair=True)
                cv2.destroyWindow('ROI')
                x, y, w, h = roi
                if w > 0 and h > 0:
                    boxes.append((x, y, x + w, y + h))
                    labels_list.append(current_label)
                    draw_boxes()
            elif key == ord('c'):  # Clear boxes
                boxes = []
                labels_list = []
                draw_boxes()
            elif key == ord('u') or key == 26:  # Undo last box (u or Ctrl+Z)
                if boxes:
                    boxes.pop()
                    labels_list.pop()
                    draw_boxes()

        cv2.destroyAllWindows()

    # After all images are processed
    with open('annotations.json', 'w') as f:
        json.dump(annotations, f)
    print("All annotations saved.")

    export_yolo_dataset()

if __name__ == '__main__':
    main()
