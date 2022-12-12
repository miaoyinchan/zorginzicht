# zorginzichtPython
To run this app, following these steps:
1. pip install -r requirements.txt
2. Start xampp: sudo /opt/lampp/xampp start
3. Create a database named "zorginzichtPython" (do not need to creat any table)
4. Create table invoice initially: flask --debug create-tables
5. Run app.py: flask --debug run
6. Upload an invoice and save it in database: curl -F 'file=@./testdata/3.pdf' http://localhost:5000/upload_file/2342
7. Ask invoic per customer: curl http://localhost:5000/api/invoices/2342
