from datetime import datetime
from flask import redirect, request, render_template, flash, url_for
from flask_bcrypt import Bcrypt
from flask_login import logout_user, login_user, login_required, current_user

from autoservisas.models import User, LimitedAdmin
from autoservisas import forms
from autoservisas import app, db, admin


admin.add_view(LimitedAdmin(User, db.session))
bcrypt = Bcrypt(app)


@app.route("/admin")
@login_required
def admin():
    return redirect(url_for(admin))


@app.route('/')
def home():
    flash('Sveiki atvyke i autoservisas.net sistema!', 'info')
    return render_template('base.html', current_user=current_user)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if current_user.is_authenticated:
        flash('Logout, kad sukurti nauja vartotoja')
        return redirect(url_for('home'))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        hidden_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(
            login = form.login.data,
            e_mail = form.e_mail.data,
            password = hidden_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Sėkmingai prisiregistravote! Galite prisijungti.', 'success')
        return redirect(url_for('home'))
    return render_template('registration.html', form=form, current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    next_page = request.args.get('next')
    if current_user.is_authenticated:
        flash('Vartotojas jau prisijunges. Atsijunkite, kad prijungti kita')
        return redirect(next_page) if next_page else redirect(url_for('home'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(e_mail=form.e_mail.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Prisijungti nepavyko', 'danger')
    return render_template('login.html', form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    next_page = request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('home'))

