from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, BooleanField, StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
from autoservisas import models

MESSAGE_BAD_EMAIL = "Neteisingas El.pastas"


class RegistrationForm(FlaskForm):

    login = StringField('Vardas', [DataRequired()])
    e_mail = StringField('El.pastas', [DataRequired(), Email(MESSAGE_BAD_EMAIL)])
    password = PasswordField('Slaptazodis', [DataRequired()])
    confirmation = PasswordField('Pakartokite slaptazodi', [EqualTo('password', "Slaptazodis nesutampa")])
    submit = SubmitField('Registruotis')

    def check_login(self, login):
        new_user = models.User.query.filter_by(login=login.data).first()
        if new_user:
            raise ValidationError('Toks vartotojas jau egzistuoja')

    def check_email(self, e_mail):
        new_email = models.User.query.filter_by(e_mail=e_mail.data).first()
        if new_email:
            raise ValidationError('toks el.paštas jau egzistuoja')


class LoginForm(FlaskForm):
    e_mail = StringField('El.pastas', [DataRequired(), Email(MESSAGE_BAD_EMAIL)])
    password = PasswordField('Slaptazodis', [DataRequired()])
    remember = BooleanField('Prisiminti mane')
    submit = SubmitField('Prisijungti')
    
class ProfileForm(FlaskForm):
    login = StringField('Vardas', [DataRequired()])
    e_mail = StringField('El.paštas', [DataRequired(), Email(MESSAGE_BAD_EMAIL)])
    is_admin = BooleanField('Administratorius')
    submit = SubmitField('Atnaujinti')

    def check_login(self, login):
        new_user = models.User.query.filter_by(login=login.data).first()
        if new_user:
            raise ValidationError('Toks vartotojas jau egzistuoja')

    def check_email(self, e_mail):
        new_email = models.User.query.filter_by(e_mail=e_mail.data).first()
        if new_email:
            raise ValidationError('toks el.paštas jau egzistuoja')

