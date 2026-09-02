import os
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "kacha badam")
jwt = JWTManager(app)

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "online",
        "service": "API Authentication Service",
        "endpoints": {
            "POST /login": {
                "description": "Authenticate with email and password to receive a JWT access token",
                "body": {"email": "string", "password": "string"}
            },
            "GET /protected-route": {
                "description": "Access protected route",
                "headers": {"Authorization": "Bearer <access_token>"}
            }
        }
    }), 200

@app.post("/login")
def handle_login():
    data = request.get_json(silent=True) or {}
    email = data.get("email")
    password = data.get("password")

    if email == "saquib1312@gmail.com" and password == "12345":
        access_token = create_access_token(identity=email)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.get("/protected-route")
@jwt_required()
def handle_protected_route():
    current_user = get_jwt_identity()
    return jsonify({
        "message": "This is a protected route. You have access!",
        "email": current_user
    }), 200

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
