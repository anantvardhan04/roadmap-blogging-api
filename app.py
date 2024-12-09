from flask import Flask, jsonify, request
import os
from datetime import datetime
import json

app = Flask(__name__)

# mock posts_table
posts_table_path = "post_data"


@app.route("/")
def index():
    return "Index page"


# Define APIs
@app.route("/posts", methods=["GET", "POST"])
def post():
    if request.method == "GET":
        posts = []
        search_term = request.args.get("term")

        for post in os.listdir(posts_table_path):
            with open(os.path.join(posts_table_path, post), "r") as file:
                post_data = json.load(file)
            if not search_term:
                posts.append(post_data)
                continue
            if (
                search_term in post_data["title"]
                or search_term in post_data["content"]
                or search_term in post_data["category"]
            ):
                posts.append(post_data)
        return jsonify(posts), 200
    elif request.method == "POST":
        post_data = request.get_json()
        # request data
        title = post_data["title"]
        content = post_data["content"]
        category = post_data["category"]
        tags = post_data["tags"]
        # additional metadata
        createdAt = updatedAt = datetime.now().isoformat()
        id = len(os.listdir(posts_table_path)) + 1
        post = {
            "id": id,
            "title": title,
            "content": content,
            "category": category,
            "tags": tags,
            "createdAt": createdAt,
            "updatedAt": updatedAt,
        }
        with open(os.path.join(posts_table_path, f"{id}.json"), "w") as file:
            json.dump(post, file, indent=4)
        return jsonify(post), 201


@app.route("/posts/<id>", methods=["PUT", "DELETE", "GET"])
def update(id):
    if request.method == "GET":
        try:
            with open(os.path.join(posts_table_path, f"{id}.json"), "r") as file:
                post_data = json.load(file)
                return jsonify(post_data), 200
        except FileNotFoundError:
            return jsonify({"message": "Post not found"}), 404
    elif request.method == "PUT":
        try:
            request_data = request.get_json()
            with open(os.path.join(posts_table_path, f"{id}.json"), "r") as file:
                post_data = json.load(file)
            post_data["title"] = request_data["title"]
            post_data["content"] = request_data["content"]
            post_data["category"] = request_data["category"]
            post_data["tags"] = request_data["tags"]
            post_data["updatedAt"] = datetime.now().isoformat()
            with open(os.path.join(posts_table_path, f"{id}.json"), "w") as file:
                json.dump(post_data, file, indent=4)
            return jsonify(post_data), 200
        except FileNotFoundError:
            return jsonify({"error": "Post not found"}), 404
    elif request.method == "DELETE":
        try:
            os.remove(os.path.join(posts_table_path, f"{id}.json"))
            return "", 204
        except FileNotFoundError:
            return jsonify({"error": "Post not found"}), 404


app.run(debug=True)
