import requests
# import unirest
from .AbstractClient import AbstractClient, SparqlConnectionError
from .. import Queries, ResultParser

__author__ = 'tmy'


class Blazegraph(AbstractClient):
    def __init__(self, server=None, user=None, password=None, prop_path=True):
        self.server = server
        self.session = requests.Session()
        self.session.auth = (user, password)
        self.property_paths = prop_path

    def get_all_class_parents(self, rdf_type):
        if self.property_paths:
            return self.__get_all_class_parents_ppath(rdf_type)
        else:
            return self.__get_all_class_parents_ppath(rdf_type)

    def __get_all_class_parents_recursive(self, rdf_type):
        query = Queries.SUB_CLASS
        done_list = []
        more = [rdf_type]
        while True:
            if not more:
                break
            cur = more.pop()
            done_list.append(cur)
            result = self.session.post(self.server, params={"query": query.format(cur)},
                                       headers={"Accept": "application/sparql-results+json"}).json()
            for o in result["results"]["bindings"]:
                new_c = o["type"]["value"]
                if new_c not in done_list and new_c not in more:
                    more.append(new_c)
        return done_list

    def __get_all_class_parents_ppath(self, rdf_type):
        query = Queries.SUB_CLASS_PROPERTY_PATH
        done_list = []
        try:
            result = self.session.post(self.server, params={"query": query.format(rdf_type)},
                                       headers={"Accept": "application/sparql-results+json"})
        except Exception as e:
            print(e)
            raise (SparqlConnectionError(e))

        if result.status_code == 200:
            result = result.json()
        else:
            raise (SparqlConnectionError(result))
        for o in result["results"]["bindings"]:
            done_list.append(o["type"]["value"])
        return done_list

    def get_types(self, instance):
        query = Queries.TYPES
        return ResultParser.parse_types(requests.post(self.server, params={"query": query.format(instance)},
                                                      headers={"Accept": "application/sparql-results+json"}))

    def count_instances(self, rdf_type):
        query = Queries.INSTANCE_COUNT
        return ResultParser.parse_instance_count(requests.post(self.server, params={"query": query.format(rdf_type)},
                                                               headers={"Accept": "application/sparql-results+json"}))

    def get_class_parents(self, rdf_type):
        query = Queries.SUB_CLASS
        return ResultParser.parse_types(
            requests.post(self.server, params={"query": query.format(rdf_type)},
                          headers={"Accept": "application/sparql-results+json"}))

    def count_shared_instances(self, rdf_type, other_type):
        query = Queries.SHARED_INSTANCE_COUNT
        return ResultParser.parse_instance_count(
            requests.post(self.server, params={"query": query.format(rdf_type, other_type)},
                          headers={"Accept": "application/sparql-results+json"}))

    def insert_triple(self, subject, predicate, obj):
        query = Queries.INSERTION.format(subject, predicate, obj)
        return requests.post(self.server, params={"query": query})

    def query(self, query):
        return requests.post(self.server, params={"query": query},
                             headers={"Accept": "application/sparql-results+json"}).json()["results"]["bindings"]
    #
    # def async_query(self, query, callback):
    #     return unirest.post(self.server, params={"query": query},
    #                         headers={"Accept": "application/sparql-results+json"}, callback=callback)
