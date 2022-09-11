from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

import mariadb
import json
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
import uuid

# Define the MariaDB engine using MariaDB Connector/Python
engine = sqlalchemy.create_engine("mariadb+mariadbconnector://test:12345@localhost:3306/librarycatalog")
db = sqlalchemy.orm.sessionmaker()
db.configure(bind=engine)
db = db()

if __name__=='__main__':
    app.run(debug=True)

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

# Provide a search function based on firstname parameters
# Example: http://localhost:5000/search?firstname=Diana
@app.route('/search', methods=['GET'])
def getEmployees():
    if request.args:
        firstnameValue = request.args.get("firstname")
        foundEmployees = db.query(Employee).filter_by(firstname=firstnameValue)
        output = []
        for employee in foundEmployees:
            currEmp = {}
            currEmp['First name']= employee.firstname
            currEmp['Last name']= employee.lastname
            currEmp['User ID']= employee.id
            output.append(currEmp)
        return jsonify(output)
    else:
        return {"message:" "Please provide a first name"}, 403



# API will reply with the provided parameters
@app.route('/param', methods=['GET'])
def search():
    args = request.args
    return jsonify(args)

# Provide an interface to add new employees
@app.route('/create', methods=['POST'])
def createEmployee():
    db.rollback()
    employeeData = request.get_json()
    employee = Employee(id=employeeData["id"], firstname=employeeData['firstname'], lastname=employeeData['lastname'])
    db.add(employee)
    db.commit()

    return {
    "Status": "Created!"
    }
