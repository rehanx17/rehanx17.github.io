from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()

    # Table for appointments
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            doctor TEXT NOT NULL
        )
    ''')

    # Table for doctors
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS doctors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')

    # Insert sample doctors if table is empty
    cursor.execute('SELECT COUNT(*) FROM doctors')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('INSERT INTO doctors (name) VALUES (?)', [
            ("Dr. Smith",), ("Dr. Johnson",), ("Dr. Lee",)
        ])

    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM doctors')
    doctors = cursor.fetchall()
    conn.close()
    return render_template('index.html', doctors=[d[0] for d in doctors])

@app.route('/book', methods=['POST'])
def book_appointment():
    name = request.form['name']
    email = request.form['email']
    date = request.form['date']
    time = request.form['time']
    doctor = request.form['doctor']

    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO appointments (name, email, date, time, doctor)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, email, date, time, doctor))
    conn.commit()
    conn.close()

    return render_template('thank_you.html', name=name, doctor=doctor, date=date, time=time)

@app.route('/appointments')
def view_appointments():
    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM appointments ORDER BY date, time')
    appointments = cursor.fetchall()
    conn.close()
    return render_template('appointments.html', appointments=appointments)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
