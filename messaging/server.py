import argparse
import importlib
import json
import traceback
from aiohttp import web
from .entities import User, Message
from .entitymanager import EntityManager


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-database_connector')
    parser.add_argument('-connection_string')
    parser.add_argument('-host')
    parser.add_argument('-port')
    return parser.parse_args()


def get_db_connector_class(connector_class_name):
    """
    Get class of DB connector
    :param connector_class_name: DB connector class name
    :type connector_class_name: str
    :return: DB connector class
    :rtype: class
    """
    parts = connector_class_name.split('.')
    assert len(parts) >= 2
    classname = parts[-1]
    modulename = '.'.join(parts[:-1])
    module = importlib.import_module(modulename)
    connector_class = getattr(module, classname)
    return connector_class


def _run_server(db, host, port):
    manager = EntityManager(db)

    async def statup_db(app):
        await manager.connect()

    async def shutdown_db(app):
        await manager.disconnect()

    #region utils
    def build_response(success, data):
        body = json.dumps({
            'success': success,
            'result': data
        })
        if success:
            status = 200
        else:
            status = 500
        return web.Response(body=body,
                            status=status,
                            content_type='application/json')

    def handler_wrapper(func):
        async def handler(request):
            try:
                return build_response(True, await func(request))
            except:
                traceback.print_exc()
                return build_response(False, None)
        return handler
    #endregion

    #region request handlers
    @handler_wrapper
    async def create_user(request):
        """
        Create user request (POST)
        POST params: None
        """
        user = await manager.create_user()
        return user.values

    @handler_wrapper
    async def follow_user(request):
        """
        Subscribe follower to target messages (POST)
        POST params:
        - follower: follower UID
        - target: target UID
        """
        post = await request.post()
        follower = User(int(post['follower']))
        target = User(int(post['target']))
        await manager.subscribe(follower, target)
        return {
            'follower': follower.values,
            'target': target.values
        }

    @handler_wrapper
    async def unfollow_user(request):
        """
        Unsubscribe follower from target messages (POST)
        POST params:
        - follower: follower UID
        - target: target UID
        """
        post = await request.post()
        follower = User(int(post['follower']))
        target = User(int(post['target']))
        await manager.unsubscribe(follower, target)
        return {
            'follower': follower.values,
            'target': target.values
        }

    @handler_wrapper
    async def post(request):
        """
        Post message (POST)
        POST params:
        - author: author UID
        - body: message text
        - reply_to: if setted - parent message id
        """
        post = await request.post()
        author = User(int(post['author']))
        body = post['body']
        if 'reply_to' in post:
            reply_to = Message(int(post['reply_to']),
                               None,
                               None,
                               None,
                               None)
        else:
            reply_to = None
        message = await manager.post(author, body, reply_to)
        return message.values

    @handler_wrapper
    async def timeline(request):
        """
        Get timeline (GET)
        GET params:
        - user - viewer user UID
        - max_messages - messages limit
        """
        user = User(int(request.query['user']))
        max_messages = int(request.query['max_messages'])
        messages = await manager.timeline(user, max_messages)
        return [message.values for message in messages]
    #endregion

    app = web.Application()
    app.on_startup.append(statup_db)
    app.on_shutdown.append(shutdown_db)
    app.router.add_post('/user', create_user)
    app.router.add_post('/follow', follow_user)
    app.router.add_post('/unfollow', unfollow_user)
    app.router.add_post('/post', post)
    app.router.add_get('/timeline', timeline)
    web.run_app(app, host=host, port=int(port))


if __name__ == '__main__':
    args = get_args()
    db_class = get_db_connector_class(args.database_connector)
    db = db_class(args.connection_string)
    _run_server(db, args.host, args.port)