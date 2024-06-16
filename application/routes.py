from flask import render_template, request, redirect, flash, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from application import app, db
from .forms import LoginForm, ContactForm, PetRegistrationForm, AppointmentForm, HealthRecordForm, NutritionForm
from .models import User
from datetime import datetime
from bson import ObjectId

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        empid = form.empid.data
        password = form.password.data
        user = db.login.find_one({"empid": empid})
        if user and check_password_hash(user['password'], password):
            user_obj = User(str(user['_id']), user['empid'], user['password'])
            login_user(user_obj)
            flash('Login successful', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials', 'danger')
    return render_template('login.html', form=form)



@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully', 'success')
    return redirect(url_for('login'))

@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')

@app.route('/submit_contact_form', methods=['POST'])
def submit_contact_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        
        # Process the form data, e.g., save it to a database or send an email
        
        # For now, let's just print the data to the console
        print(f"Name: {name}, Email: {email}, Message: {message}")
        
        # Redirect the user to a thank you page
        return render_template('thank_you.html')



@app.route('/view_hub')
@login_required
def view_hub():
    return render_template('view_hub.html')

@app.route('/pet/register', methods=['POST', 'GET'])
@login_required
def pet_register():
    form = PetRegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        pet_id = form.pet_id.data
        name = form.name.data
        species = form.species.data
        breed = form.breed.data
        age = form.age.data
        owner_id = current_user.get_id()
        db.pets.insert_one({"pet_id": pet_id, "name": name, "species": species, "breed": breed, "age": age, "owner_id": owner_id})
        flash('Pet registration successful', 'success')
        return redirect(url_for('view_pets'))
    return render_template('pet_register.html', form=form)

@app.route('/pets')
@login_required
def view_pets():
    pets = db.pets.find({"owner_id": current_user.get_id()})
    return render_template('view_pets.html', pets=pets)

@app.route('/pet/edit/<pet_id>', methods=['POST', 'GET'])
@login_required
def edit_pet(pet_id):
    pet = db.pets.find_one({"_id": ObjectId(pet_id)})
    if not pet:
        abort(404)

    form = PetRegistrationForm(data=pet)
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        breed = form.breed.data
        age = form.age.data
        db.pets.update_one(
            {"_id": ObjectId(pet_id)},
            {"$set": {"name": name, "species": species, "breed": breed, "age": age}}
        )
        flash('Pet updated successfully', 'success')
        return redirect(url_for('view_pets'))

    return render_template('edit_pet.html', form=form, pet=pet)

@app.route('/pet/delete/<pet_id>', methods=['POST'])
@login_required
def delete_pet(pet_id):
    db.pets.delete_one({"_id": ObjectId(pet_id)})
    flash('Pet deleted successfully', 'success')
    return redirect(url_for('view_pets'))

@app.route('/appointment/create', methods=['POST', 'GET'])
@login_required
def create_appointment():
    form = AppointmentForm()
    if request.method == 'POST' and form.validate_on_submit():
        appointment_id = form.appointment_id.data
        pet_id = form.pet_id.data
        date = datetime.combine(form.date.data, datetime.min.time())  # Convert date to datetime
        description = form.description.data
        owner_id = current_user.get_id()
        db.appointments.insert_one({"appointment_id": appointment_id, "pet_id": pet_id, "date": date, "description": description, "owner_id": owner_id})
        flash('Appointment created successfully', 'success')
        return redirect(url_for('view_appointments'))
    else:
        print(form.errors)  # Debugging: Print form errors if validation fails
    return render_template('create_appointment.html', form=form)

@app.route('/appointments')
@login_required
def view_appointments():
    appointments = db.appointments.find({"owner_id": current_user.get_id()})
    return render_template('view_appointments.html', appointments=appointments)

@app.route('/appointment/edit/<appointment_id>', methods=['POST', 'GET'])
@login_required
def edit_appointment(appointment_id):
    appointment = db.appointments.find_one({"_id": ObjectId(appointment_id)})
    if not appointment:
        abort(404)

    form = AppointmentForm(data=appointment)
    if request.method == 'POST' and form.validate_on_submit():
        pet_id = form.pet_id.data
        date = datetime.combine(form.date.data, datetime.min.time())  # Convert date to datetime
        description = form.description.data
        db.appointments.update_one(
            {"_id": ObjectId(appointment_id)},
            {"$set": {"pet_id": pet_id, "date": date, "description": description}}
        )
        flash('Appointment updated successfully', 'success')
        return redirect(url_for('view_appointments'))

    return render_template('edit_appointment.html', form=form, appointment=appointment)

@app.route('/appointment/delete/<appointment_id>', methods=['POST'])
@login_required
def delete_appointment(appointment_id):
    db.appointments.delete_one({"_id": ObjectId(appointment_id)})
    flash('Appointment deleted successfully', 'success')
    return redirect(url_for('view_appointments'))

@app.route('/health_record/add', methods=['POST', 'GET'])
@login_required
def add_health_record():
    form = HealthRecordForm()
    if request.method == 'POST' and form.validate_on_submit():
        pet_id = form.pet_id.data
        date = datetime.combine(form.date.data, datetime.min.time())  # Convert date to datetime
        description = form.description.data
        db.health_records.insert_one({"pet_id": pet_id, "date": date, "description": description})
        flash('Health record added successfully', 'success')
        return redirect(url_for('view_health_records'))
    return render_template('add_health_record.html', form=form)

@app.route('/health_records')
@login_required
def view_health_records():
    health_records = db.health_records.find()
    return render_template('view_health_records.html', health_records=health_records)

@app.route('/health_record/edit/<record_id>', methods=['POST', 'GET'])
@login_required
def edit_health_record(record_id):
    record = db.health_records.find_one({"_id": ObjectId(record_id)})
    if not record:
        abort(404)

    form = HealthRecordForm(data=record)
    if request.method == 'POST' and form.validate_on_submit():
        pet_id = form.pet_id.data
        date = datetime.combine(form.date.data, datetime.min.time())  # Convert date to datetime
        description = form.description.data
        db.health_records.update_one(
            {"_id": ObjectId(record_id)},
            {"$set": {"pet_id": pet_id, "date": date, "description": description}}
        )
        flash('Health record updated successfully', 'success')
        return redirect(url_for('view_health_records'))

    return render_template('edit_health_record.html', form=form, record=record)

@app.route('/health_record/delete/<record_id>', methods=['POST'])
@login_required
def delete_health_record(record_id):
    db.health_records.delete_one({"_id": ObjectId(record_id)})
    flash('Health record deleted successfully', 'success')
    return redirect(url_for('view_health_records'))

@app.route('/nutrition/add', methods=['POST', 'GET'])
@login_required
def add_nutrition_record():
    form = NutritionForm()
    if request.method == 'POST' and form.validate_on_submit():
        pet_id = form.pet_id.data
        date = datetime.combine(form.date.data, datetime.min.time())  # Convert date to datetime
        food_type = form.food_type.data
        quantity = form.quantity.data
        db.nutrition_records.insert_one({"pet_id": pet_id, "date": date, "food_type": food_type, "quantity": quantity})
        flash('Nutrition record added successfully', 'success')
        return redirect(url_for('view_nutrition_records'))
    return render_template('add_nutrition_record.html', form=form)

@app.route('/nutrition_records')
@login_required
def view_nutrition_records():
    nutrition_records = db.nutrition_records.find()
    return render_template('view_nutrition_records.html', nutrition_records=nutrition_records)

@app.route('/nutrition/edit/<record_id>', methods=['POST', 'GET'])
@login_required
def edit_nutrition_record(record_id):
    record = db.nutrition_records.find_one({"_id": ObjectId(record_id)})
    if not record:
        abort(404)

    form = NutritionForm(data=record)
    if request.method == 'POST' and form.validate_on_submit():
        pet_id = form.pet_id.data
        date = datetime.combine(form.date.data, datetime.min.time())  # Convert date to datetime
        food_type = form.food_type.data
        quantity = form.quantity.data
        db.nutrition_records.update_one(
            {"_id": ObjectId(record_id)},
            {"$set": {"pet_id": pet_id, "date": date, "food_type": food_type, "quantity": quantity}}
        )
        flash('Nutrition record updated successfully', 'success')
        return redirect(url_for('view_nutrition_records'))

    return render_template('edit_nutrition_record.html', form=form, record=record)

@app.route('/nutrition/delete/<record_id>', methods=['POST'])
@login_required
def delete_nutrition_record(record_id):
    db.nutrition_records.delete_one({"_id": ObjectId(record_id)})
    flash('Nutrition record deleted successfully', 'success')
    return redirect(url_for('view_nutrition_records'))



@app.route('/contact/add', methods=['POST', 'GET'])
@login_required
def add_contact():
    form = ContactForm()
    if request.method == 'POST' and form.validate_on_submit():
        contact_id = form.contact_id.data
        name = form.name.data
        phone = form.phone.data
        email = form.email.data
        address = form.address.data
        owner_id = current_user.get_id()
        db.contacts.insert_one({"contact_id": contact_id, "name": name, "phone": phone, "email": email, "address": address, "owner_id": owner_id})
        flash('Contact added successfully', 'success')
        return redirect(url_for('view_contacts'))
    return render_template('add_contact.html', form=form)

@app.route('/contacts')
@login_required
def view_contacts():
    contacts = db.contacts.find({"owner_id": current_user.get_id()})
    return render_template('view_contacts.html', contacts=contacts)

@app.route('/contact/edit/<contact_id>', methods=['POST', 'GET'])
@login_required
def edit_contact(contact_id):
    contact = db.contacts.find_one({"_id": ObjectId(contact_id)})
    if not contact:
        abort(404)

    form = ContactForm(data=contact)
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        phone = form.phone.data
        email = form.email.data
        address = form.address.data
        db.contacts.update_one(
            {"_id": ObjectId(contact_id)},
            {"$set": {"name": name, "phone": phone, "email": email, "address": address}}
        )
        flash('Contact updated successfully', 'success')
        return redirect(url_for('view_contacts'))

    return render_template('edit_contact.html', form=form, contact=contact)

@app.route('/contact/delete/<contact_id>', methods=['POST'])
@login_required
def delete_contact(contact_id):
    db.contacts.delete_one({"_id": ObjectId(contact_id)})
    flash('Contact deleted successfully', 'success')
    return redirect(url_for('view_contacts'))