# flproj

1.* *User* is a table for ALL users (administrators and passengers/customers). It stores the username, first/last name, email/phone, password and the access level(which defines whether the user is administrator or passenger) for a particular user.
  * *Order* table uses user- and carId and also stores the dates of shipping/returning, order status(which can be placed, approved or delivered) and boolean variable which defines order completion.
  *Table called *Car* contains name field.
   
   ![alt text](https://github.com/irayarka/flproj/blob/lab-3/DB_UML.png)

2. [SQLAlchemy ORM Models](https://github.com/irayarka/flproj/blob/lab-3/models.py)
3. [File from versions](https://github.com/irayarka/flproj/blob/lab-3/7551ca4ed77b_.py)
