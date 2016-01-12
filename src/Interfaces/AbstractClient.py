__author__ = 'tmy'

import abc


class AbstractClient(object):
    """
    Abstract class to implement a remote sparql interface.
    """
    metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_sub_class_of_subjects(self):
        pass

    @abc.abstractmethod
    def get_all_class_parents(self, rdf_type):
        pass

    @abc.abstractmethod
    def get_class_parents(self, rdf_type):
        pass

    @abc.abstractmethod
    def count_instances(self, rdf_type):
        pass

    @abc.abstractmethod
    def count_shared_instances(self, rdf_type, other_type):
        pass

    @abc.abstractmethod
    def get_types(self, instance):
        pass

    @abc.abstractmethod
    def query(self, query):
        pass


class SparqlConnectionError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Problem on server / service: " + str(self.value)