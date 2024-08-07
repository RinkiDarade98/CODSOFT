import cv2
import os
import numpy as np

# Load HAAR face classifier
face_classifier = cv2.CascadeClassifier('data/haarcascade_frontalface_default.xml')

# Load functions
def face_extractor(img):
    # Function detects faces and returns the cropped face
    # If no face detected, it returns None
    faces = face_classifier.detectMultiScale(img, 1.3, 5)
    
    if len(faces) == 0:
        return None
    
    # Crop the first face found
    for (x, y, w, h) in faces:
        x = x - 10
        y = y - 10
        cropped_face = img[y:y + h + 50, x:x + w + 50]
        return cropped_face

# Initialize Webcam
cap = cv2.VideoCapture(0)
count = 0

# Prompt user for their name
name = input("Enter Your Name: ")

# Create a directory for the user if it doesn't exist
user_folder = os.path.join('Images', name)
if not os.path.exists(user_folder):
    os.makedirs(user_folder)

# Collect 100 samples of your face from webcam input
while True:
    ret, frame = cap.read()
    if face_extractor(frame) is not None:
        count += 1
        face = cv2.resize(face_extractor(frame), (400, 400))

        # Save file in the user's directory with a unique name
        file_name_path = os.path.join(user_folder, str(count) + '.jpg')
        cv2.imwrite(file_name_path, face)

        # Put count on images and display live count
        cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow('Face Cropper', face)
        
    else:
        print("Face not found")
        pass

    if cv2.waitKey(1) == 13 or count == 100:  # 13 is the Enter Key
        break
        
cap.release()
cv2.destroyAllWindows()      
print("Collecting Samples Complete")
