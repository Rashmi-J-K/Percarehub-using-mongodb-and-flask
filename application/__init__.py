from flask import Flask
from flask_pymongo import PyMongo
from flask_login import LoginManager
from bson import ObjectId
from application.models import User

app = Flask(__name__)
app.config["SECRET_KEY"] = "26070cfe795e9f3a8ce805b3cc6334472d544a80"
app.config["MONGO_URI"] = "mongodb+srv://raksh212003:yaji2003@cluster0.frxunn7.mongodb.net/pet?retryWrites=true&w=majority&appName=Cluster0"

# Initialize PyMongo
mongodb_client = PyMongo(app)
db = mongodb_client.db

# Setup LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    user = db.login.find_one({"_id": ObjectId(user_id)})
    if user:
        return User(str(user['_id']), user['empid'], user['password'])
    return None

# Import routes at the end to avoid circular imports
from application import routes
