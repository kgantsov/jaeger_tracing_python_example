import json
import logging

import aiohttp
import asyncio
from aiohttp import web
from opentracing.ext import tags
from opentracing.propagation import Format
from opentracing.scope_managers.asyncio import AsyncioScopeManager
from tracing import init_tracer


tracer = init_tracer('gateway', scope_manager=AsyncioScopeManager)


async def fetch(session, url, span):
    span.set_tag(tags.HTTP_METHOD, 'GET')
    span.set_tag(tags.HTTP_URL, url)
    span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_CLIENT)

    headers = {}
    tracer.inject(span, Format.HTTP_HEADERS, headers)

    async with session.get(url, headers=headers) as response:
        return await response.json()


async def handle_favicon(request):
    return web.Response(text='')


async def handle(request):
    token = request.match_info.get('token', "MY_TOKEN")

    async with aiohttp.ClientSession() as session:
        with tracer.start_active_span('process_request') as scope:
            data = await fetch(session, 'http://localhost:5003/token/{}/'.format(token), scope.span)
            print(data)

            role_tasks = [
                asyncio.ensure_future(
                    fetch(session, 'http://localhost:5002/roles/{}/'.format(x), scope.span)
                )
                for x in ['can_read_assets', 'can_read_users']
            ]

            acl_tasks = [
                asyncio.ensure_future(
                    fetch(session, 'http://localhost:5002/acls/{}/'.format(x), scope.span)
                )
                for x in ['read', 'write', 'delete']
            ]

            responses = await asyncio.gather(*acl_tasks, *role_tasks)
            print(responses)

            data = await fetch(
                session, 'http://localhost:5001{}'.format(request.path_qs), scope.span
            )
            print(data)

            return web.Response(text=json.dumps(data))

app = web.Application()
app.add_routes([
    web.get('/favicon.ico', handle_favicon),
    web.get(r'/{parts:.+}', handle),
])

web.run_app(app)
