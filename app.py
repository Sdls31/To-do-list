from datetime import datetime
from flask import Flask, jsonify, request, abort

app = Flask(__name__)

tasks = []
BASE_URL = '/api/v1/'


@app.route('/')
def home():
    return 'Welcome to my To-Do List'

@app.route('/api/v1/tasks', methods=['POST'])
def create_task():
    if not request.json:
        abort(400, error = 'Missing body in request')
    print(request.json)
    if not 'name' in request.json:
        return jsonify({'404': 'ERROR no existe ese campo name'})
    elif not 'category' in request.json:
        return jsonify({'404': 'ERROR no existe ese campo category'})
    else:
        this_time = datetime.now()
        task = {
            'id' : len(tasks) + 1,
            'name' : request.json['name'],
            'category' : request.json['category'],
            'status' : False,
            'created': this_time,
            'updated' : this_time 
        }
        tasks.append(task)
        return jsonify({'task': task}), 201


@app.route('/api/v1/tasks', methods=['GET'])
def get_task():
    return jsonify({'task': tasks})


@app.route('/api/v1/tasks/<int:id>', methods=['GET'])
def get_particular_task(id):
    this_task = [task for task in tasks if task['id'] == id]
    if len(this_task) == 0:
        abort(404, error="ID not found!")
    return jsonify({'task': this_task[0]})
    

@app.route('/api/v1/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    this_task = [task for task in tasks if task['id'] == id]
    if len(this_task) == 0:
        abort(404, error="ID not found!")
    this_task[0]['status'] = not this_task[0]['status']
    # tasks[this_task[0]['id']]['status'] = True
    return jsonify({'task': this_task[0]})

    
@app.route('/api/v1/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    this_task = [task for task in tasks if task['id'] == id]
    if len(this_task) == 0:
        abort(404, error="ID not found!")
    tasks.remove(this_task[0])
    return jsonify({'task': True})
    
if __name__ == "__main__":
    app.run(debug=True)