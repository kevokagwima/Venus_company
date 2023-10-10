from flask import Flask
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mssql+pyodbc://KEVINKAGWIMA/venus?driver=ODBC+Driver+11+for+SQL+Server"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://kevokagwima:Hunter1234@kevokagwima.mysql.pythonanywhere-services.com/kevokagwima$tickets"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db.init_app(app)

def main():
  db.create_all()

def add_role():
  new_role = Role(
    role_name = "Normal"
  )
  db.session.add(new_role)
  db.session.commit()
  print(f"Added role {new_role.role_name}")

if __name__ == '__main__':
  with app.app_context():
    main()
