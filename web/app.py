import requests
from flask import Flask, request

app = Flask(__name__)
control_instance_number = 0

def store_instance(instance):
    return 'Store {}'.format(instance)

def get_instances():
    return 'List of Instances'

def get_instance_info(instance):
    return requests.get('https://mcapi.us/server/status?ip=23.96.52.8&port=25565').content

def delete_instances(instance):
    return 'Delete {}'.format(instance)

@app.route('/')
def hello_world():
    return 'Flask Dockerized'

@app.route('/instance', methods=['GET'])
def getInstances():
    if request.method == 'GET':
        return get_instances()

@app.route('/instance/<instance>', methods=['GET', 'POST', 'DELETE'])
def instance(instance):
    if request.method == 'POST':
        return store_instance(instance)
    elif request.method == 'GET':
        return get_instance_info(instance)
    elif request.method == 'DELETE':
        return delete_instances(instance)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')