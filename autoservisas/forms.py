from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField, IntegerField, SelectField, FloatField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Length, NumberRange
from autoservisas import models

MESSAGE_BAD_EMAIL = "Neteisingas El.pastas"

def car_query():
    return models.Car.query.filter_by(user_id=models.current_user.id)
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
    submit = SubmitField('Atnaujinti')

    def check_login(self, login):
        new_user = models.User.query.filter_by(login=login.data).first()
        if new_user:
            raise ValidationError('Toks vartotojas jau egzistuoja')

    def check_email(self, e_mail):
        new_email = models.User.query.filter_by(e_mail=e_mail.data).first()
        if new_email:
            raise ValidationError('toks el.paštas jau egzistuoja')

class CarForm(FlaskForm):
    make = StringField('Marke', [DataRequired()])
    model = StringField('Modelis', [DataRequired()])
    year = IntegerField('Pagaminimo metai', [DataRequired(), NumberRange(min=1908, max=2023, message='neteisingai ivesti pagaminimo metai')])
    # year = SelectField('Pagaminimo metai', [DataRequired()], choices=list(range(2000, 2023)))
    engine = SelectField('Variklio tipas', [DataRequired()], choices=['benzinas', 'dyzelis', 'benzinas/dujos', 'benzinas/elektra', 'elektra'])
    registration = StringField('Valstybinis numeris', [DataRequired(), Length(min=1, max=6, message='netinkamas simboliu skaicius')])
    vin = StringField('VIN', [DataRequired(), Length(min=11, max=17, message='netinkamas simboliu skaicius')])
    submit = SubmitField('Issaugoti')

class DefectForm:
    description = StringField('Gedimo aprasymas', [DataRequired()])
    car_id = QuerySelectField(
        query_factory=car_query, 
        allow_blank=False, 
        get_label=lambda obj: str(f'{obj.make} {obj.model} {obj.registration}'), 
        get_pk=lambda obj: str(obj)
    )
    status = SelectField('Busena', [DataRequired()], choices=["priimtas", "remontuojamas", "laukiame detalių", "įvykdytas", "atiduotas"])
    price = FloatField('Kaina')
    submit = SubmitField('Issaugoti')

