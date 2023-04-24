from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['MYSQL_HOST'] = '54.174.186.23'
app.config['MYSQL_USER'] = 'support'
app.config['MYSQL_PASSWORD'] = '0i160t47'
app.config['MYSQL_DB'] = 'flaskusers'
mysql = MySQL(app)

app.secret_key = 'mysecretkey'

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data=cur.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST': 
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        dni = request.form['dni']
        cur = mysql.connection.cursor() 
        cur.execute('INSERT INTO contacts (nombre, apellido, correo, direccion, telefono,dni) VALUES (%s, %s, %s, %s, %d, %d)', 
        (nombre, apellido, correo, direccion, telefono, dni))
        mysql.connection.commit()
        flash('Contact Added Succesfully')
        return redirect(url_for('Index'))

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        dni = request.form['dni']
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE contacts
        SET nombre = %s,
            apellido = %s,
            correo = %s,
            direccion = %s,
            telefono = %d,
            dni = %d
        WHERE id = %s
        """, (nombre, apellido, correo, direccion, telefono, dni,id ))
        mysql.connection.commit()
        flash('Contact updated successfully')
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contact Removed Successfully')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)
