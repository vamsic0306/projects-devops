# orders app placeholder
###############################################################
# ORDERS MICROSERVICE
# Features:
# ✔ Create order
# ✔ List orders for logged-in user
# ✔ JWT validation by calling Users service /verify endpoint
# ✔ PostgreSQL DB (orders-db)
# ✔ Auto create tables
# ✔ Production-ready Flask app
###############################################################

from flask import Flask, request, jsonify
import requests
import psycopg2
from psycopg2.extras import RealDictCursor
import os
import datetime

app = Flask(__name__)

# Environment variables (Kubernetes Secrets)
USERS_SERVICE_URL = os.environ.get("USERS_SERVICE_URL")  # http://users:5001
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME", "ordersdb")
DB_USER = os.environ.get("DB_USER", "orders_admin")
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
# Auto Create Orders Table
#################################################
def create_tables():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            product TEXT NOT NULL,
            amount NUMERIC(10,2) NOT NULL,
            status TEXT DEFAULT 'created',
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

create_tables()


#################################################
# JWT VALIDATION (call users-service)
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
# CREATE ORDER
#################################################
@app.route("/orders", methods=["POST"])
def create_order():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"error": "Missing Authorization header"}), 401

    validation = validate_token(token)

    if not validation.get("valid"):
        return jsonify({"error": "Invalid or expired token"}), 401

    user = validation.get("user")
    user_id = user.get("user_id")

    data = request.json
    product = data.get("product")
    amount = data.get("amount")

    if not product or not amount:
        return jsonify({"error": "Missing fields"}), 400

    conn = get_db_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("""
        INSERT INTO orders (user_id, product, amount)
        VALUES (%s, %s, %s)
        RETURNING *;
    """, (user_id, product, amount))
    order = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"message": "Order created", "order": order})


#################################################
# LIST ORDERS FOR LOGGED IN USER
#################################################
@app.route("/orders", methods=["GET"])
def list_orders():
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
    cur.execute("SELECT * FROM orders WHERE user_id=%s", (user_id,))
    orders = cur.fetchall()
    cur.close()
    conn.close()

    return jsonify({"orders": orders})


#################################################
# HEALTH CHECK
#################################################
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "orders-service healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
