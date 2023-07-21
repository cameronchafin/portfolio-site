from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_mail import Mail, Message
import os
from dotenv import load_dotenv
import datetime

load_dotenv()

application = Flask(__name__)
year = datetime.date.today().year

# App & email configuration
application.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
application.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
application.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT'))
application.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS') == 'True'
application.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
application.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')

mail = Mail(application)


class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField("submit")


@application.route("/")
def index():
    return render_template('index.html', year=year)


@application.route("/about")
def about():
    return render_template('about.html', year=year)


@application.route("/projects")
def projects():
    return render_template('projects.html', year=year)


@application.route("/contact", methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        # Process the form data and send email
        msg = Message(subject=form.subject.data,
                      sender=app.config['MAIL_USERNAME'],
                      recipients=['cameronchafin.esl@gmail.com'])
        msg.body = f"From: {form.name.data}\nEmail: {form.email.data}\n\n{form.message.data}"
        mail.send(msg)

        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form, year=year)


@application.route("/resume")
def resume():
    return render_template('resume.html', year=year)


if __name__ == "__main__":
    application.run(debug=True)
