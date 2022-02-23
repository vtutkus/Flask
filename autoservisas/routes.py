from datetime import datetime
from flask import redirect, request, render_template, flash, url_for
from flask_bcrypt import Bcrypt
from flask_login import logout_user, login_user, login_required, current_user

from autoservisas.models import User, Car, Defect, LimitedAdmin
from autoservisas import forms
from autoservisas import app, db, admin


admin.add_view(LimitedAdmin(User, db.session))
admin.add_view(LimitedAdmin(Car, db.session))
admin.add_view(LimitedAdmin(Defect, db.session))
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
        is_first_user = not User.query.first()
        new_user = User(
            login = form.login.data,
            e_mail = form.e_mail.data,
            password = hidden_password,
            is_admin = is_first_user,
            is_worker = is_first_user
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


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = forms.ProfileForm()
    if form.validate_on_submit():
        current_user.login = form.login.data
        current_user.e_mail = form.e_mail.data
        db.session.commit()
        flash('Profilis atnaujintas!', 'success')
        return redirect(url_for('profile'))
    elif request.method == "GET":
        form.login.data = current_user.login
        form.e_mail.data = current_user.e_mail
    return render_template('profile.html', current_user=current_user, form=form)

@app.route('/cars', methods=['GET', 'POST'])
@login_required
def cars():
    try:
        all_my_cars = Car.query.filter_by(user_id=current_user.id).all()
    except:
        all_my_cars = []
    return render_template("cars.html", all_my_cars=all_my_cars)

@app.route("/new_car", methods=["GET", "POST"])
def new_car():
    form = forms.CarForm()
    if form.validate_on_submit():
        new_car = Car(
            make = form.make.data,
            model = form.model.data,
            year = form.year.data,
            engine = form.engine.data,
            registration = form.registration.data,
            vin = form.vin.data,
            user_id = current_user.id
        )
        db.session.add(new_car)
        db.session.commit()
        return redirect(url_for('cars'))
    return render_template("car_form.html", form=form)


@app.route("/redaguojamas_tevas/<int:id>", methods=["GET", "POST"])
def edit_parent(id):
    form = forms.TevasForm()
    try:
        tevas = Tevas.query.get(id)
    except:
        return redirect(url_for('parents'))
    if form.validate_on_submit():
        tevas.vardas = form.vardas.data
        tevas.pavarde = form.pavarde.data
        if hasattr(form.vaikas.data, 'id'):
            tevas.vaikas_id = form.vaikas.data.id
        else:
            tevas.vaikas_id = None
        db.session.commit()
        return redirect(url_for('parents'))
    return render_template("tevas_form.html", form=form, tevas=tevas)

@app.route("/trinamas_tevas/<int:id>")
def delete_parent(id):
    try:
        tevas = Tevas.query.get(id)
    except:
        return redirect(url_for('parents'))
    db.session.delete(tevas)
    db.session.commit()
    return redirect(url_for('parents'))

@app.route('/defects', methods=['GET', 'POST'])
@login_required
def defects():
    try:
        all_defects = Defect.query.all()
    except:
        all_defects = []
    return render_template("defects.html", all_defects=all_defects)

@app.route('/logout')
def logout():
    logout_user()
    next_page = request.args.get('next')
    return redirect(next_page) if next_page else redirect(url_for('home'))

