import logging

from flask import Flask
from flask import jsonify

from tracing import init_tracer
from decorators import trace

tracer = init_tracer('users')

app = Flask(__name__)


@app.route('/users/<string:user_id>/')
@trace(tracer, 'get_user')
def get_user(user_id):
        return jsonify({'id': user_id, 'name': 'User {}'.format(user_id)})


if __name__ == '__main__':
    app.run(port=5004)
