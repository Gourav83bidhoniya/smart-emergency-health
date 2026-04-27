from flask import request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

# Direct Database Connection yahin kar diya!
load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client['smart_health_db']
profiles_col = db['profiles']
meds_col = db['medicines']

# Profile Logic
def get_user_profile(userId):
    profile = profiles_col.find_one({"userId": userId})
    if profile:
        profile['_id'] = str(profile['_id'])
        return jsonify(profile), 200
    return jsonify({}), 200

def save_user_profile():
    data = request.json
    profiles_col.update_one(
        {"userId": data['userId']}, 
        {"$set": data}, 
        upsert=True
    )
    return jsonify({"message": "Profile saved securely!"}), 200

# Medicine Logic
def get_user_medicines(userId):
    meds = list(meds_col.find({"userId": userId}))
    for m in meds: 
        m['_id'] = str(m['_id'])
    return jsonify(meds[::-1]), 200

def add_user_medicine():
    data = request.json
    if 'status' not in data:
        data['status'] = 'pending'
    res = meds_col.insert_one(data)
    data['_id'] = str(res.inserted_id)
    return jsonify(data), 201

def update_medicine_status(med_id):
    data = request.json
    meds_col.update_one(
        {"_id": ObjectId(med_id)},
        {"$set": {"status": data.get("status")}}
    )
    return jsonify({"message": "Status updated!"}), 200
