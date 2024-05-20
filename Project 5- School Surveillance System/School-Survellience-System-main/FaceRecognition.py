import os
import cv2
import face_recognition

# Directory containing known person images
known_images_folder = "Images"  # Change this to the folder path containing known person images

# Load the known images and encode the faces
known_encodings = []
for filename in os.listdir(known_images_folder):
    path = os.path.join(known_images_folder, filename)
    known_image = face_recognition.load_image_file(path)
    encoding = face_recognition.face_encodings(known_image)[0]
    known_encodings.append(encoding)

# Initialize video capture
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    # Find face locations in the frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Loop through the detected faces
    for face_location, face_encoding in zip(face_locations, face_encodings):
        # Compare the encodings with known encodings
        results = face_recognition.compare_faces(known_encodings, face_encoding)

        # Draw a rectangle around the detected face with green color for known persons and red color for unknown persons
        top, right, bottom, left = face_location
        color = (0, 255, 0) if True in results else (0, 0, 255)
        cv2.rectangle(frame, (left, top), (right, bottom), color, 2)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release video capture
video_capture.release()
cv2.destroyAllWindows()
