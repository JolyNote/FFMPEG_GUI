from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['TEMP_FOLDER'] = 'temp'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'Файл не найден'

    file = request.files['file']
    if file.filename == '':
        return 'Неправильный файл'

    format = request.form.get('format_name')
    bitrate = request.form.get('bitrate')
    delaudio = request.form.get('delaudio')
    x = request.form.get('x')
    y = request.form.get('y')

    filename = secure_filename(file.filename)
    filename_formatless = file.filename.split('.')[0]
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(save_path):
        file.save(save_path)
    return convertation(format, x, y, bitrate, file, filename_formatless, delaudio)
    
def convertation(format, x, y, bitrate, file, filename_formatless, delaudio):

    # Проверка на существование битрейта
    if bitrate != '':
        bitrate_option = f'-b:a {bitrate}k'
    else:
        bitrate_option = ''

    # Поверка на существование скейла
    if x != '' and y != '':
        scale_option = f'-vf scale={x}:{y}'
    else:
        scale_option = ''

    # Удаление аудио из видео
    if delaudio == '1':
        del_audio = f'-an'
    else:
        del_audio = ''

    os.system(f'ffmpeg -y -i uploads/{file.filename} {scale_option} {bitrate_option} {del_audio} temp/{filename_formatless}.{format}')

    return f'{filename_formatless}.{format} <a href="/download/{filename_formatless}.{format}">Скачать файл </a>'

@app.route('/upload_audio', methods=['POST'])
def upload_audio():
    if 'file' not in request.files:
       return 'Файл не найден'

    file = request.files['file']
    if file.filename == '':
        return 'Неправильный файл'


    filename = secure_filename(file.filename)
    filename_formatless = file.filename.split('.')[0]
    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if not os.path.exists(save_path):
        file.save(save_path)
    return extraction(file, filename_formatless)

def extraction(file, filename_formatless):
    os.system(f'ffmpeg -y -i uploads/{file.filename} -vn -f mp3 temp/{filename_formatless}.mp3')

    return f'{filename_formatless}.mp3 <a href="/download/{filename_formatless}.mp3">Скачать файл </a>'

@app.route('/download/<filename>')
def download(filename):
    filepath = os.path.join(app.config['TEMP_FOLDER'], filename)
    response = send_from_directory(app.config['TEMP_FOLDER'], filename, as_attachment=True)
    os.remove(filepath)
    return response

if __name__ == '__main__':
    app.run(port=5007)
