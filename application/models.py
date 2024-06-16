from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, empid, password):
        self.id = user_id
        self.empid = empid
        self.password = password

    


class Pet:
    def __init__(self, pet_id, name, species, breed, age, owner_id):
        self.id = pet_id
        self.name = name
        self.species = species
        self.breed = breed
        self.age = age
        self.owner_id = owner_id

class Appointment:
    def __init__(self, appointment_id, pet_id, date, description):
        self.appointment_id = appointment_id
        self.pet_id = pet_id
        self.date = date
        self.description = description

class HealthRecord:
    def __init__(self, pet_id, date, description):
        self.pet_id = pet_id
        self.date = date
        self.description = description

class NutritionRecord:
    def __init__(self, pet_id, date, food_type, quantity):
        self.pet_id = pet_id
        self.date = date
        self.food_type = food_type
        self.quantity = quantity
        
    def get_id(self):
        return self.id


    