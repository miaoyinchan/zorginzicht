import os
from pathlib import Path
from contextlib import contextmanager
from peewee import (
    MySQLDatabase, Model, BigIntegerField,
    DecimalField, CharField, DateField
)

import pymysql
import pymysql.cursors
from flask import Flask, flash, request, redirect, url_for, render_template, g, jsonify
from werkzeug.utils import secure_filename

from extract_info import extract_info, pdf_to_text, clean_text, tokenize

# DONE: connect with database server.
# DONE: create table Invoice.
# TODO: save the extracted info to table Invoice.
# TODO: create endpoint for table invoice.

# TODO: endpoint for extracted info
# TODO:
# [x] endpoint for uploading pdf.
# [ ] extract data from uploaded PDF
# [ ] insert extracted data in database


DATABASE = 'zorginzichtPython'
DEBUG = True

UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'pdf'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# create a peewee database instance -- our models will use this database to
# persist information.
mysql_db = MySQLDatabase(
    DATABASE,
    user="root",
    field_types={'auto_bigint': 'BIGINT AUTO_INCREMENT'},
)


class BaseModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = mysql_db


class AutoBigIntegerField(BigIntegerField):
    db_field = 'auto_bigint'


class Invoice(BaseModel):
    # id (bigint) PK auto-incrementing integer
    # customer_id (obtained from frontend url)
    # invoice_date(date)
    # amount (decimal)
    # caretype (varchar)
    id = AutoBigIntegerField(primary_key=True)
    customer_id = BigIntegerField(unique=True)
    invoice_date = DateField()
    amount = DecimalField()
    caretype = CharField()


# Custom command to create table initially.
@app.cli.command("create-tables")
def create_tables():
    with mysql_db:
        mysql_db.create_tables([Invoice])


# Request handlers -- these two hooks are provided by flask
# and we will use them to create and tear down a database
# connection on each request.
@app.before_request
def before_request():
    g.db = mysql_db
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Endpoint of uploading pdf, it deals with POST request from frontend
@app.post('/upload_file')
def upload_file():
    url = url_for("overview")

    # Check if the post request has the file part
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url)
    file = request.files['file']
    # If the user does not select a file, the browser submits an
    # empty file without a filename.
    if file.filename in ('', None):
        flash('No selected file')
        return redirect(url)
    if file and not allowed_file(file.filename):
        flash('File not allowed')
        return redirect(url)

    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    # return redirect(url_for('overview'))
    return {"status": "OK"}


# Endpoint of extracted info. of invoice
@app.get('/api/get_extracted_info')
def api_get_extracted_info():
    results = get_extracted_info()
    return jsonify(results)


@app.get('/overview')
def overview():
    results = get_extracted_info()
    return render_template("overview.html", invoices=results)


def get_extracted_info():
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
