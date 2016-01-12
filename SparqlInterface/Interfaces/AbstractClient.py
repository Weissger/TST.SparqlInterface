__author__ = 'tmy'

import abc


class AbstractInterface(object):
    """
    Abstract class to implement a remote sparql interface.
    """
    metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_sub_class_of_subjects_distinct(self):
        pass

    @abc.abstractmethod
    def get_sub_class_of_objects_ppath(self, rdf_type):
        pass

    @abc.abstractmethod
    def get_sub_class_of_objects_recursive(self, rdf_type):
        pass

    @abc.abstractmethod
    def get_sub_class_of_objects(self, rdf_type):
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


class SparqlConnectionError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return "Problem on server / service: " + str(self.value)