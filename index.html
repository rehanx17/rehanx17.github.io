from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Create SQLite database if it doesn't exist
def init_db():
    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()
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
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book_appointment():
    # Getting form data
    name = request.form['name']
    email = request.form['email']
    date = request.form['date']
    time = request.form['time']
    doctor = request.form['doctor']

    # Insert appointment into the database
    conn = sqlite3.connect('appointments.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO appointments (name, email, date, time, doctor)
        VALUES (?, ?, ?, ?, ?)
    ''', (name, email, date, time, doctor))
    conn.commit()
    conn.close()

    return redirect(url_for('thank_you'))

@app.route('/thank_you')
def thank_you():
    return '''
        <h1>Thank you for booking an appointment!</h1>
        <p>We have received your appointment request.</p>
    '''

if __name__ == '__main__':
    init_db()  # Initialize the database when the app starts
    app.run(debug=True)
