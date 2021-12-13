# Add to this file for the sample app lab
from flask import Flask, url_for, redirect, jsonify, request
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json, os
import sqlite3 as sql
from datetime import datetime
from sqlalchemy import text

user = None


webApp = Flask(__name__)
webApp.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Customer.sqlite'
webApp.config['SQLALCHEMY_TRACK_MODIFICATION'] = True
db = SQLAlchemy(webApp)
ma = Marshmallow(webApp)

class Customer(db.Model):
    __tablename__ = "customer"
    customer_id = db.Column(db.String(50), primary_key=True)
    customer_name = db.Column(db.String(50))
    customer_email = db.Column(db.String(50))
    customer_password = db.Column(db.String(50))

    def __init__(self, customer_id, customer_name, customer_email, customer_password):
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.customer_email = customer_email
        self.customer_password = customer_password
        

class CustomerSchema(ma.Schema):
    class Meta:
        fields = ("customer_id", "customer_name" , "customer_email", "customer_password")

customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)

@webApp.route("/")
def main():
    if(user is None):
        return redirect(url_for("test"))
    else:
        return redirect(url_for("home"))

@webApp.route('/test', methods=['GET'])
def test():
    global user
    if(user is None):
        return render_template('test.html')
    else:
        user = None
        return render_template('test.html')

@webApp.route("/home")
def home():
    global user
    if(user is None):
        return redirect(url_for("test"))
    else:
        return render_template('index.html', user=user)

@webApp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        email = data[0]["email"]
        password = data[0]["password"]

        global user
        customer = Customer.query.filter_by(customer_email=email).first()
        user = customer_schema.dump(customer)
    
        message = ""
    
        if(len(user)>0):
            if (user['customer_password'] == password):
                #return redirect(url_for("home")) 
                message = {'message':"Welcome"}

            else:
                user = None
                message = {'message':"Incorrect Email or Password"}
                #return redirect(url_for("test"))
        else:
            user = None
            message = {'message':"There is no email registered"}
            #return redirect(url_for("test"))
        
    return jsonify(message)

@webApp.route('/aboutus', methods=['GET', 'POST'])
def aboutus():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return redirect(url_for('main'))

    # show the form, it wasn't submitted
    return render_template('aboutus.html')

@webApp.route('/register')
def register():
    # show the form, it wasn't submitted
    return render_template('regpage.html')

@webApp.route('/createdAcc', methods=['GET', 'POST'])
def createdAcc():
    if request.method == 'POST':
        data = request.get_json()
        #print(data)
        
        customer_id = datetime.now().strftime("%Y%m%d%H%M%S")
        customer_name = data[0]['name']
        customer_email = data[0]['email']
        customer_password = data[0]['password']

        check_email = Customer.query.filter_by(customer_email=customer_email).first()
        existing_email = customer_schema.dump(check_email)
        #print(len(existing_email))
        if len(existing_email) > 0:
            message = {'message':"Email is already used"}

        else:
            new_customer = Customer(customer_id, customer_name, customer_email, customer_password)
            db.session.add(new_customer)
            db.session.commit()

            message = {'message':"Successfully Registered"}
        
        return jsonify(message)

@webApp.route('/customers', methods=['GET'])
def customers():
    global user
    if(user is None):
        return redirect(url_for("test"))
    else:
        customers = Customer.query.all()
        result = customers_schema.dump(customers)
        #print(result)
        
        return render_template('customers.html', rows=result, user=user)

    

@webApp.route('/customers/<customer_id>', methods=['GET'])
def read_customer(customer_id):
    result = []
    customer = Customer.query.get(customer_id)
    result.append(customer_schema.dump(customer))
    #print(result)
    #customer_schema.jsonify(result)
    global user
    return render_template('customers.html', rows=result, user=user)


@webApp.route('/customers/delete/<customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    if request.method == 'DELETE':
        customer = Customer.query.get(customer_id)
        db.session.delete(customer)
        db.session.commit()

        customers = Customer.query.all()
        result = customers_schema.dump(customers)
        #print(result)
    global user
    return render_template('customers.html', rows=result, user=user)


@webApp.route('/update/<customer_id>', methods=['GET', 'PUT'])
def updatePage(customer_id):
    global user
    return render_template('updateCustomer.html', user=user)

@webApp.route('/updated/<customer_id>', methods=['GET', 'PUT'])
def update_customer(customer_id):
    global user
    if request.method == 'PUT':
        customer = Customer.query.get(customer_id)
        data = request.get_json()

        name = data[0]['name']
        email = data[0]['email']
        password = data[0]['password']

        check_email = Customer.query.filter_by(customer_email=email).first()
        existing_email = customer_schema.dump(check_email)

        if user['customer_email'] == email:
            customer.customer_name = name
            customer.customer_email = email
            customer.customer_password = password


            db.session.commit()

            customers = Customer.query.all()
            result = customers_schema.dump(customers)

            message = {'message':"User Updated"}
        else:
            if len(existing_email) > 0:
                message = {'message':"Email is already used"}
            else:
                customer.customer_name = name
                customer.customer_email = email
                customer.customer_password = password

                db.session.commit()

                customers = Customer.query.all()
                result = customers_schema.dump(customers)

                message = {'message':"User Updated"}

        return jsonify(message)
    


if __name__ == "__main__":
    db.create_all()
    webApp.run(host="0.0.0.0", port=8080, debug=True)
