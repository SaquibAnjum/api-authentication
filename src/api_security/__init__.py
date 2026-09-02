# from flask import Flask,request

# app = Flask(__name__)

# database=[
#     {"email":"saquib1312@gmail.com", "password":"12345"},
#     {"email":"john.doe@example.com", "password":"5678"}
# ]

# @app.get("/protected-route")
# def handle_protected_route():
#     email = request.headers.get("x-email")
#     password = request.headers.get("x-password")

#     options=list(map(lambda x: x["email"]==email and x["password"]==password, database))
#     print(options)

#     if True in options:
#         return {
#             "message": "This is a protected route. You have access!",
#             "email": email,
#             "password": password
#         }
#     else:
#         return {
#             "message": "Access denied."
#         }

# if __name__ == "__main__":
#     app.run(debug=True)

#--------------------------------------



from flask import Flask,request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "kacha badam"  # Change this to a strong secret key in production
jwt = JWTManager(app)

@app.post("/login")
def handle_login():
    email = request.json.get("email")
    password = request.json.get("password")

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

if __name__ == "__main__":
    app.run(debug=True)
