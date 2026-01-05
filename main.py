#  INSTALL PACKAGES
from flask import Flask, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import InputRequired, Email, Length

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# loads .env into environment
load_dotenv()


MY_EMAIL = os.getenv("MY_EMAIL")
APP_PASSWORD = os.getenv("APP_PASSWORD")
FLASK_SECRET_KEY= os.getenv("FLASK_SECRET_KEY")

# CONFIGURE FLASK
app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY


def send_enquiry(name, sender_email, message):
    try:
        # Email setup
        subject = f"New message from {name}"
        body = f"""
        You have received a new message from your portfolio contact form.
        
        Name: {name}
        Email: {sender_email}
        
        Message:
        {message}
        """

        # Create a MIME message
        msg = MIMEMultipart()
        msg["From"] = MY_EMAIL
        msg["To"] = MY_EMAIL
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        # Connect to GMAIL SMTP
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=APP_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg=msg.as_string()
            )
        print("✅ Email sent successfully")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

@app.route('/')
def home():
    return render_template("welcome3.html")

@app.route('/profile')
def profile():
    return render_template("mywork.html")

class MyForm(FlaskForm):
    name = StringField('Name',  validators=[
        InputRequired(message="Please enter your name."),
        Length(min=2, max=50)
    ])
    email = StringField('Email',  validators=[
        InputRequired(message="Please enter your email."),
        Email(message="Please enter a valid email address.")
    ])
    message = TextAreaField('Message',  validators=[
        InputRequired(message="Please enter your message."),
        Length(min=5, max=1000)
    ])
    submit = SubmitField("Send Message")

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = MyForm()
    if form.validate_on_submit():
        send_enquiry(
            name = form.name.data,
            sender_email= form.email.data,
            message=form.message.data
        )
        flash("Your message has been sent successfully!", "success")
        return redirect(url_for('home'))
    return render_template("contact.html", form=form)






if __name__ == '__main__':
    app.run(debug=True)

