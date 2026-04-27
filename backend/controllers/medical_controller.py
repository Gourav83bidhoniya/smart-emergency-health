from flask import request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()

# ✅ Sirf ek baar DB connect karo
client = MongoClient(os.getenv("MONGO_URI"))
db = client['smart_health_db']
profiles_col = db['profiles']
meds_col = db['medicines']


# Profile Logic
def get_user_profile(userId):
    if not userId:
        return jsonify({"error": "userId is required!"}), 400

    profile = profiles_col.find_one({"userId": userId})
    if profile:
        profile['_id'] = str(profile['_id'])
        return jsonify(profile), 200
    return jsonify({}), 200


def save_user_profile():
    data = request.json

    if not data or not data.get("userId"):
        return jsonify({"error": "userId is required!"}), 400

    profiles_col.update_one(
        {"userId": data['userId']},
        {"$set": data},
        upsert=True
    )
    return jsonify({"message": "Profile saved securely!"}), 200


# Medicine Logic
def get_user_medicines(userId):
    if not userId:
        return jsonify({"error": "userId is required!"}), 400

    meds = list(meds_col.find({"userId": userId}))
    for m in meds:
        m['_id'] = str(m['_id'])
    return jsonify(meds[::-1]), 200


def add_user_medicine():
    data = request.json

    if not data or not data.get("userId"):
        return jsonify({"error": "userId is required!"}), 400

    if 'status' not in data:
        data['status'] = 'pending'

    res = meds_col.insert_one(data)
    data['_id'] = str(res.inserted_id)
    return jsonify(data), 201


def update_medicine_status(med_id):
    data = request.json

    if not data or not data.get("status"):
        return jsonify({"error": "status is required!"}), 400

    try:
        meds_col.update_one(
            {"_id": ObjectId(med_id)},
            {"$set": {"status": data.get("status")}}
        )
        return jsonify({"message": "Status updated!"}), 200
    except Exception as e:
        return jsonify({"error": f"Invalid medicine ID: {str(e)}"}), 400
