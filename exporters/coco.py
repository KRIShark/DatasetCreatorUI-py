import os
import cv2
import json
import shutil

def export_coco(annotations: dict, labels: list, images_path: str = 'frames', output_dir: str = 'exported/coco') -> None:
    images = []
    anns = []
    categories = [{"id": i, "name": name} for i, name in enumerate(labels)]
    os.makedirs(os.path.join(output_dir, 'images'), exist_ok=True)
    ann_id = 1
    for img_id, (img_name, objs) in enumerate(annotations.items(), start=1):
        img_path = os.path.join(images_path, img_name)
        img = cv2.imread(img_path)
        if img is None:
            continue
        h, w, _ = img.shape
        shutil.copy(img_path, os.path.join(output_dir, 'images', img_name))
        images.append({"id": img_id, "file_name": img_name, "width": w, "height": h})
        for ann in objs:
            x1, y1, x2, y2 = ann['box']
            bbox = [x1, y1, x2 - x1, y2 - y1]
            anns.append({
                "id": ann_id,
                "image_id": img_id,
                "category_id": ann['label'],
                "bbox": bbox,
                "area": (x2 - x1) * (y2 - y1),
                "iscrowd": 0
            })
            ann_id += 1
    coco = {"images": images, "annotations": anns, "categories": categories}
    os.makedirs(output_dir, exist_ok=True)
    with open(os.path.join(output_dir, 'annotations.json'), 'w') as f:
        json.dump(coco, f)
