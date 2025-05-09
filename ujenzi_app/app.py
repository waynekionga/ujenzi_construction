from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import datetime
import pymysql.cursors  # Ensure this is imported
import base64
import requests
from requests.auth import HTTPBasicAuth
import os 

app = Flask(__name__)
CORS(app)

# Database connection function
def get_db_connection():
    # Use "localhost" for local development, or your Render database host when deployed
    return pymysql.connect(
        host="localhost",           # Change to "localhost" for local development
        user="root",                # Your MySQL username
        password="14550",           # Your MySQL password
        database="ujenzi_db",       # Your database name
        cursorclass=pymysql.cursors.DictCursor
    )

# -------- SIGNUP --------
@app.route('/api/signup', methods=['POST'])
def signup():
    data = request.get_json()

    username = data['username']
    email = data['email']
    password = data['password']
    phone = data['phone']

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if email already exists
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()

    if existing_user:
        cursor.close()
        conn.close()
        return jsonify({'error': 'Email already registered'}), 409

    # Insert new user
    sql = "INSERT INTO users (username, email, password, phone) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (username, email, password, phone))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({'message': 'User registered successfully'}), 201


# -------- LOGIN --------
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()  # ← this was request.form before

    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)  # to get dictionary output
    sql = "SELECT username, email, phone FROM users WHERE email=%s AND password=%s"
    cursor.execute(sql, (email, password))

    user = cursor.fetchone()
    conn.close()

    if not user:
        return jsonify({"message": "Login failed. Invalid credentials"}), 401

    # You can optionally generate a token here and return it
    return jsonify({"message": "Login successful", "user": user}), 200

# -------- ADD + FETCH WORKERS --------
@app.route("/api/workers", methods=["GET", "POST"])
def workers():
    if request.method == "POST":
        data = request.get_json()
        name = data.get("name")
        role = data.get("role")
        phone = data.get("phone")
        worker_photo_path = data.get("worker_photo")
        worker_photo = os.path.basename(worker_photo_path)


        if not name or not role or not phone or not worker_photo:
            return jsonify({"error": "Missing fields"}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO workers (name, role, phone, worker_photo) VALUES (%s, %s, %s, %s)",
            (name, role, phone, worker_photo)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Worker added successfully"}), 201

    elif request.method == "GET":
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT name, role, phone, worker_photo FROM workers")
        workers = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(workers)

# -------- GET PROJECTS --------
@app.route("/api/projects", methods=["GET"])
def get_projects():
    conn = get_db_connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)  # ✅ This works with pymysql
    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(projects), 200


# -------- ADD PROJECT --------
@app.route("/api/projects", methods=["POST"])
def add_project():
    data = request.get_json()
    name = data.get("name")
    description = data.get("description")
    blueprint = data.get("blueprint")
    status = data.get("status")

    if not name or not description or not blueprint or not status:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO projects (name, description, blueprint, status) VALUES (%s, %s, %s, %s)",
        (name, description, blueprint, status)
    )
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"message": "Project added successfully"}), 201

# -------- M-PESA PAYMENT --------
@app.route('/api/mpesa_payment', methods=['POST'])
def mpesa_payment():
    amount = request.form.get('amount')
    phone = request.form.get('phone')

    if not amount or not phone:
        return jsonify({"error": "Amount and phone are required"}), 400

    # Sandbox credentials (keep secret in prod)
    consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
    consumer_secret = "amFbAoUByPV2rM5A"

    # Get access token
    token_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    r = requests.get(token_url, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    access_token = "Bearer " + r.json()['access_token']

    # Generate password
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    business_short_code = "174379"
    passkey = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
    data_to_encode = business_short_code + passkey + timestamp
    password = base64.b64encode(data_to_encode.encode()).decode('utf-8')

    # STK Push Payload
    payload = {
        "BusinessShortCode": business_short_code,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone,
        "PartyB": business_short_code,
        "PhoneNumber": phone,
        "CallBackURL": "https://mydomain.com/callback",  # Use a real URL when live
        "AccountReference": "Ujenzi Construction",
        "TransactionDesc": "Service Payment"
    }

    headers = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }

    # Trigger STK Push
    response = requests.post(
        "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
        json=payload,
        headers=headers
    )

    return jsonify({
        "message": "An M-PESA prompt has been sent to your phone. Complete payment to proceed.",
        "safaricom_response": response.json()
    })

# Run the app locally
if __name__ == '__main__':
    app.run(debug=True)
