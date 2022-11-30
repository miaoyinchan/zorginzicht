import os
from pathlib import Path
from contextlib import contextmanager

import pymysql
import pymysql.cursors
from flask import Flask, flash, request, redirect, url_for, render_template, g, jsonify
from werkzeug.utils import secure_filename

from extract_info import extract_info, pdf_to_text, clean_text, tokenize


UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}


def get_db_conn():
    if "db" not in g:
        g.db = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="zorginzicht",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,
        )

    return g.db


def close_db(e=None):
    db = g.pop("db", None)

    if db is not None:
        db.close()


@contextmanager
def transaction():
    conn = get_db_conn()
    with conn.cursor() as cursor:
        yield cursor
    conn.commit()


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.teardown_appcontext(close_db)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.post('/upload_file')
def upload_file():
    url = url_for("overview")

    # check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename == '':
        flash('No selected file')
        return redirect(url)
    if file and not allowed_file(file.filename):
        flash('File not allowed')
        return redirect(url)

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect(url_for('overview'))


@app.get('/api/overview')
def api_overview():
    with transaction() as cursor:
        cursor.execute("SELECT 1")

    results = get_overview_data()
    return jsonify(results)


@app.get('/overview')
def overview():
    results = get_overview_data()
    return render_template("overview.html", invoices=results)


def get_overview_data():
    dir = os.listdir(UPLOAD_FOLDER)
    results = []

    if len(dir) == 0:
        print("There is no file uploaded.")
    else:
        for p in Path(UPLOAD_FOLDER).glob("*.pdf"):
            # print(p)
            text = pdf_to_text(p)
            new_lines = clean_text(text)
            tokens = tokenize(new_lines)
            results.append(extract_info(tokens))

    return results
