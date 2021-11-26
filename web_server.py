# Add to this file for the sample app lab
from flask import Flask, url_for, redirect, jsonify, request
from flask import request
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json, os
import sqlite3 as sql
from datetime import datetime

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
        # show the form, it wasn't submitted
        return render_template('test.html')
    else:
        user = None
        return render_template('test.html')

@webApp.route("/home")
def home():
    return render_template('index.html')

@webApp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form["email_login"]
        password = request.form["pass_login"]

        con = sql.connect("Customer.sqlite")
        con.row_factory = sql.Row

        cur = con.cursor()

        cur.execute("select * from customer where customer_email='{}' and customer_password='{}';".format(email, password))

        global user
        user = cur.fetchone()

        if (user is None):
            return render_template("test.html")
        else:
            if (len(user) > 0):
                return redirect(url_for("home"))
            

    return render_template("test.html")

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
        customer_id = datetime.now().strftime("%Y%m%d%H%M%S")
        customer_name = request.form["name_signup"]
        customer_email = request.form['email_signup']
        customer_password = request.form['password_signup']
        new_customer = Customer(customer_id, customer_name, customer_email, customer_password)
        db.session.add(new_customer)
        db.session.commit()
        
        return redirect(url_for('test'))

@webApp.route('/customers', methods=['GET'])
def customers():
    customers = Customer.query.all()
    result = customers_schema.dump(customers)
    #print(result)
    return render_template('customers.html', rows=result)

@webApp.route('/customers/<customer_id>', methods=['GET'])
def read_customer(customer_id):
    result = []
    customer = Customer.query.get(customer_id)
    result.append(customer_schema.dump(customer))
    #print(result)
    #customer_schema.jsonify(result)
    return render_template('customers.html', rows=result)


@webApp.route('/customers/delete/<customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    customer = Customer.query.get(customer_id)
    db.session.delete(customer)
    db.session.commit()

    customers = Customer.query.all()
    result = customers_schema.dump(customers)
    #print(result)
    return render_template('customers.html', rows=result)


@webApp.route('/customers/update')
def updatePage():
    # show the form, it wasn't submitted
    return render_template('updateCustomer.html')

@webApp.route('/update', methods=['GET', 'POST'])
def update_customer():
    if request.method == 'POST':
        customer_id = request.form['id_update']
        name = request.form['name_update']
        email = request.form['email_update']
        password = request.form['password_update']

        con = sql.connect("Customer.sqlite")
        con.execute("UPDATE customer set customer_name='{}', customer_email='{}', customer_password='{}' where customer_id='{}';".format(name, email, password, customer_id))
        con.commit()
        con.close()

        customers = Customer.query.all()
        result = customers_schema.dump(customers)
        #print(result)
        return render_template('customers.html', rows=result)

    elif request.method == 'GET':
        return render_template('updateCustomer.html')
    


if __name__ == "__main__":
    webApp.run(host="0.0.0.0", port=8080, debug=True)
