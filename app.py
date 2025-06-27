from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL
from config import db_config

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = db_config['host']
app.config['MYSQL_USER'] = db_config['user']
app.config['MYSQL_PASSWORD'] = db_config['password']
app.config['MYSQL_DB'] = db_config['database']

mysql = MySQL(app)

# Home Page - Show Registration Form
@app.route('/')
def index():
    return render_template('register.html')

# Handle Form Submission
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        course = request.form['course']
        address = request.form['address']

        # Insert data into DB
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO students (name, email, phone, course, address) VALUES (%s, %s, %s, %s, %s)",
                       (name, email, phone, course, address))
        mysql.connection.commit()
        cursor.close()

        return redirect('/students')

# View Registered Students
@app.route('/students')
def students():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM students")
    data = cursor.fetchall()
    cursor.close()
    return render_template('students.html', students=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
