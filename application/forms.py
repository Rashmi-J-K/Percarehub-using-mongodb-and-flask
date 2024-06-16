from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, TextAreaField, DateField, TimeField,PasswordField
from wtforms.validators import DataRequired,Length, EqualTo

class LoginForm(FlaskForm):
    empid = StringField('Employee ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class PetRegistrationForm(FlaskForm):
    pet_id = StringField('Pet ID', validators=[DataRequired()])
    name = StringField('Pet Name', validators=[DataRequired()])
    species = StringField('Species', validators=[DataRequired()])
    breed = StringField('Breed', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    submit = SubmitField('Register Pet')




class AppointmentForm(FlaskForm):
    appointment_id = StringField('Appointment ID', validators=[DataRequired()])
    pet_id = StringField('Pet ID', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Create Appointment')


class HealthRecordForm(FlaskForm):
    pet_id = StringField('Pet ID', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField('Add Health Record')

class NutritionForm(FlaskForm):
    pet_id = StringField('Pet ID', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    food_type = StringField('Food Type', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    submit = SubmitField('Add Nutrition Record')



class EditHealthRecordForm(FlaskForm):
    pet_id = StringField('Pet ID', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])

class EditNutritionForm(FlaskForm):
    pet_id = StringField('Pet ID', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    food_type = StringField('Food Type', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])


class ContactForm(FlaskForm):
    contact_id = StringField('Contact ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    submit = SubmitField('Submit')