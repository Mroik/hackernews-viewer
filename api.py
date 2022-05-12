import json

from requests import Session


ENDPOINT = "https://hacker-news.firebaseio.com/v0/"
session = Session()


def flush_session():
    global session
    session = Session()


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
    pass


class Comment(Item):
    pass


class Job(Item):
    pass


class Poll(Item):
    pass


class PollOpt(Item):
    pass


def from_data(data: str) -> Item:
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
    return from_data(data)
