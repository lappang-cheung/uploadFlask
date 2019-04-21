import os
from uuid import uuid4
from subprocess import TimeoutExpired
from flask import Flask, render_template, request, jsonify
from common.docxtopdf import LibreOfficeError, convert_to
from common.errors import RestAPIError, InternalServerErrorError

__author__ = 'leo'

app = Flask(__name__)

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Routes
@app.route("/")

def index():
    return render_template("upload.html")

@app.route("/upload", methods=['POST'])

def upload():
    target = os.path.join(APP_ROOT, 'docs/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)

    return render_template("complete.html")

@app.route("/uploads", methods=['Post'])

def uploads():
    upload_id = str(uuid4())
    target = os.path.join(APP_ROOT, 'pdfs/')
    source = os.path.join(APP_ROOT, 'docs/')
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        print(file)
        filename = file.filename
        destination = "/".join([target, filename])
        previous = "/".join([source,filename])
        print(previous)

        try:
            result = convert_to(source,previous,timeout=15)
        except LibreOfficeError:
            raise InternalServerErrorError({'message': 'Error when converting file to PDF'})

        print(result)

    return render_template("complete.html")


if __name__=="__main__":
    app.run(port=4444, debug=True)