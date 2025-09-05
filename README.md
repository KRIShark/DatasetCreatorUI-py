# YOLOv8 Dataset Creation Tool

This Python tool allows you to create labeled datasets for various model training by annotating images with bounding boxes and exporting them in multiple formats.

## Setup Manual

### Prerequisites:

- Python 3.x installed on your system.

### Installation Steps:

1. **Install Required Packages:**

   Open a command prompt or terminal, navigate to the directory containing the script, and run:

uv pip install -r requirements.txt


2. **Prepare the 'frames' Directory:**

Ensure that you have a folder named `frames` in the same directory as the script. This folder should contain all the images you want to annotate. If you have a JSON file with existing labels, place it inside this `frames` directory.
3. **Configure settings:**

   Edit `settings.json` to define label names and choose an export format. The index of each label in the array is used as the class id.
   Example:
   ```json
   {
     "labels": ["EnamyTank", "FrendlyTank"],
     "export_format": "YOLOv8"
   }
   ```
   Supported export formats: YOLOv11, YOLOv9, YOLOv8, YOLOv5, YOLOv7, COCO JSON, YOLO Darknet, Pascal VOC XML, TFRecord, PaliGemma, CreateML JSON.

---

## User Manual

### Starting the Application:

Run the script by executing:

uv run main.py


Replace `your_script_name.py` with the actual name of the script file.

### Annotating Images:

- **Display:**

  - The application will load and display images from the `frames` directory one by one in a window titled 'Image'.

- **Drawing Bounding Boxes:**

  - **Select a Label:**

    - Before drawing a box, select a label by pressing number keys starting from **1** on your keyboard.
    - The selected label will be printed in the console.

  - **Add a Box:**

    - Press **'b'** to open the ROI selector.
    - Draw the box and press **Enter** or **Space** to confirm.
    - Each box is shown in a color corresponding to its label with the label number displayed above it.

- **Navigating Between Images:**

  - Press **'n'** to proceed to the **next image**.
  - Press **'p'** to go back to the **previous image**.

### Saving and Exiting:

- **Save Annotations and Exit:**

  - Press **'s'** or the **'ESC'** key to save all annotations to `annotations.json` and exit the application.

- **Export Dataset:**

  - Press **'e'** to save annotations and export the dataset in the format specified in `settings.json`.
  - Images will be copied to an `images` folder, and label files will be created in a `labels` folder.

### Additional Controls:

- **Clear All Boxes on Current Image:**

  - Press **'c'** to remove all drawn bounding boxes on the current image.

- **Undo Last Box:**
  - Press **Ctrl+Z** or **'u'** to undo the last bounding box you drew.

### Annotations File:

- Annotations are saved in a JSON file named `annotations.json` in the same directory as the script.
- The format includes the image name, labels, and bounding box coordinates.

### YOLO Dataset Format:

- When exporting in YOLO formats, each image will have a corresponding label file with the same base name and a `.txt` extension.
- Label files contain lines in the format:

<class_id> <x_center> <y_center> <width> <height>


- Coordinates are normalized between 0 and 1.
- `class_id` starts from 0.

### Example of a Label File:

0 0.5444 0.4045 0.0249 0.0842


### Notes:

- Ensure that you select the correct label before drawing each bounding box.
- The labels correspond to the number keys pressed:

  - Pressing **'1'** selects the first label, **'2'** selects the second, and so on.

- The application assumes labels start at **1**.

### Troubleshooting:

- **Images Not Displaying:**

  - Verify that images are in the `frames` directory.
  - Supported image formats are `.jpg`, `.jpeg`, and `.png`.

- **No Images Found Error:**

  - Ensure the `frames` directory is in the same location as the script and contains images.

- **Incorrect Labeling:**

  - Remember that YOLO class IDs start from 0, so label **1** becomes **0** in YOLO format.

### Exiting the Application:

- To ensure all your work is saved, use the **'s'**, **'e'**, or **'ESC'** keys to exit properly.

---
