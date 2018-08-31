from flask import Flask, request
from kubernetes import client, config
from kubernetes.client.rest import ApiException
from os import path
from pprint import pprint

import kubernetes
import requests
import time
import yaml

app = Flask(__name__)
control_instance_number = 0
POD_YAML_FILE = "minecraft-server-pod.yaml"
SERVICE_YAML_FILE = "minecraft-server-service.yaml"
NAMESPACE = "default"
PRETTY = 'pretty_example'

def store_instance():
    config.load_kube_config()
    podspec = {}
    servicespec = {}

    with(open(path.join("yaml", POD_YAML_FILE))) as podfile:
        podspec = yaml.load(podfile)
        print("Pod spec is:" + str(podspec))

    with(open(path.join("yaml", SERVICE_YAML_FILE))) as servicefile:
        servicespec = yaml.load(servicefile)
        print("Service spec is:" + str(servicespec))
    try:
        k8sapi = client.CoreV1Api()
        identity = str(int(time.time()))
        podspec["metadata"]["name"] = podspec["metadata"]["name"] + "-" + identity
        k8sapi.create_namespaced_pod(namespace=NAMESPACE, body=podspec, pretty=PRETTY)
        servicespec["metadata"]["name"] = servicespec["metadata"]["name"] + "-" + identity
        k8sapi.create_namespaced_service(namespace=NAMESPACE, body=servicespec, pretty=PRETTY)
    except ApiException as e:
        print("Exception when creating pod: %s\n" % e)
    return ('', 200)

def get_instances():
    return 'List of Instances'

def get_instance_info(instance):
    return requests.get('https://mcapi.us/server/status?ip=23.96.52.8&port=25565').content

def delete_instances(instance):
    return 'Delete {}'.format(instance)

@app.route('/')
def hello_world():
    return 'Flask Dockerized'

@app.route('/instance', methods=['GET', 'POST'])
def getInstances():
    if request.method == 'GET':
        return get_instances()
    elif request.method == 'POST':
        return store_instance()

@app.route('/instance/<instance>', methods=['GET', 'DELETE'])
def instance(instance):
    if request.method == 'GET':
        return get_instance_info(instance)
    elif request.method == 'DELETE':
        return delete_instances(instance)

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')