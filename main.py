import os
import json
import re
import cv2
from exporters import export_dataset

with open('settings.json') as f:
    settings = json.load(f)

labels = settings.get('labels', [])
export_format = settings.get('export_format', 'YOLOv8')

current_label = 0
boxes = []
labels_list = []
annotations = {}
image_files = []
current_image_index = 0
img = None
img_original = None

label_map = {str(i + 1): i for i in range(len(labels))}
color_palette = [
    (0, 255, 0),
    (0, 0, 255),
    (255, 0, 0),
    (0, 255, 255),
    (255, 0, 255),
    (255, 255, 0),
    (128, 0, 128),
    (0, 128, 128),
    (128, 128, 0),
]
color_map = {i: color_palette[i % len(color_palette)] for i in range(len(labels))}

def draw_boxes():
    global img
    img = img_original.copy()
    for box, label in zip(boxes, labels_list):
        x1, y1, x2, y2 = box
        color = color_map.get(label, (0, 255, 0))
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        text_y = y1 - 10 if y1 - 10 > 10 else y1 + 20
        cv2.putText(img, labels[label], (x1, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

def save_annotations():
    global annotations, image_file, boxes, labels_list
    annotations[image_file] = []
    for box, label in zip(boxes, labels_list):
        x1, y1, x2, y2 = box
        annotations[image_file].append({'label': label, 'box': [x1, y1, x2, y2]})

def sorted_numerically(image_list):
    def numerical_sort(value):
        parts = re.findall(r'\d+', value)
        return list(map(int, parts)) if parts else [0]
    return sorted(image_list, key=numerical_sort)

def main():
    global img, img_original, image_file, boxes, labels_list, current_label, current_image_index
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
            if key == ord('n'):
                save_annotations()
                current_image_index += 1
                break
            elif key == ord('p') and current_image_index > 0:
                save_annotations()
                current_image_index -= 1
                break
            elif key == ord('s') or key == 27:
                save_annotations()
                with open('annotations.json', 'w') as f:
                    json.dump(annotations, f)
                cv2.destroyAllWindows()
                return
            elif key == ord('e'):
                save_annotations()
                with open('annotations.json', 'w') as f:
                    json.dump(annotations, f)
                export_dataset(export_format, annotations, labels)
                print(f"Dataset exported in {export_format} format.")
                cv2.destroyAllWindows()
                return
            elif chr(key) in label_map:
                current_label = label_map[chr(key)]
                print(f"Label set to {labels[current_label]} ({current_label})")
            elif key == ord('b'):
                roi = cv2.selectROI('Image', img, fromCenter=False, showCrosshair=True)
                cv2.destroyWindow('ROI')
                x, y, w, h = roi
                if w > 0 and h > 0:
                    boxes.append((x, y, x + w, y + h))
                    labels_list.append(current_label)
                    draw_boxes()
            elif key == ord('c'):
                boxes = []
                labels_list = []
                draw_boxes()
            elif key == ord('u') or key == 26:
                if boxes:
                    boxes.pop()
                    labels_list.pop()
                    draw_boxes()

        cv2.destroyAllWindows()

    with open('annotations.json', 'w') as f:
        json.dump(annotations, f)
    print("All annotations saved.")
    export_dataset(export_format, annotations, labels)

if __name__ == '__main__':
    main()
