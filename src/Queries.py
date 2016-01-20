SUB_CLASS_PROPERTY_PATH = """SELECT distinct ?type WHERE {{
          <{}> rdfs:subClassOf+ ?type
        }}""".replace('\n', '')

TYPES = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT ?type
            WHERE {{ <{}> rdf:type ?type}}
        """.replace('\n', '')

INSTANCE_COUNT = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT (COUNT(?instance) as ?count)
            WHERE {{ ?instance rdf:type <{}> }}
        """.replace('\n', '')

SUB_CLASS = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT *
            WHERE {{ <{}> rdfs:subClassOf ?type }}
        """.replace('\n', '')

SHARED_INSTANCE_COUNT = """
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            SELECT (COUNT(?instance) as ?count)
            WHERE {{ ?instance rdf:type <{}>. ?instance rdf:type <{}>}}
        """.replace('\n', '')

INSERTION = """
            INSERT DATA
            {{
              {} {} {} .
            }}
        """.replace('\n', '')
