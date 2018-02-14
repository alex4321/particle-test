import aiopg
from .database import Database


class DatabasePostgresql(Database):
    """
    Postgresql database interface.
    """

    def __init__(self, connection_string):
        """
        Initialize database
        :param connection_string: connection string
        :type connection_string: str
        """
        self._pool = None
        self._connection = None
        self._dsn = connection_string

    async def connect(self):
        """
        Connect to database
        """
        self._pool = await aiopg.create_pool(self._dsn)
        self._connection = await self._pool.acquire()

    async def disconnect(self):
        """
        Disconnect from database
        """
        self._pool.release(self._connection)

    async def create_user(self):
        """
        Create user
        :return: UID (integer)
        """
        sql = "INSERT INTO users VALUES (DEFAULT) RETURNING users.uid"
        async with self._connection.cursor() as cur:
            await cur.execute(sql)
            (uid,) = await cur.fetchone()
            return uid

    async def subscribe(self, follower_id, target_id):
        """
        Subscribe follower user to target user
        :type follower_id: int
        :type target_id: int
        """
        sql = "INSERT INTO followers (follower, target) VALUES (%(follower)s, %(target)s)"
        async with self._connection.cursor() as cur:
            await cur.execute(sql, {
                'follower': follower_id,
                'target': target_id
            })

    async def unsubscribe(self, follower_id, target_id):
        """
        Unsubscribe follower user from target user
        :type follower_id: int
        :type target_id: int
        """
        sql = "DELETE FROM followers WHERE followers.follower=%(follower)s AND followers.target=%(target)s"
        async with self._connection.cursor() as cur:
            await cur.execute(sql, {
                'follower': follower_id,
                'target': target_id
            })

    async def post(self, author_id, body, unix_timestamp, reply_to_message_id):
        """
        Post message
        :param author_id: author UID
        :type author_id: int
        :param body: message text
        :type body: str
        :param unix_timestamp: message initiation unix time (**by UTC**)
        :type unix_timestamp: float
        :param reply_to_message_id: id of parent message or None
        :type reply_to_message_id: int|NoneType
        :return: message id
        :rtype: int
        """
        sql = "INSERT INTO messages (author_id, body, unix_timestamp, reply_to) VALUES (" + \
              "%(author)s, %(body)s, %(unix_timestamp)s, %(reply_to)s" + \
              ") " + \
              "RETURNING messages.id"
        async with self._connection.cursor() as cur:
            await cur.execute(sql, {
                "author": author_id,
                "body": body,
                "unix_timestamp": unix_timestamp,
                "reply_to": reply_to_message_id
            })
            (mid,) = await cur.fetchone()
            return mid

    async def timeline(self, uid, max_messages):
        """
        Timeline getting
        :param uid: viewer user id
        :type uid: int
        :param max_messages: messages limit
        :type max_messages: int
        :return: messages (tuples of id, author_id, body, unix timestamp, parent message id)
        :rtype: list[(int, int, str, float, int|NoneType)]
        """
        sql = "SELECT messages.id, messages.author_id, messages.body, messages.unix_timestamp, messages.reply_to " + \
              "FROM messages " + \
              "INNER JOIN users ON (messages.author_id = users.uid) " + \
              "INNER JOIN followers ON users.uid = followers.target " + \
              "LEFT OUTER JOIN messages parent_messages ON parent_messages.id = messages.reply_to " + \
              "LEFT OUTER JOIN users parent_messages_author ON parent_messages_author.uid = parent_messages.author_id " + \
              "LEFT OUTER JOIN followers parent_message_followers ON parent_message_followers.target=parent_messages_author.uid " + \
              "WHERE followers.follower=%(uid)s AND (" + \
              "    messages.reply_to IS NULL OR " + \
              "    parent_message_followers.follower=%(uid)s " + \
              ") " + \
              "ORDER BY messages.unix_timestamp DESC " + \
              "LIMIT %(max_messages)s"
        async with self._connection.cursor() as cur:
            await cur.execute(sql, {
                'uid': uid,
                'max_messages': max_messages
            })
            result = [
                (mid, uid, body, float(time), reply_to)
                for mid, uid, body, time, reply_to in await cur.fetchall()
            ]
            return result