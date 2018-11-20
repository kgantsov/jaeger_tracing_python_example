import logging
from datetime import datetime

from flask import Flask
from flask import jsonify

from tracing import init_tracer
from decorators import trace

tracer = init_tracer('metadata')

app = Flask(__name__)


@app.route('/metadata/assets/<string:asset_id>/')
@trace(tracer, 'get_asset_metadata')
def get_asset_metadata(asset_id):
        return jsonify({
            'title': 'Asset {}'.format(asset_id),
            'status': 'CLOSED',
            'date_created': datetime.now().isoformat(),
        })


if __name__ == '__main__':
    app.run(port=5005)
