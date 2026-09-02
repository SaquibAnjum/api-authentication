import os
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.environ.get(
    "JWT_SECRET_KEY",
    "super-secret-jwt-key-for-api-authentication-production-use"
)
jwt = JWTManager(app)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "online",
        "message": "API Authentication Service is running!",
        "endpoints": {
            "POST /login": "Send email and password to receive JWT token",
            "GET /protected-route": "Send JWT token in Authorization header to access"
        }
    }), 200

@app.route("/login", methods=["GET", "POST"])
def handle_login():
    if request.method == "GET":
        return jsonify({
            "message": "Send a POST request with JSON body to log in.",
            "example_body": {
                "email": "saquib1312@gmail.com",
                "password": "12345"
            }
        }), 200

    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    if email == "saquib1312@gmail.com" and password == "12345":
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route("/protected-route", methods=["GET"])
@jwt_required()
def handle_protected_route():
    current_user = get_jwt_identity()
    return jsonify({
        "message": "This is a protected route. You have access!",
        "email": current_user
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
