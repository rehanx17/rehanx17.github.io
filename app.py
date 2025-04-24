
from flask import Flask, render_template, request, redirect, send_file
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///submissions.db'
db = SQLAlchemy(app)

class ContactSubmission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))
    message = db.Column(db.Text)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['POST'])
def contact():
    name = request.form['name']
    email = request.form['email']
    message = request.form['message']
    new_submission = ContactSubmission(name=name, email=email, message=message)
    db.session.add(new_submission)
    db.session.commit()
    return redirect('/')

@app.route('/admin')
def admin():
    submissions = ContactSubmission.query.all()
    return render_template('admin.html', submissions=submissions)

@app.route('/export/excel')
def export_excel():
    submissions = ContactSubmission.query.all()
    data = [(s.id, s.name, s.email, s.message) for s in submissions]
    df = pd.DataFrame(data, columns=["ID", "Name", "Email", "Message"])
    file_path = "submissions.xlsx"
    df.to_excel(file_path, index=False)
    return send_file(file_path, as_attachment=True)

@app.route('/export/pdf')
def export_pdf():
    submissions = ContactSubmission.query.all()
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    y = 800
    for s in submissions:
        p.drawString(30, y, f"Name: {s.name}, Email: {s.email}, Message: {s.message}")
        y -= 20
        if y < 50:
            p.showPage()
            y = 800
    p.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="submissions.pdf")

if __name__ == '__main__':
    app.run(debug=True)
