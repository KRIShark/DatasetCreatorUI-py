"""Export dataset in various formats."""
import os
from .yolo import export_yolo
from .coco import export_coco
from .pascal_voc import export_pascal_voc
from .tfrecord import export_tfrecord
from .paligemma import export_paligemma
from .createml import export_createml

EXPORTERS = {
    "YOLOv8": export_yolo,
    "YOLOv5": export_yolo,
    "YOLOv7": export_yolo,
    "YOLOv9": export_yolo,
    "YOLOv11": export_yolo,
    "YOLO Darknet": export_yolo,
    "COCO JSON": export_coco,
    "Pascal VOC XML": export_pascal_voc,
    "TFRecord": export_tfrecord,
    "PaliGemma": export_paligemma,
    "CreateML JSON": export_createml,
}


def export_dataset(fmt: str, annotations: dict, labels: list, images_path: str = "frames") -> None:
    exporter = EXPORTERS.get(fmt)
    if exporter is None:
        raise ValueError(f"Unsupported export format: {fmt}")
    exporter(annotations, labels, images_path)
