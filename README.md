# zorginzichtPython
To run this app, following these steps:
1. Start xampp: sudo /opt/lampp/xampp start
2. Create a database named "zorginzichtPython" (do not need to creat any table)
3. Create table invoice initially: flask --debug create-tables
4. Run app.py: flask --debug run
5. Upload an invoice and save it in database: curl -F 'file=@./testdata/3.pdf' http://localhost:5000/upload_file/2342
6. Ask invoic per customer: curl http://localhost:5000/api/invoices/2342
