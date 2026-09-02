import os
from flask import Flask, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)

app = Flask(__name__)

# JWT configuration (use a 32+ character default key to satisfy SHA-256 requirements)
app.config["JWT_SECRET_KEY"] = os.environ.get(
    "JWT_SECRET_KEY",
    "super-secret-jwt-key-for-api-authentication-production-use"
)
jwt = JWTManager(app)

# Helper metadata dictionary
API_INFO = {
    "status": "online",
    "service": "API Authentication Service",
    "endpoints": {
        "GET /": "Service health and API overview",
        "POST /login": {
            "description": "Authenticate user and get JWT access token",
            "body": {"email": "saquib1312@gmail.com", "password": "12345"}
        },
        "GET /protected-route": {
            "description": "Access protected resource",
            "headers": {"Authorization": "Bearer <access_token>"}
        }
    }
}

# Root / Info routes
@app.route("/", methods=["GET"])
@app.route("/api", methods=["GET"])
@app.route("/api/", methods=["GET"])
@app.route("/api/index", methods=["GET"])
def index():
    return jsonify(API_INFO), 200

# Login routes
@app.route("/login", methods=["GET", "POST"])
@app.route("/api/login", methods=["GET", "POST"])
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

# Protected routes
@app.route("/protected-route", methods=["GET"])
@app.route("/api/protected-route", methods=["GET"])
@jwt_required()
def handle_protected_route():
    current_user = get_jwt_identity()
    return jsonify({
        "message": "This is a protected route. You have access!",
        "email": current_user
    }), 200

# Custom error handlers for clear API responses
@app.errorhandler(404)
def handle_404(e):
    return jsonify({
        "error": "Not Found",
        "message": f"The requested URL '{request.path}' was not found on this server.",
        "available_endpoints": [
            "GET /",
            "POST /login",
            "GET /protected-route"
        ]
    }), 404

@app.errorhandler(405)
def handle_405(e):
    return jsonify({
        "error": "Method Not Allowed",
        "message": f"Method {request.method} is not allowed for '{request.path}'."
    }), 405

def main():
    app.run(debug=True)

if __name__ == "__main__":
    main()
