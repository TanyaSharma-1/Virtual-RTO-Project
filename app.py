from flask import Flask, render_template, request, redirect, url_for, session
from extensions import db
import config
from sqlalchemy import text
from datetime import datetime
import os
from werkzeug.utils import secure_filename
from models import Admin, Registration, Feedback

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)

UPLOAD_FOLDER = os.path.join('static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def home():
    return "Virtual RTO Flask App is working and connected to MySQL!"


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Admin.query.filter_by(username=username, password=password).first()
        if user:
            session['admin_id'] = user.admin_id
            return redirect(url_for('dashboard'))
        else:
            error = 'Invalid username or password'
    return render_template('login.html', error=error)


@app.route('/dashboard')
def dashboard():
    if 'admin_id' in session:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session.pop('admin_id', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        dob = request.form['dob']
        address = request.form['address']
        city = request.form['city']
        phone = request.form['phone']
        email = request.form['email']
        vehicle_type = request.form['vehicle_type']

        photo_file = request.files['photo']
        signature_file = request.files['signature']

        photo_filename = secure_filename(photo_file.filename) if photo_file and allowed_file(photo_file.filename) else None
        signature_filename = secure_filename(signature_file.filename) if signature_file and allowed_file(signature_file.filename) else None

        if photo_filename:
            photo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
        if signature_filename:
            signature_file.save(os.path.join(app.config['UPLOAD_FOLDER'], signature_filename))

        reg = Registration(
            name=name,
            gender=gender,
            dob=dob,
            address=address,
            city=city,
            phone=phone,
            email=email,
            vehicle_type=vehicle_type,
            photo=photo_filename,
            signature=signature_filename,
            reg_date=datetime.now()
        )
        db.session.add(reg)
        db.session.commit()
        return "Registration successful!✅"
    return render_template('register.html')


@app.route('/admin/registrations')
def view_registrations():
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    users = Registration.query.all()
    return render_template('registrations.html', users=users)


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        new_feedback = Feedback(name=name, email=email, message=message)
        db.session.add(new_feedback)
        db.session.commit()
        return "Feedback submitted! Thank you.✅"
    return render_template('feedback.html')


@app.route('/admin/feedbacks')
def view_feedbacks():
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    feedbacks = Feedback.query.order_by(Feedback.submitted_at.desc()).all()
    return render_template('admin_feedbacks.html', feedbacks=feedbacks)


@app.route('/admin/upload-result', methods=['GET', 'POST'])
def upload_test_result():
    if 'admin_id' not in session:
        return redirect(url_for('login'))

    registrations = Registration.query.all()

    if request.method == 'POST':
        reg_id = request.form['reg_id']
        result_status = request.form['result']
        score = request.form['score']
        exam_date = request.form['exam_date']

        db.session.execute(
            text("INSERT INTO test_results (reg_id, result, score, exam_date) VALUES (:reg_id, :result, :score, :exam_date)"),
            {"reg_id": reg_id, "result": result_status, "score": score, "exam_date": exam_date}
        )
        db.session.commit()
        return "Result uploaded successfully!✅"

    return render_template('add_result.html', registrations=registrations)


@app.route('/check-result', methods=['GET', 'POST'])
def check_result():
    result_data = None
    error = None

    if request.method == 'POST':
        email = request.form['email']
        user = Registration.query.filter_by(email=email).first()
        if user:
            result = db.session.execute(
                text("SELECT * FROM test_results WHERE reg_id = :reg_id"),
                {"reg_id": user.id}
            ).fetchone()

            if result:
                result_data = {
                    'name': user.name,
                    'email': user.email,
                    'score': result.score,
                    'result': result.result,
                    'exam_date': result.exam_date
                }
            else:
                error = "⚠️ No test result found for this user."
        else:
            error = "⚠️ No user found with that email."
    return render_template('check_result.html', result=result_data, error=error)

from flask import make_response
from xhtml2pdf import pisa
from io import BytesIO
from jinja2 import Template

@app.route('/download-pdf/<email>')
def download_pdf(email):
    user = Registration.query.filter_by(email=email).first()
    if not user:
        return "User not found", 404

    result = db.session.execute(
        text("SELECT * FROM test_results WHERE reg_id = :reg_id"),
        {"reg_id": user.id}
    ).fetchone()

    if not result:
        return "Result not found", 404

    result_data = {
        'name': user.name,
        'email': user.email,
        'score': result.score,
        'result': result.result,
        'exam_date': result.exam_date
    }

    html = render_template('result_pdf.html', result=result_data)
    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(html, dest=pdf)

    if pisa_status.err:
        return "PDF generation failed", 500

    pdf.seek(0)
    response = make_response(pdf.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename={user.name}_result.pdf'
    return response


@app.route('/download-forms')
def download_forms():
    if 'admin_id' not in session:
        return redirect(url_for('login'))
    return render_template('download_forms.html')


if __name__ == '__main__':
    app.run(debug=True)
