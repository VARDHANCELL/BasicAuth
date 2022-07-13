from gettext import find
from colorama import Cursor
from flask import Flask, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
from functools import wraps
from user import User, ACCESS
import mysql.connector
app = Flask(__name__)

app.secret_key = 'your secret key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DB'] = 'pythonlogin'

mysql = MySQL(app)




@app.route('/pythonlogin', methods=['POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
    
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', [username, password])
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = username
            session['role'] = account['role']
            msg = 'Logged in successfully!'
        else:
          msg = 'Incorrect username/password!'
        return msg
    
@app.route('/logout/' , methods=['POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return "Logout successfully"



@app.route('/register', methods=['POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = %s', [email])
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        msg = 'Please fill out the form!'
    return msg

@app.route('/admin.panel', methods=['POST'])
def profile():
    print(session.get('role'))
    if not session.get('username'):
        return "session expired!"
    if session.get('role') != 'ADMIN':
        return "ACCESS DENIED"
    else:
        return "ACCESS Granted"

 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
app.run(debug=True,host='0.0.0.0', port=4000)