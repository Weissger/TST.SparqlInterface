import requests

from .SparqlInterface.Interfaces.AbstractInterface import SparqlConnectionError
from SparqlInterface.Interfaces import AbstractInterface


__author__ = 'tmy'


class Blazegraph(AbstractInterface):
    def __init__(self, server):
        self.server = server

    def get_sub_class_of_objects_recursive(self, rdf_type):
        query = """SELECT ?class WHERE {{
          <{}> rdfs:subClassOf ?class
        }}""".replace('\n', '')
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
                new_c = o["class"]["value"]
                if new_c not in done_list and new_c not in more:
                    more.append(new_c)
        return done_list

    def get_sub_class_of_objects_ppath(self, rdf_type):
        query = """SELECT distinct ?class WHERE {{
          <{}> rdfs:subClassOf+ ?class
        }}""".replace('\n', '')
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
            done_list.append(o["class"]["value"])
        return done_list

    def get_types(self, instance):
        query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT ?type
            WHERE { <""" + instance + """> rdf:type ?type}
        """
        return set([binding["type"]["value"] for binding in requests.post(self.server, params={"query": query},
                                                                          headers={
                                                                              "Accept": "application/sparql-results+json"}).json()[
            "results"]["bindings"]])

    def count_instances(self, rdf_type):
        query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT (COUNT(?instance) as ?count)
            WHERE { ?instance rdf:type <""" + rdf_type + """> }
        """
        return int(requests.post(self.server, params={"query": query},
                                 headers={"Accept": "application/sparql-results+json"}).json()["results"]["bindings"][
            0]["count"]["value"])

    def get_sub_class_of_objects(self, rdf_type):
        query = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT *
            WHERE { <""" + rdf_type + """> rdfs:subClassOf ?class }
        """
        return set([binding["class"]["value"] for binding in requests.post(self.server, params={"query": query},
                                                                           headers={
                                                                               "Accept": "application/sparql-results+json"}).json()[
            "results"]["bindings"]])

    def count_shared_instances(self, rdf_type, other_type):
        query = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT (COUNT(?instance) as ?count)
            WHERE { ?instance rdf:type <""" + rdf_type + """>. ?instance rdf:type <""" + other_type + """>}
        """
        return int(requests.post(self.server, params={"query": query},
                                 headers={"Accept": "application/sparql-results+json"}).json()["results"]["bindings"][
            0]["count"]["value"])

    def insert_triple(self, subject, predicate, obj):
        query = """
            INSERT DATA
            {
              {} {} {} .
            }
        """.format(subject, predicate, obj)
        return requests.post(self.server, params={"query": query})