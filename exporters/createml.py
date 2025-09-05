import os
import cv2
import json
import shutil

def export_createml(annotations: dict, labels: list, images_path: str = 'frames', output_dir: str = 'exported/createml') -> None:
    os.makedirs(os.path.join(output_dir, 'images'), exist_ok=True)
    data = []
    for img_name, objs in annotations.items():
        img_path = os.path.join(images_path, img_name)
        img = cv2.imread(img_path)
        if img is None:
            continue
        shutil.copy(img_path, os.path.join(output_dir, 'images', img_name))
        anns = []
        for ann in objs:
            x1, y1, x2, y2 = ann['box']
            anns.append({
                'label': labels[ann['label']],
                'coordinates': {
                    'x': (x1 + x2) / 2,
                    'y': (y1 + y2) / 2,
                    'width': abs(x2 - x1),
                    'height': abs(y2 - y1)
                }
            })
        data.append({'image': img_name, 'annotations': anns})
    with open(os.path.join(output_dir, 'annotations.json'), 'w') as f:
        json.dump(data, f)
