def parse_types(results):
    return set([binding["type"]["value"] for binding in results.json()["results"]["bindings"]])


def parse_instance_count(results):
    return int(results.json()["results"]["bindings"][0]["count"]["value"])
