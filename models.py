from extensions import db  

class Admin(db.Model):
    __tablename__ = 'admin_master'

    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    f_name = db.Column(db.String(50), nullable=False)
    l_name = db.Column(db.String(50), nullable=False)
    address = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    mobile = db.Column(db.String(18), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    sec_que = db.Column(db.String(50), nullable=False)
    sec_ans = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
from extensions import db

class Registration(db.Model):
    __tablename__ = 'registration'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10))
    dob = db.Column(db.Date)
    address = db.Column(db.Text)
    city = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    vehicle_type = db.Column(db.String(50))
    photo = db.Column(db.String(100))       
    signature = db.Column(db.String(100))   
    reg_date = db.Column(db.DateTime)
class Feedback(db.Model):
    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    message = db.Column(db.Text, nullable=False)
    submitted_at = db.Column(db.DateTime, default=db.func.current_timestamp())
