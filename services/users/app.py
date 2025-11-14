# users app placeholder
###############################################
# USERS MICROSERVICE (Python + Flask)
# Features:
# ✔ User Registration
# ✔ User Login
# ✔ JWT Token Generation
# ✔ JWT Token Verification
# ✔ PostgreSQL DB (users-db)
# ✔ Auto-create tables
###############################################

from flask import Flask, request, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor
import bcrypt
import jwt
import datetime
import os

app = Flask(__name__)

# JWT Secret (should come from K8s Secret)
JWT_SECRET = os.environ.get("JWT_SECRET", "defaultsecret")
JWT_ALGO = "HS256"

# PostgreSQL connection details (from K8s Secrets)
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME", "usersdb")
DB_USER = os.environ.get("DB_USER", "users_admin")
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
# Create USERS table if not exists
#################################################
def create_tables():
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

create_tables()


#################################################
# REGISTER USER
#################################################
@app.route("/register", methods=["POST"])
def register():
    data = request.json
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"error": "Missing fields"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO users (name, email, password_hash)
            VALUES (%s, %s, %s)
            RETURNING id, name, email;
        """, (name, email, hashed_password.decode('utf-8')))
        user = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
    except psycopg2.Error:
        return jsonify({"error": "Email already exists"}), 409

    return jsonify({"message": "User registered successfully"}), 201


#################################################
# LOGIN USER (Generate JWT Token)
#################################################
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    conn = get_db_conn()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("SELECT * FROM users WHERE email=%s", (email,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    if not bcrypt.checkpw(password.encode('utf-8'), user["password_hash"].encode('utf-8')):
        return jsonify({"error": "Invalid email or password"}), 401

    # Generate JWT token
    payload = {
        "user_id": user["id"],
        "email": user["email"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=6)
    }

    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

    return jsonify({
        "message": "Login successful",
        "token": token
    })


#################################################
# VERIFY TOKEN (Used by Orders / Payments)
#################################################
@app.route("/verify", methods=["POST"])
def verify():
    token = request.json.get("token")

    try:
        decoded = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO])
        return jsonify({"valid": True, "user": decoded})
    except jwt.ExpiredSignatureError:
        return jsonify({"valid": False, "error": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"valid": False, "error": "Invalid token"}), 401


#################################################
# HEALTH CHECK (Used by Kubernetes)
#################################################
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "users-service healthy"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
