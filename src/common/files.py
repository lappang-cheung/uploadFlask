# common/files.py
import os
from werkzeug.utils import secure_filename

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

def uploads_url(path):
    target = os.path.join(APP_ROOT, 'pdfs/')

    if not os.path.isdir(target):
        os.mkdir(target)
    return path.replace(target, '/uploads')

def save_to(folder, file):
    os.makedirs(folder, exist_ok=True)
    save_path = os.path.join(folder, secure_filename(file.filename))
    file.save(save_path)
    return save_path