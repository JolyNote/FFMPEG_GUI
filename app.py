from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os
import subprocess
import shutil
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])

def upload():
    format = request.form.get('format_name')
    x = request.form.get('x')
    y = request.form.get('y')
    file = request.files['file']
    filename_formatless = file.filename.split('.')[0]

    if 'file' not in request.files:
        return 'Файл не найден'
    if file.filename == '':
        return 'Неправильный файл'
    filename = secure_filename(file.filename)
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(save_path):
        os.remove(save_path)
    file.save(save_path)

    result = os.system(f'ffmpeg -y -i uploads/{file.filename}  -vf scale={x}:{y} temp/{filename_formatless}.{format}')

    return f'{filename_formatless}.{format} <a href="/download/{filename_formatless}.{format}">Скачать файл</a>'


@app.route('/download/<filename>')
def download(filename):
    filepath = os.path.join('temp', filename)
    response = send_from_directory('temp', filename, as_attachment=True)
    os.remove(filepath)
    return response
    


if __name__ == '__main__':
    app.run(port=5003)

    