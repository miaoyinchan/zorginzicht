import os
from pathlib import Path
from contextlib import contextmanager
from datetime import datetime

import pymysql
import pymysql.cursors
from flask import Flask, flash, request, redirect, url_for, g, jsonify
from werkzeug.utils import secure_filename
from peewee import (
    MySQLDatabase, Model, BigIntegerField, fn,
    DecimalField, CharField, DateField, IntegerField
)
from playhouse.shortcuts import model_to_dict

from extract_info import extract_info, pdf_to_text, clean_text, tokenize

# DONE: connect with database server.
# DONE: create table Invoice.
# DONE: create endpoint of uploading invoice (pdf) per customer.
# DONE: extract info from uploaded invoice.
# DONE: save the extracted info to table Invoice.
# DONE: create endpoint for getting invoice per customer.
# DONE: sum up amount per caretype per customer.
# DONE: create endpoint for getting sum per caretype per customer.


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
    # invoice_nr (int)
    # id = AutoBigIntegerField(primary_key=True)
    customer_id = BigIntegerField() # One customer can upload more than 1 invoice.
    invoice_date = DateField()
    amount = DecimalField()
    caretype = CharField()
    invoice_nr = IntegerField()


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
# Test with: curl -F 'file=@./testdata/3.pdf' http://localhost:5000/upload_file/2342
@app.post('/upload_file/<int:customer_id>')
def upload_file(customer_id):

    # Check if the post request has the file part
    if 'file' not in request.files:
        return {"status": "error", "message": "no file in request"}

    file = request.files['file']

    if not file or not file.filename:
        return {"status": "error", "message": "no file"}
    if file and not allowed_file(file.filename):
        return {"status": "error", "message": "file now allowed"}

    filename = secure_filename(file.filename)
    filepath = Path(app.config['UPLOAD_FOLDER']) / filename
    file.save(filepath)

    text = pdf_to_text(filepath)
    new_lines = clean_text(text)
    tokens = tokenize(new_lines)
    results = extract_info(tokens)
    print(results)

    # Save the extracted info in database (table Invoice).
    # FIXED: extract_info does not have consistent results! Query fails!
    fallback_invoice_date = datetime.now().date()
    Invoice.create(
        customer_id=customer_id,
        invoice_date=results.get('invoice_date', fallback_invoice_date),
        amount=results.get('amount'),
        caretype=results.get('caretype'),
        invoice_nr=results.get('invoice_nr'),
    )

    return {"status": "OK"}


# Test with: curl -v http://localhost:5000/api/invoices/2342
# Endpoint for getting invoice per customer.
@app.get("/api/invoices/<int:customer_id>")
def get_invoices(customer_id):
    return {
        "status": "OK",
        "results": [
            model_to_dict(invoice)
            for invoice in Invoice
                .select()
                .where(Invoice.customer_id == customer_id)
        ],
    }


# Test with: curl -v http://localhost:5000/api/sum_per_caretype/2342
# Endpoint for getting sum per caretype per customer.
@app.get("/api/sum_per_caretype/<int:customer_id>")
def get_sum_per_caretype(customer_id):
    invoices = Invoice.select(
        Invoice.caretype, fn.SUM(Invoice.amount).alias("sum")
    ).where(Invoice.customer_id == customer_id).group_by(Invoice.caretype)
    print()
    return {
        "status": "OK",
        "results": [
            {"caretype": invoice.caretype, "total": invoice.sum}
            for invoice in invoices
        ],
    }
