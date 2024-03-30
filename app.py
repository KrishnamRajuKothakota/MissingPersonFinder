from flask import Flask, render_template, request
import face_recognition
from PIL import Image

app = Flask(__name__)

missing_persons = []

def compare_images(image1_path, image2_path):
    image1 = face_recognition.load_image_file(image1_path)
    image2 = face_recognition.load_image_file(image2_path)

    image1_encoding = face_recognition.face_encodings(image1)
    image2_encoding = face_recognition.face_encodings(image2)

    if not image1_encoding or not image2_encoding:
        return False

    match = face_recognition.compare_faces(image1_encoding, image2_encoding[0])
    return match[0]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    age = request.form['age']
    phone = request.form['phone']
    image = request.files['image']

    missing_persons.append({'name': name, 'age': age, 'phone': phone, 'image': image.filename})
    image.save(f'uploads/{image.filename}')

    return 'Registered successfully!'

@app.route('/upload', methods=['POST'])
def upload():
    uploaded_image = request.files['image']

    for missing_person in missing_persons:
        # if uploaded_image.filename in f'uploads/{missing_person["image"]}':
        if compare_images(uploaded_image,f'uploads/{missing_person["image"]}'):
            return f'Match found! Details: {missing_person}'
    
    # if uploaded_image.filename not in f'uploads/{missing_person["image"]}':
    #     return 'No match found'
    return 'No match found.'

if __name__ == '__main__':
    app.run(debug=True, port=5001)