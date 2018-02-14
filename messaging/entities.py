import json


class User:
    def __init__(self, uid):
        self.uid = uid

    @property
    def values(self):
        return {
            'uid': self.uid
        }

    def __str__(self):
        return json.dumps(self.values)

    def __repr__(self):
        return str(self)


class Message:
    def __init__(self, id, author, body, unix_timestamp, reply_to_message):
        self.id = id
        self.author = author
        self.body = body
        self.unix_timestamp = unix_timestamp
        self.reply_to_message = reply_to_message

    @property
    def values(self):
        reply_to_message_values = None
        if self.reply_to_message is not None:
            reply_to_message_values = self.reply_to_message.values
        author_values = None
        if self.author is not None:
            author_values = self.author.values
        return {
            'id': self.id,
            'author': author_values,
            'body': self.body,
            'unix_timestamp': self.unix_timestamp,
            'reply_to_message': reply_to_message_values,
        }

    def __str__(self):
        return json.dumps(self.values)

    def __repr__(self):
        return str(self)