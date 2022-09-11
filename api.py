from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import mariadb
import json
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base


app = Flask(__name__)
engine = sqlalchemy.create_engine("mariadb+mariadbconnector://test:12345@localhost:3306/librarycatalog")
Base = declarative_base()

Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()


@app.route('/test', methods=['GET'])
def test():
    return {
        'test': 'test1'
    }


@app.route('/employees', methods=['GET'])
def getEmployees():

    allEmployees = session.query(Employee).get(1)

    return {
        'test': allEmployees
        }

class Employee(Base):
   __tablename__ = 'employees'
   id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
   firstname = sqlalchemy.Column(sqlalchemy.String(length=100))
   lastname = sqlalchemy.Column(sqlalchemy.String(length=100))
   active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

Base.metadata.create_all(engine)

# Create a session
# Session = sqlalchemy.orm.sessionmaker()
# Session.configure(bind=engine)
# session = Session()

## Add some new employees
# addEmployee("Bruce", "Wayne")
# addEmployee("Diana", "Prince")
# addEmployee("Clark", "Kent")

# Show all employees
print('All Employees')
selectAll()
print("----------------")

# Update employee status
updateEmployeeStatus(2,False)

# Show active employees
print('Active Employees')
selectByStatus(True)
print("----------------")

# Delete employee
# deleteEmployee(1)
