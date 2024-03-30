from PIL import Image
import face_recognition
import numpy as np

def compare_images(image1_path, image2_path):
    image1 = Image.open(image1_path)
    image2 = Image.open(image2_path)

    encoding1 = face_recognition.face_encodings(np.array(image1))
    encoding2 = face_recognition.face_encodings(np.array(image2))

    if not encoding1 or not encoding2:
        return False

    match = face_recognition.compare_faces(encoding1, encoding2)
    return any(match)
