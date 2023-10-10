from flask import Flask, render_template, flash, redirect, url_for, request, session
from flask_login import login_manager, LoginManager, login_user, logout_user, current_user, login_required
from models import * 
from form import *
from modules import send_email
from datetime import datetime, date
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["Hms_secret_key"]
app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://KEVINKAGWIMA/venus?driver=ODBC+Driver+11+for+SQL+Server"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://kevokagwima:Hunter1234@kevokagwima.mysql.pythonanywhere-services.com/kevokagwima$tickets"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = '/login'
login_manager.login_message = "Please login to access this page"
login_manager.login_message_category = "danger"
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  try:
    return Users.query.filter_by(id=user_id).first()
  except:
    flash("Failed to login the user", category="danger")

@app.before_request
def event_expiry():
  pass

@app.route("/register", methods=["POST", "GET"])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    new_user = Users(
      first_name = form.first_name.data,
      last_name = form.last_name.data,
      email = form.email_address.data,
      phone_number = form.phone_number.data,
      joining_code = form.referral_code.data,
      passwords = form.password.data,
    )
    db.session.add(new_user)
    db.session.commit()
    flash("Registration successfull", category="success")
    message = {
      'receiver': new_user.email,
      'subject': f"Account Creation",
      'body': f"Your account has been successfully created."
    }
    send_email(**message)
    return redirect(url_for('login'))
  
  if form.errors != {}:
    for err_msg in form.errors.values():
      flash(f"{err_msg}", category="danger")

  return render_template("register.html", form=form)

@app.route("/login", methods=["POST", "GET"])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = Users.query.filter_by(email=form.email_address.data).first()
    if user and user.check_password_correction(attempted_password=form.password.data):
      login_user(user, remember=True)
      flash("Login successfull", category="success")
      if current_user.status == "Active":
        return redirect(url_for("home"))
      else:
        return redirect(url_for('account_info'))
    elif user is None:
      flash("No user with that email", category="danger")
      return redirect(url_for('login'))
    else:
      flash("Invalid credentials", category="danger")
      return redirect(url_for('login'))
  return render_template("login.html", form=form)

@app.route("/account-info")
@login_required
def account_info():
  return render_template("info.html")

@app.route("/")
@app.route("/home")
@login_required
def home():
  users = Users.query.all()
  roles = Role.query.all()
  mpesa_codes = MpesaCode.query.all()
  return render_template("index.html", roles=roles, mpesa_codes=mpesa_codes, users=users)

@app.route("/invited_users/<int:referral_code>")
@login_required
def invited_users(referral_code):
  users = Users.query.filter_by(joining_code=referral_code).all()
  return render_template("invited-users.html", users=users)

@app.route("/verify-account", methods=["POST"])
@login_required
def verify_account():
  new_ref_code = MpesaCode(
    ref_code = request.form.get("ref-code"),
    user = current_user.id
  )
  db.session.add(new_ref_code)
  db.session.commit()
  flash("Activation request sent", category="success")
  return redirect(url_for('home'))

@app.route("/approve/<int:mpesa_id>")
def approve(mpesa_id):
  try:
    mpesa = MpesaCode.query.get(mpesa_id)
    user = Users.query.get(mpesa.user)
    user.status = "Active"
    db.session.delete(mpesa)
    db.session.commit()
    flash("Verification is approved", category="success")
    return redirect(url_for('home'))
  except:
    flash("An error occurred. Try again later", category="danger")
    return redirect(url_for('home'))

@app.route("/decline/<int:mpesa_id>")
def decline(mpesa_id):
  try:
    mpesa = MpesaCode.query.get(mpesa_id)
    db.session.delete(mpesa)
    db.session.commit()
    flash("Verification is declined", category="success")
    return redirect(url_for('home'))
  except:
    flash("An error occurred. Try again later", category="danger")
    return redirect(url_for('home'))

@app.route("/logout")
@login_required
def logout():
  logout_user()
  flash("Logout successfull", category="success")
  return redirect(url_for('login'))

if __name__ == "__main__":
  app.run(debug=True)
