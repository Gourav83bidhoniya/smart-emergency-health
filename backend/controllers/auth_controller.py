from flask import request, jsonify
from pymongo import MongoClient
import os
import random
import string
from dotenv import load_dotenv

# Direct Database Connection yahin kar diya!
load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client['smart_health_db']
users_col = db['users']

def register_user():
    data = request.json
    
    if users_col.find_one({"phone": data.get("phone")}):
        return jsonify({"error": "Phone number already registered!"}), 400

    user_id = 'usr_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=9))
    new_user = {**data, "userId": user_id}
    
    users_col.insert_one(new_user)
    new_user['_id'] = str(new_user['_id'])
    
    return jsonify({"message": "Account created!", "user": new_user}), 201

def login_user():
    data = request.json
    user = users_col.find_one({"phone": data.get("phone"), "password": data.get("password")})
    
    if not user:
        return jsonify({"error": "Invalid phone number or password"}), 400
        
    user['_id'] = str(user['_id'])
    return jsonify({"message": "Login successful", "user": user}), 200
