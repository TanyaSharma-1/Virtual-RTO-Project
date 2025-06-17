from app import app, db
import models  # ensure your Admin model is in models.py

with app.app_context():
    db.create_all()
    print("Database tables created successfully.✅")
