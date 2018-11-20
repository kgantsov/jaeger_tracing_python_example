from flask import Flask
from flask import jsonify

import requests

from opentracing.ext import tags
from opentracing.propagation import Format

from tracing import init_tracer
from decorators import trace

tracer = init_tracer('assets')

app = Flask(__name__)


def http_get(url):
    span = tracer.active_span
    span.set_tag(tags.HTTP_METHOD, 'GET')
    span.set_tag(tags.HTTP_URL, url)
    span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_CLIENT)

    headers = {}
    tracer.inject(span, Format.HTTP_HEADERS, headers)

    return requests.get(url, headers=headers)


@app.route('/assets/<int:asset_id>/')
@trace(tracer, 'check_token')
def hello(asset_id):
    response = http_get('http://localhost:5005/metadata/assets/{}/'.format(asset_id))
    return jsonify({
        'id': asset_id,
        'name': 'Asset {}'.format(asset_id),
        'metadata': response.json()
    })


if __name__ == '__main__':
    app.run(port=5001)
