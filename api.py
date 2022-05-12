import json
from typing import Union

from requests import Session


ENDPOINT = "https://hacker-news.firebaseio.com/v0/"
session = Session()


def flush_session():
    global session
    session = Session()


# Items

class Item:
    """Superclass used to rappresent hackernews items"""
    def __init__(self, data: str = None):
        if data is not None:
            self.parse(data)

    def parse(self, data: str):
        """Parse json string to set attributes"""
        data = json.loads(data)
        for k in data:
            self.__setattr__(k, data[k])


class Story(Item):
    def get_comments(self, start: int = 0, n: int = 10) -> list['Comment']:
        return [get_item(id) for id in self.kids[start:start + n]]


class Comment(Item):
    def get_replies(self, start: int = 0, n: int = 10) -> list['Comment']:
        return [get_item(id) for id in self.kids[start:start + n]]

    def get_parent(self) -> Union[Story, 'Comment']:
        return get_item(self.parent)


class Job(Item):
    pass


class Poll(Item):
    def get_comments(self, start: int = 0, n: int = 10) -> list[Comment]:
        return [get_item(id) for id in self.kids[start:start + n]]

    def get_options(self) -> list['PollOpt']:
        return [get_item(id) for id in self.parts]


class PollOpt(Item):
    def get_poll(self) -> Poll:
        return get_item(self.poll)


def from_item_data(data: str) -> Item:
    """
    Helper function to get an Item object

    :param str data: A json string containing the data of the Item
    """
    parsed = json.loads(data)
    match parsed["type"]:
        case "story":
            return Story(data)
        case "comment":
            return Comment(data)
        case "job":
            return Job(data)
        case "poll":
            return Poll(data)
        case "pollopt":
            return PollOpt(data)


def get_item(id: int) -> Item:
    """Return a Hackernews item"""
    data = session.get(ENDPOINT + f"item/{id}.json").text
    return from_item_data(data)


# Users

class User:
    def __init__(self, data: str = None):
        if data is not None:
            self.parse(data)

    def parse(self, data: str):
        data = json.loads(data)
        for k in data:
            self.__setattr__(k, data[k])

    def from_id(id: str) -> 'User':
        data = session.get(ENDPOINT + f"user/{id}.json").text
        return User(data)

