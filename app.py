from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func #avarage
from send_email import send_email

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

# in terminal to create the tables
# from app import db
# db.create_all()

class Collector(db.Model):
    __tablename__ = "collector"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    height = db.Column(db.Integer)

    def __init__(self, email_, height_):
        self.email = email_
        self.height = height_
    

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/success", methods=['POST'])
def success():
    if request.method =='POST':
        email = request.form["email_name"]
        height = request.form["height_name"]
        if db.session.query(Collector).filter(Collector.email == email).count() == 0:
            data = Collector(email,height)
            db.session.add(data)
            db.session.commit()
            avg = round(db.session.query(func.avg(Collector.height)).scalar(),1)
            count = db.session.query(Collector.height).count()
            send_email(email,height,avg,count)
            return render_template("success.html")
    return render_template("index.html", text="Email already exist!")


def main():
    app.debug=True
    app.run(port="5001")


if __name__ == '__main__':
    main()    




