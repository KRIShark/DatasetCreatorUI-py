import os
import json

def export_tfrecord(annotations: dict, labels: list, images_path: str = 'frames', output_dir: str = 'exported/tfrecord') -> None:
    os.makedirs(output_dir, exist_ok=True)
    # Placeholder implementation writing JSON instead of real TFRecord
    with open(os.path.join(output_dir, 'data.tfrecord'), 'w') as f:
        json.dump({'annotations': annotations, 'labels': labels}, f)
