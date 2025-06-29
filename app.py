from flask import Flask, render_template, request, send_from_directory
from rembg import remove
from PIL import Image
import os
import uuid

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'results'

@app.route('/', methods=['GET', 'POST'])
def index():
    image_url = None
    if request.method == 'POST':
        if 'image' not in request.files:
            return render_template('index.html', error='No file uploaded.')
        file = request.files['image']
        if file.filename == '':
            return render_template('index.html', error='No file selected.')
        filename = f"{uuid.uuid4().hex}.png"
        input_path = os.path.join(UPLOAD_FOLDER, filename)
        output_path = os.path.join(RESULT_FOLDER, filename)
        file.save(input_path)

        input_image = Image.open(input_path)
        output_image = remove(input_image)
        output_image.save(output_path)

        image_url = f'/results/{filename}'
    return render_template('index.html', image_url=image_url)

@app.route('/results/<filename>')
def result_file(filename):
    return send_from_directory(RESULT_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
