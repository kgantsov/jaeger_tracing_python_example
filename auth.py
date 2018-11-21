import logging

import requests
from flask import Flask
from flask import jsonify

from opentracing.ext import tags
from opentracing.propagation import Format
from tracing import init_tracer
from decorators import trace

app = Flask(__name__)

tracer = init_tracer('auth')


def http_get(url):
    span = tracer.active_span
    span.set_tag(tags.HTTP_METHOD, 'GET')
    span.set_tag(tags.HTTP_URL, url)
    span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_CLIENT)

    headers = {}
    tracer.inject(span, Format.HTTP_HEADERS, headers)

    return requests.get(url, headers=headers)


@app.route('/token/<string:token>/')
@trace(tracer, 'check_token')
def hello(token):
    response = http_get('http://localhost:5004/users/1/')

    result = jsonify({'token': token, 'access': 'granted', 'user': response.json()})

    return result


if __name__ == '__main__':
    app.run(port=5003)
