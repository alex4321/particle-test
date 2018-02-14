from .entities import User, Message
from .database import Database
from datetime import datetime
import pytz
from tzlocal import get_localzone


def _current_time():
    """
    Get current time (timezone automatically converts to UTC)
    :return: current time (unix time by UTC timezone)
    :rtype: float
    """
    tz = get_localzone()
    dt = datetime.now(tz).astimezone(pytz.utc)
    return dt.timestamp()


class EntityManager:
    """
    Wrapper to work with database query parameters/results as entities from messaging.entities
    """

    def __init__(self, db):
        """
        Initialization
        :param db: database wrapper
        :type db: Database
        """
        self.db = db

    async def connect(self):
        """
        Initialize connections
        """
        await self.db.connect()

    async def disconnect(self):
        """
        Close connections
        """
        await self.db.disconnect()

    async def create_user(self):
        """
        Create user
        :return: user
        :rtype: User
        """
        return User(await self.db.create_user())

    async def subscribe(self, follower, target):
        """
        Subscribe follower user to target user
        :type follower: User
        :type target: User
        """
        await self.db.subscribe(follower.uid, target.uid)

    async def unsubscribe(self, follower, target):
        """
        Unsubscribe follower user from target user
        :type follower: User
        :type target: User
        """
        await self.db.unsubscribe(follower.uid, target.uid)

    async def post(self, author, body, reply_to_message):
        """
        Post message
        :param author: author
        :type author: User
        :param body: message text
        :type body: str
        :param reply_to_message: parent message or None
        :type reply_to_message: Message|NoneType
        :return: message
        :rtype: Message
        """
        if reply_to_message is not None:
            reply_to_message_id = reply_to_message.id
        else:
            reply_to_message_id = None
        unix_timestamp = _current_time()
        mid = await self.db.post(author.uid, body, unix_timestamp, reply_to_message_id)
        return Message(mid, author, body, unix_timestamp, reply_to_message)

    async def timeline(self, user, max_messages):
        """
        Timeline getting
        :param user: viewer user
        :type user: User
        :param max_messages: messages limit
        :type max_messages: int
        :return: messages
        :rtype: list[Message]
        """
        messages = []
        for row in await self.db.timeline(user.uid, max_messages):
            mid, uid, body, time, reply_to = row
            if reply_to:
                reply_to_message = Message(reply_to, None, None, None, None)
            else:
                reply_to_message = None
            messages.append(Message(
                mid,
                User(uid),
                body,
                time,
                reply_to_message
            ))
        return messages
