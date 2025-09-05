import os
import cv2
import shutil
import xml.etree.ElementTree as ET

def export_pascal_voc(annotations: dict, labels: list, images_path: str = 'frames', output_dir: str = 'exported/pascal_voc') -> None:
    images_dir = os.path.join(output_dir, 'images')
    ann_dir = os.path.join(output_dir, 'annotations')
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(ann_dir, exist_ok=True)
    for img_name, objs in annotations.items():
        img_path = os.path.join(images_path, img_name)
        img = cv2.imread(img_path)
        if img is None:
            continue
        h, w, d = img.shape
        shutil.copy(img_path, os.path.join(images_dir, img_name))
        annotation = ET.Element('annotation')
        ET.SubElement(annotation, 'filename').text = img_name
        size = ET.SubElement(annotation, 'size')
        ET.SubElement(size, 'width').text = str(w)
        ET.SubElement(size, 'height').text = str(h)
        ET.SubElement(size, 'depth').text = str(d)
        for ann in objs:
            obj = ET.SubElement(annotation, 'object')
            ET.SubElement(obj, 'name').text = labels[ann['label']]
            bndbox = ET.SubElement(obj, 'bndbox')
            x1, y1, x2, y2 = ann['box']
            ET.SubElement(bndbox, 'xmin').text = str(x1)
            ET.SubElement(bndbox, 'ymin').text = str(y1)
            ET.SubElement(bndbox, 'xmax').text = str(x2)
            ET.SubElement(bndbox, 'ymax').text = str(y2)
        tree = ET.ElementTree(annotation)
        xml_path = os.path.join(ann_dir, os.path.splitext(img_name)[0] + '.xml')
        tree.write(xml_path)
