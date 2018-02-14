class Database:
    """
    Database "interface"
    """

    def __init__(self, connection_string):
        """
        Initialize database
        :param connection_string: connection string
        :type connection_string: str
        """
        raise NotImplementedError()

    async def connect(self):
        """
        Connect to database
        """
        raise NotImplementedError()

    async def disconnect(self):
        """
        Disconnect from database
        """
        raise NotImplementedError()

    async def create_user(self):
        """
        Create user
        :return: UID (integer)
        """
        raise NotImplementedError()

    async def subscribe(self, follower_id, target_id):
        """
        Subscribe follower user to target user
        :type follower_id: int
        :type target_id: int
        """
        raise NotImplementedError()

    async def unsubscribe(self, follower_id, target_id):
        """
        Unsubscribe follower user from target user
        :type follower_id: int
        :type target_id: int
        """
        raise NotImplementedError()

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
        raise NotImplementedError()

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
        raise NotImplementedError()
