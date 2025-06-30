from flask import Flask, request, jsonify
import jwt
import datetime
import json

SECRET_KEY = "A random secret key"

users_db = [
    {
        "username" : "John",
        "password" : "John123"
    },
    {
        "username" : "Kelly",
        "password": "Kelly123"
    }
]

users_orders = [
    {
        "user" : "John",
        "orders" : ["ProductA","ProductB","ProductC"]
    },
    {
        "user": "Kelly",
        "orders" : ["ProductX","ProductY"]
    }
]


app = Flask(__name__)


# Login Route
@app.route("/login",methods=["POST"])
def login():
    username = request.json["username"]
    password = request.json["password"]

    # Check whether the user exists in the user database/local storage
    user_found = [user for user in users_db if user["username"] == username and user["password"]==password]

    if user_found:
        payload =  {
                "username" : username,
                # time when the jwt token will expire
                "exp" : int((datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp())
            }
        jwt_token = jwt.encode(
           payload,
           SECRET_KEY,
           algorithm = "HS256"
        )

        return jsonify({"token" : jwt_token})
    
    return jsonify({"message": "Invalid user credentials or User does not exist.."}),401


# Protected Route (Orders route)
@app.route("/orders",methods=["GET"])
def orders():
    auth_headers = request.headers["Authorization"]
    jwt_token = auth_headers.split(" ")[1]

    try:
        decoded_token = jwt.decode(
            jwt_token,
            SECRET_KEY,
            algorithms = ["HS256"]
        )

        username = decoded_token["username"]
        user_orders = [user_order["orders"] for user_order in users_orders if user_order["user"] == username]

        if user_orders:
            return jsonify({"message": f"User: {username} has the Orders: {user_orders[0]}"})
        else:
            return jsonify({"message" : f"No orders for User: {username}"})

    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token Expired"}),401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid Token Provided"}),401



if __name__ == "__main__":
    app.run(debug=True)
