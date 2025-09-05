import os
import cv2
import shutil

def export_yolo(annotations: dict, labels: list, images_path: str = 'frames', output_dir: str = 'exported/yolo') -> None:
    images_dir = os.path.join(output_dir, 'images')
    labels_dir = os.path.join(output_dir, 'labels')
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(labels_dir, exist_ok=True)
    for img_name, objs in annotations.items():
        img_src = os.path.join(images_path, img_name)
        img = cv2.imread(img_src)
        if img is None:
            continue
        h, w, _ = img.shape
        shutil.copy(img_src, os.path.join(images_dir, img_name))
        label_path = os.path.join(labels_dir, os.path.splitext(img_name)[0] + '.txt')
        with open(label_path, 'w') as f:
            for ann in objs:
                label = ann['label']
                x1, y1, x2, y2 = ann['box']
                x_c = ((x1 + x2) / 2) / w
                y_c = ((y1 + y2) / 2) / h
                bw = abs(x2 - x1) / w
                bh = abs(y2 - y1) / h
                f.write(f"{label} {x_c} {y_c} {bw} {bh}\n")
