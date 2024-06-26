# Project 5: School Surveillance System

**Contributor:**
- Kunal Pratyush Srivastav

**Grade:** XII

**School:** Shaheed Rajpal DAV Public School, Delhi



# Face Recognition System using OpenCV and Face Recognition Library

This Python script implements a basic face recognition system using OpenCV and the face recognition library. The system detects faces in a live video stream from a webcam and compares them with known faces stored in a specified directory.

## Requirements

- Python 3.11

## Setup

1. Clone or download this repository to your local machine.

2. Activate the virtual environment:

    ```
    source venv/bin/activate   # On Linux/Mac
    venv\Scripts\activate      # On Windows
    ```

3. Install the required dependencies using pip:

    ```
    pip install -r requirements.txt
    ```

## Usage

1. Prepare the known person images:
    - There is a folder named `Images` in the root directory.
    - Add images of known persons to this folder. Ensure that each image contains only one face.

2. Run the Python script:

    ```
    python face_recognition_system.py
    ```

3. The webcam will open, and the script will start detecting faces in the live video stream.
   
4. Press 'q' to exit the program.

## Customization

- You can change the directory containing known person images by modifying the `known_images_folder` variable in the script.

- Adjust the rectangle colors for known and unknown persons by modifying the `color` variable.

## Credits

This project utilizes the following libraries:

- OpenCV: https://github.com/opencv/opencv
- Face Recognition: https://github.com/ageitgey/face_recognition
