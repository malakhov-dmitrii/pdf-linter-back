
from json_exporter import export_as_json
import os
from flask import Flask, flash, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    file_name = request.args.get('file')
    return jsonify(export_as_json(file_name))
    # return "200"


if __name__ == '__main__':
    app.run()
