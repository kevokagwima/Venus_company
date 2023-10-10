from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import UserMixin
import random

db = SQLAlchemy()
bcrypt = Bcrypt()

class Role(db.Model):
  __tablename__ = "Roles"
  id = db.Column(db.Integer(), primary_key=True)
  role_name = db.Column(db.String(10), nullable=False)
  user = db.relationship("Users", backref="user-role", lazy=True)

class Users(db.Model, UserMixin):
  __tablename__ = "Users"
  id = db.Column(db.Integer(), primary_key=True)
  unique_id = db.Column(db.Integer(), nullable=False, default=random.randint(100000,999999))
  referral_code = db.Column(db.Integer(), nullable=False, default=random.randint(100000000,999999999))
  joining_code = db.Column(db.Integer(), nullable=True)
  first_name = db.Column(db.String(50), nullable=False)
  last_name = db.Column(db.String(50), nullable=False)
  email = db.Column(db.String(100), nullable=False)
  phone_number= db.Column(db.String(10), nullable=False)
  password = db.Column(db.String(100), nullable=False)
  status = db.Column(db.String(10), default="Pending")
  role = db.Column(db.Integer(), db.ForeignKey('Roles.id'), default=2)
  mpesa_code = db.Relationship("MpesaCode", backref="user-mpesa-code", lazy=True)

  @property
  def passwords(self):
    return self.passwords

  @passwords.setter
  def passwords(self, plain_text_password):
    self.password = bcrypt.generate_password_hash(plain_text_password).decode("utf-8")

  def check_password_correction(self, attempted_password):
    return bcrypt.check_password_hash(self.password, attempted_password)

class MpesaCode(db.Model):
  __tablename__ = "Mpesa_code"
  id = db.Column(db.Integer(), primary_key=True)
  ref_code = db.Column(db.String(10), nullable=False)
  status = db.Column(db.String(10), default="Pending")
  user = db.Column(db.Integer(), db.ForeignKey("Users.id"))
