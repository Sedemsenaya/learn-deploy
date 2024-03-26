from flask import Flask, jsonify, request
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

client = MongoClient('mongodb://localhost:27017/')
db = client['Todo']
collection = db['todo']


@app.route('/')
def hello():
    return ('Hello World!')

@app.route('/getTodos', methods=["GET"])
def get_todos():
    todos = list(collection.find({}, {"_id": 0, "Name": 1}))  # Retrieve all todos from the collection
    return jsonify(todos)

@app.route('/push', methods=["POST"])
def push():
    data = request.get_json()
    collection.insert_one({"Name": data["text"]})
    return jsonify({"Name": data["text"]})


@app.route('/update', methods=['PUT'])
def update_todo():
    data = request.get_json()
    old_text = data['oldText']
    new_text = data['newText']

    # Update the todo item in the collection
    collection.update_one({"Name": old_text}, {"$set": {"Name": new_text}})

    return jsonify({"message": f"Todo updated from '{old_text}' to '{new_text}'"})


@app.route('/delete', methods=['DELETE'])
def delete():
    data = request.get_json()
    textToDelete = data['text']
    collection.delete_one({"Name": textToDelete})  # Delete the todo from the collection
    return jsonify({"message": f"{textToDelete} Deleted Successfully!"})


if __name__ == '__main__':
    app.run(port=5000, debug=True)
