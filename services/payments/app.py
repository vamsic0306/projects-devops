# payments app placeholder
###############################################################
# PAYMENTS MICROSERVICE
# Features:
# ✔ Validate JWT via Users service
# ✔ Validate order exists via Orders service
# ✔ Create new payment record
# ✔ PostgreSQL DB (payments-db)
# ✔ Auto-create payments table
# ✔ Production-ready Flask app
###############################################################

from flask import Flask, request, jsonify
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
import os

app = Flask(__name__)

# Environment variables from Kubernetes Secrets
USERS_SERVICE_URL = os.environ.get("USERS_SERVICE_URL")     # e.g. http://users:5001
ORDERS_SERVICE_URL = os.environ.get("ORDERS_SERVICE_URL")   # e.g. http://orders:5002

DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME", "paymentsdb")
DB_USER = os.environ.get("DB_USER", "payments_admin")
DB_PASSWORD = os.environ.get("DB_PASSWORD")


#################################################
# Connect to PostgreSQL
#################################################
def get_db_conn():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


#################################################
# Auto-create payments table
#################################################
def create_tables():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS payments (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            order_id INTEGER NOT NULL,
            amount NUMERIC(10,2) NOT NULL,
            status TEXT DEFAULT 'success',
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

create_tables()


#################################################
# Validate JWT → via users-service
#################################################
def validate_token(token):
    try:
        response = requests.post(
            f"{USERS_SERVICE_URL}/verify",
            json={"token": token},
            timeout=3
        )
        return response.json()
    except Exception:
        return {"valid": False, "error": "Auth service unavailable"}


#################################################
# Validate Order Exists → via orders-service
#################################################
def validate_order(token, order_id):
    try:
        response = requests.get(
            f"{ORDERS_SERVICE_URL}/orders",
            headers={"Authorization": token},
            timeout=3
        )
        orders = response.json().get("orders", [])

        for order in orders:
            if order["id"] == order_id:
                return order
        return None
    except Exception:
        return None


#################################################
# PROCESS PAYMENT
#################################################
@app.route("/pay", methods=["POST"])
def pay():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Missing Authorization header"}), 401

    # Validate JWT
    validation = validate_token(token)

    if not validation.get("valid"):
        return jsonify({"error": "Invalid or expired token"}), 401

    user = validation.get("user")
    user_id = user.get("user_id")

    # Request body
    data = request.json
    order_id = data.get("order_id")
    amount = data.get("amount")

    if not order_id or not amount:
        return jsonify({"error": "order_id and amount are required"}), 400

    # Validate order
    order = validate_order(token, order_id)
    if not order:
        return jsonify({"error": "Invalid order or not found"}), 400

    # Insert payment record
    conn = get_db_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        INSERT INTO payments (user_id, order_id, amount)
        VALUES (%s, %s, %s)
        RETURNING *;
    """, (user_id, order_id, amount))

    payment = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({
        "message": "Payment successful",
        "payment": payment
    })


#################################################
# LIST USER PAYMENTS
#################################################
@app.route("/payments", methods=["GET"])
def list_payments():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Missing Authorization header"}), 401

    validation = validate_token(token)

    if not validation.get("valid"):
        return jsonify({"error": "Invalid or expired token"}), 401

    user = validation.get("user")
    user_id = user.get("user_id")

    conn = get_db_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT * FROM payments WHERE user_id=%s", (user_id,))
    payments = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify({"payments": payments})


#################################################
# HEALTH CHECK
#################################################
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "payments-service healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
