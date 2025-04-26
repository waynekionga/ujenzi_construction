from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql
import datetime
import base64
import requests
from requests.auth import HTTPBasicAuth

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
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.form
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    phone = data.get("phone")

    if not username or not email or not password or not phone:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO users (username, email, password, phone) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (username, email, password, phone))
    conn.commit()
    conn.close()

    return jsonify({"message": "Signup successful!"})

# -------- LOGIN --------
@app.route("/api/login", methods=["POST"])
def login():
    data = request.form
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "SELECT username, email, phone FROM users WHERE username=%s AND email=%s AND password=%s"
    cursor.execute(sql, (username, email, password))

    if cursor.rowcount == 0:
        conn.close()
        return jsonify({"message": "Login failed. Invalid credentials"}), 401

    user = cursor.fetchone()
    conn.close()
    return jsonify({"message": "Login successful", "user": user})

# -------- ADD WORKER --------
@app.route("/api/workers", methods=["POST"])
def add_worker():
    data = request.form
    name = data.get("name")
    role = data.get("role")
    phone = data.get("phone")

    if not name or not role or not phone:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO workers (name, role, phone) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, role, phone))
    conn.commit()
    conn.close()

    return jsonify({"message": "Worker added successfully!"})

# -------- ADD PROJECT --------
@app.route("/api/projects", methods=["POST"])
def add_project():
    data = request.form
    project_name = data.get("project_name")
    blueprint_url = data.get("blueprint_url")
    status = data.get("status")

    if not project_name or not blueprint_url or not status:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    sql = "INSERT INTO projects (project_name, blueprint_url, status) VALUES (%s, %s, %s)"
    cursor.execute(sql, (project_name, blueprint_url, status))
    conn.commit()
    conn.close()

    return jsonify({"message": "Project added successfully!"})

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
