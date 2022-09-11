from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

import mariadb
import json
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

# Define the MariaDB engine using MariaDB Connector/Python
engine = sqlalchemy.create_engine("mariadb+mariadbconnector://test:12345@localhost:3306/librarycatalog")
db = sqlalchemy.orm.sessionmaker()
db.configure(bind=engine)
db = db()

app = Flask(__name__)
Base = declarative_base()

# Define the class for what an employee is
class Employee(Base):
    __tablename__ = 'employees'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    firstname = sqlalchemy.Column(sqlalchemy.String(length=100))
    lastname = sqlalchemy.Column(sqlalchemy.String(length=100))

    def __init__(self, firstname, lastname, id):
        self.firstname = firstname
        self.lastname = lastname
        self.id = id

@app.route('/test', methods=['GET'])
def test():
    return {
        'test': 'test1'
            }

# Provide a search function that returns all current DB entries
@app.route('/search', methods=['GET'])
def getEmployees():
    allEmployees = db.query(Employee).all()
    output = []
    for employee in allEmployees:
        currEmp = {}
        currEmp['firstname']= employee.firstname
        currEmp['lastname']= employee.lastname
        currEmp['id']= employee.id
        output.append(currEmp)
    return jsonify(output)

# Provide an interface to add new employees
@app.route('/create', methods=['POST'])
def createEmployee():
    employeeData = request.get_json()
    employee = Employee(id=employeeData["id"], firstname=employeeData['firstname'], lastname=employeeData['lastname'])
    db.add(employee)
    db.commit()
    return {
    "Status": "Created!"
    }

if __name__=='__main__':
    app.run(debug=True)
