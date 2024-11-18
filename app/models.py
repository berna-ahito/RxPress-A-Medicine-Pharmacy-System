from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)  # 'user' or 'admin'

class MedicineList(db.Model):
    __tablename__ = 'medicine_list' 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    strength = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)

