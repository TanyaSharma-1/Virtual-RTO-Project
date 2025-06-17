# 🚗 Virtual RTO Portal — Flask + MySQL Project

This is a complete Regional Transport Office (RTO) management system built using **Python Flask** and **MySQL** for the final semester project.

---

## 🔧 Tech Stack

- 🐍 Python 3.x
- 🌐 Flask (Backend Framework)
- 🗄️ MySQL + SQLAlchemy (ORM)
- 🧾 HTML5, Bootstrap 5 (UI)
- 📦 xhtml2pdf (for PDF result download)

---

## ✅ Features

| User Side | Admin Panel |
|-----------|-------------|
| 🚗 Vehicle Registration with photo & signature | 🔐 Admin login (secure session) |
| 💬 Submit feedback | 📋 View all registrations |
| 📊 Check RTO test result via email | 📥 Upload & view test results |
| 🧾 Download result as PDF | 📬 View submitted feedback |
| 📄 Download official RTO forms | 📁 Download forms (static) |

---
## 🔗 App Navigation Links (Localhost)

- 👤 [User Registration](http://localhost:5000/register)
- 🔐 [Admin Login](http://localhost:5000/login)
- 🧾 [Admin Dashboard](http://localhost:5000/dashboard)
- 📥 [Upload Test Result](http://localhost:5000/admin/upload-result)
- 📊 [Check Result & Download PDF](http://localhost:5000/check-result)
- 💬 [Feedback Form](http://localhost:5000/feedback)
- 📬 [View Feedbacks (Admin)](http://localhost:5000/admin/feedbacks)
- 👥 [View All Registrations](http://localhost:5000/admin/registrations)
- 📄 [Download RTO Forms](http://localhost:5000/download-forms)

## 🧪 How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/virtual-rto.git
cd virtual-rto

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # For Linux / macOS
# OR
venv\Scripts\activate      # For Windows

### 3. Install Dependencies
```bash
pip install -r requirements.txt

### 4. Start MySQL and Setup Database
```bash
-- Login to MySQL
mysql -u root -p

-- Then run:
CREATE DATABASE virtual_rto;
CREATE USER 'flaskuser'@'localhost' IDENTIFIED BY 'Flask123!';
GRANT ALL PRIVILEGES ON virtual_rto.* TO 'flaskuser'@'localhost';
FLUSH PRIVILEGES;
EXIT;

### 5. Run the Flask App
```bash
python app.py
http://localhost:5000


### 📂 Project Structure
```bash 
virtual-rto/
│
├── app.py                # Main Flask App
├── config.py             # DB + App Config
├── models.py             # SQLAlchemy Models
├── requirements.txt      # All dependencies
├── templates/            # HTML templates
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   └── ...
├── static/
│   ├── css/style.css
│   ├── uploads/          # Uploaded photos & signatures
│   └── forms/            # Downloadable forms
└── README.md
