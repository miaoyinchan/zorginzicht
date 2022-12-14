# zorginzichtPython
To run this app, following these steps:
1. pip install -r requirements.txt
2. start xampp: sudo /opt/lampp/xampp start
3. create a database named "zorginzichtPython" (do not need to creat any table)
4. create table invoice initially: flask --debug create-tables
5. run app.py: flask --debug run
6. open in browser: http://127.0.0.1:5000/static/index.html
7. upload invoices from ./testdata folder
8. view Invoice table in db, you will see the uploaded invoice inserted in the table.
9. test endpoint for getting sum per cartype per customer:
   curl -v http://localhost:5000/api/sum_per_caretype/2342

   SELECT caretype, SUM(amount) FROM `invoice` WHERE customer_id=2342 GROUP BY caretype;

10. cd /home/an/Sources/ZorginzichtBackend1/WebApplication3 (or your dir to this code)
11. dotnet run
12. open browser to: http://localhost:5008/swagger/index.html
