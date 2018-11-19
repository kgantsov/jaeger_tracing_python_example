import logging
from jaeger_client import Config


def init_tracer(service, scope_manager=None):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)

    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
            'reporter_batch_size': 1,
        },
        service_name=service,
        scope_manager=scope_manager
    )
    return config.initialize_tracer()
