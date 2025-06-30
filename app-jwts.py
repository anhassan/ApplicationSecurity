from flask import Flask, request, jsonify
import jwt
import datetime
import json

app = Flask(__name__)

SECRET_KEY = "A random secret key in the server"

orders = [
    {"user" : "John",
     "orders": ["Product A", "Product B", "Product C"]
     }
]

users = [
    {
        "username" : "John",
        "password" : "John123"
    }
]

@app.route("/login", methods=['POST'])
def login():
    req_data = request.json
    user_name = req_data["username"]
    password = req_data["password"]

    req_user = {"username" : user_name, "password": password}

    if req_user in users:
        jwt_token = jwt.encode(
            {"username" : user_name,
            "exp" : int((datetime.datetime.now() + datetime.timedelta(hours=1)).timestamp())
            },
            SECRET_KEY, 
            algorithm = 'HS256'
        )

        return jsonify({"token": jwt_token})
    
    return jsonify({"message" : "Invalid credentials or User does not exists"}),401


@app.route("/orders", methods = ["GET"])
def get_orders():
    print("=======================")
    print(request.headers)
    print("==============")
    print(request.headers["Authorization"])
    print("+++++++++++++++++++")

    auth_header = request.headers["Authorization"]
    jwt_token = auth_header.split(" ")[1]
    
    try:
        decoded_token = jwt.decode(
            jwt_token,
            SECRET_KEY,
            algorithms = ["HS256"]
        )

        user_name = decoded_token["username"]
        user_order = [order["orders"] for order in orders if order["user"] == user_name]

        if user_order:
            return jsonify({"message": f"User: {user_name} orders are: {user_order[0]}"})
        else:
            return jsonify({"message" : f"No orders for user: {user_name} exists!"})

    except jwt.ExpiredSignatureError:
        return jsonify({"message" : "Token has expired"},401)
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid Token"},401)

    return jsonify({"message": decoded_token})


if __name__ == "__main__":
    app.run(debug=True)
