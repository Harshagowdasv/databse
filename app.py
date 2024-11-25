from flask import Flask, render_template, request, redirect, url_for
import csv
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Check if uploaded file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        name = request.form['name']
        file = request.files['image']

        if 'image' not in request.files or file.filename == '':
            return "No image file selected."

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Save the name and image path (full path) in the CSV file
            with open('data.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                # Save the name and the full path of the image
                writer.writerow([name, filepath])
            
            return redirect(url_for('upload_file'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
