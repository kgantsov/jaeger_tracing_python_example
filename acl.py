import random
import time

from flask import Flask
from flask import jsonify

from tracing import init_tracer
from decorators import trace

app = Flask(__name__)

tracer = init_tracer('acls')


@app.route('/acls/<string:permission>/')
@trace(tracer, 'check_permission')
def check_permissions(permission):
    time.sleep(random.randint(1, 5) / 10)
    return jsonify({'access': 'granted', 'permission': permission})


@app.route('/roles/<string:role>/')
@trace(tracer, 'check_role')
def check_roles(role):
    time.sleep(random.randint(1, 5) / 10)
    return jsonify({'role': role, 'access': 'granted'})


if __name__ == '__main__':
    app.run(port=5002)
