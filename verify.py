from authy.api import AuthyApiClient
from flask import (Flask, request, redirect, render_template, session, url_for, flash)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from forms import RegisterForm, LoginForm

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = app.config['SECRET_KEY']

db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = AuthyApiClient(app.config['AUTHY_API_KEY'])


@app.route("/phone_verification", methods=["GET", "POST"])
def phone_verification():
    if request.method == "POST":
        form = LoginForm()

        country_code = request.form.get("country_code")
        phone_number = request.form.get("phone_number")
        method = request.form.get("method")
        session['country_code'] = country_code
        session['phone_number'] = phone_number

        try:
            # fetch country code and phone from database and check against the entered data
            user = User.query.filter_by(phone_number=phone_number).first()
            if user.country_code == form.country_code.data:
                if user.phone_number == form.phone_number.data:
                    api.phones.verification_start(phone_number, country_code, via=method)
                    return redirect(url_for("verify"))
        except AttributeError:
            return render_template("phone_verification.html")

    return render_template("phone_verification.html")


@app.route("/verify", methods=["GET", "POST"])
def verify():
    if request.method == "POST":
        token = request.form.get("token")
        phone_number = session.get("phone_number")
        country_code = session.get("country_code")

        verification = api.phones.verification_check(phone_number, country_code, token)
        if verification.ok():
                return render_template("success.html")
    return render_template("verify.html")


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), unique=True)
    last_name = db.Column(db.String(80))
    phone_number = db.Column(db.String(11), unique=True)
    country_code = db.Column(db.String(11))
    password = db.Column(db.String(14))

    def __init__(self, first_name, last_name, phone_number, country_code, password):
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.country_code = country_code
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.first_name


@app.route('/', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            try:
                new_user = User(form.first_name.data, form.last_name.data, form.phone_number.data,
                                form.country_code.data, form.password.data)
                new_user.authenticated = True
                db.session.add(new_user)
                db.session.commit()
                return render_template("register_done.html")
            except IntegrityError:
                db.session.rollback()
                flash('ERROR! number ({}) already exists.'.format(form.phone_number.data), 'error')
    return render_template('register.html', form=form)


@app.route('/signout')
def sign_out():
    print(session.pop('country_code', 'phone_number'))
    return redirect(url_for('phone_verification'))


if __name__ == '__main__':
    app.run(debug=True)
