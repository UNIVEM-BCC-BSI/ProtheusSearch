from flask import Flask, request, jsonify
import json
app = Flask(__name__)
app.run(debug=True)
# read file
with open('tasks.json', 'r') as myfile:
    data=myfile.read()
# parse file
obj = json.loads(data)
@app.route('/todo/getall',methods=['GET'])
def getTasks():
    return jsonify(obj)