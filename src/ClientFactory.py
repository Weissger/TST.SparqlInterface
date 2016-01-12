__author__ = 'tmy'

from .Interfaces.Blazegraph import Blazegraph

URI_CLASS_MAP = {'blazegraph': Blazegraph}


def make_client(server=None, user=None, password=None, prop_path=None):
    interface = [URI_CLASS_MAP[x] for x in URI_CLASS_MAP.keys() if x in server]
    if interface:
        return interface[0](server=server, user=user, password=password, prop_path=prop_path)
    else:
        raise UnknownService(server)


class UnknownService(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Service isn't supported " + str(self.value)