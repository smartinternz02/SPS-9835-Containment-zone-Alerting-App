# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 16:54:58 2021

@author: 91980
"""
from flask import Flask , render_template, request, redirect, url_for
from flask_mysqldb import MySQL
import MySQLdb.cursors
import sys
import json
import flask

app = Flask(__name__)
app.config['MYSQL_HOST'] = "remotemysql.com"
app.config['MYSQL_USER'] = "kypqAMEvgU"
app.config['MYSQL_PASSWORD'] ="eDnJvR1JS4"
app.config['MYSQL_DB'] = "kypqAMEvgU"

mysql = MySQL(app)
app.secret_key="abc"


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/login',methods=["POST"])
def login():
    
    if request.method == "POST":
        name = request.form['uname']
        password = request.form['pass']
        #cursor = mysql.connection.cursor()
        #cursor.execute("select * from admin")
        if name=='Krish' and password == 'qwert':
            return redirect(url_for('success'))
        else:
            return "TRY AGAIN"
        
@app.route('/success')
def success():
    return render_template("suc.html")

@app.route('/register', methods =["POST"])
def register():
    msg = ''
    abcd = "Zone updated succesfully"
    if request.method == 'POST':
        zone_name = request.form['zone_name']
        latitude = request.form['latitude']
        longitude = request.form['longitude']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cursor.execute('SELECT * FROM zoneupdate WHERE zone_name = % s', (zone_name, ))
        #account = cursor.fetchone()
        #if account:
           # msg = 'Account already exists !'
        # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        #     msg = 'Invalid email address !'
        # elif not re.match(r'[A-Za-z0-9]+', username):
        #     msg = 'Username must contain only characters and numbers !'
        # elif not username or not password or not email:
        #     msg = 'Please fill out the form !'
        #cursor.execute('INSERT INTO dummy VALUES ( % s, % s, % s)', (zone_name, latitude, longitude ))
        insert_query1 = "INSERT INTO dummy (zone_name, latitude, longitude) VALUES (%s, %s, %s)"
        insert_values1 = (zone_name, latitude, longitude)
        cursor.execute(insert_query1, insert_values1)
        mysql.connection.commit()
        msg = 'You have successfully registered !'
    # elif request.method == 'POST':
    #     msg = 'Please fill out the form !'
    return abcd
        
        
        #datas=cursor.fetchall()
    #return render_template("suc.html")
@app.route('/registerUsers', methods =["GET","POST"])
def connection():
    msg_received = flask.request.get_json()
    msg_subject = msg_received["subject"]
    if msg_subject == "registerUsers":
        return registerUsers(msg_received)
    elif msg_subject == "loginUsers":
        return loginUsers(msg_received)
    else:
        return "Invalid request."
   
def registerUsers(msg_received):
    firstname = msg_received["firstname"]
    lastname = msg_received["lastname"]
    username = msg_received["username"]
    password = msg_received["password"]

    select_query = "SELECT * FROM users where username = " + "'" + username + "'"
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(select_query)
    records = cursor.fetchall()
    if len(records) != 0:
        return "Another user used the username. Please chose another username."

    insert_query = "INSERT INTO users (firstname, lastname, username, password) VALUES (%s, %s, %s, %s)"
    insert_values = (firstname, lastname, username, password)
    try:
        cursor.execute(insert_query, insert_values)
        mysql.connection.commit()
        return "success"
    except Exception as e:
        print("Error while inserting the new record :", repr(e))
        return "failure"

def loginUsers(msg_received):
    username = msg_received["username"]
    password = msg_received["password"]
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    select_query = "SELECT firstname, lastname FROM users where username = " + "'" + username + "' and password = " + "'" + password + "'"
    cursor.execute(select_query)
    records = cursor.fetchall()

    if len(records) == 0:
        return "failure"
    else:
        return "success"
    

@app.route('/getloc', methods =["GET","POST"])
def getloc():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    select_query = "SELECT latitude,longitude FROM dummy ORDER BY Id DESC LIMIT 1"
    cursor.execute(select_query)
    records = cursor.fetchall()
    #print(records)
    lat1=records[0]['latitude']
    lat2=records[0]['longitude']
    print(lat1,lat2)
    return(lat1+lat2)
        


    


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080,debug=True)
    