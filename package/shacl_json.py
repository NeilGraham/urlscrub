import re

from rdflib import Graph, Namespace
from rdflib.term import URIRef, BNode, Literal
from rdflib.namespace import SH, RDF, XSD

meta = Namespace("metadata:")


def get_one(l: list, description: str, allow_empty: bool = False):
    """Returns first element of list, or None if empty and 'allow_empty' is True.
    If list is not as expected, throws error with description provided.

    Args:
        l (list): List to return 1 item from.
        description (str): Description of list to be used in error message.
        allow_empty (bool, optional): Allow list to be of length 0.
            Defaults to False.

    Raises:
        ValueError: _description_

    Returns:
        _type_: _description_
    """
    if (allow_empty and len(l) > 1) or len(l) != 1:
        raise ValueError(f"Expected 1 {description}. Got {len(l)}.")

    if allow_empty and len(l) == 0:
        return None
    else:
        return l[0]


def json_to_graph(
    json: dict, shacl_graph: Graph, target_node_shape: URIRef, data_graph: Graph = None
) -> Graph:
    """Parse JSON into an RDF graph with respect to a sh:NodeShape definition.

    Args:
        json (dict): _description_
        shacl_graph (Graph): Graph containing sh:NodeShape definition.
        target_node_shape (URIRef): sh:NodeShape URI to use for parsing.
        data_graph (Graph, optional): Graph to parse data into. Defaults to None.

    Raises:
        ValueError: 'target_node_shape' is not defined in 'shacl_graph'.
        ValueError: Subject URI references variables that are not in JSON
        ValueError: Cannot specify both sh:datatype and sh:node on a single 
            sh:property.

    Returns:
        Graph: 'data_graph' with data from JSON added.
    """
    if data_graph == None:
        data_graph = Graph()

    # If 'target_node_shape' definition does not exist in 'shacl_graph', raise error.
    if not (len(shacl_graph.triples((target_node_shape, RDF.type, SH.NodeShape))) > 0):
        raise ValueError(
            f"Target node shape does not exist in SHACL graph: "
            + target_node_shape.n3()
        )

    # Get subject URI from 'meta:subjectURI', else use Blank Node.
    subject_uri = (
        get_one(
            shacl_graph.objects(target_node_shape, meta + "subjectURI"),
            f"meta:subjectURI for {target_node_shape.n3()}",
            allow_empty=True,
        )  # Get the object of the triple returned.
        or BNode()  # If no triples returned, use Blank Node.
    )
    # If subject URI specified on 'meta:subjectURI', see if variables are referenced.
    if type(subject_uri) == URIRef:
        uri_construct = subject_uri.n3()[1:-1]
        variables_referenced = re.findall(
            r"(?<={)[a-zA-Z][_a-zA-Z0-9]*(?=})", subject_uri
        )
        # If variables are referenced, replace with values from 'json'.
        if len(variables_referenced) > 0:
            # If 'json' does not contain any variables specified, raise error.
            if any(variable not in json for variable in variables_referenced):
                raise ValueError(
                    "Subject URI references variables that are not in JSON: '"
                    + "', '".join(filter(lambda v: v not in json, variables_referenced))
                    + "'."
                )
            # Replace variables in subject URI with values from JSON.
            for variable in variables_referenced:
                uri_construct = uri_construct.replace(f"{{{variable}}}", json[variable])
            # Replace 'subject_uri' with replaced variable string.
            subject_uri = URIRef(uri_construct)

    # Add 'rdf:type' statements to 'data_graph'.
    for type_uri in shacl_graph.objects(target_node_shape, SH.targetClass):
        data_graph.add((subject_uri, RDF.type, type_uri))

    # Add triples to 'data_graph' for each property specified.
    for property_uri in shacl_graph.objects(target_node_shape, SH.property):
        prop_predicates = {
            "path": (SH.path, True),
            "variable": (meta + "variable", True),
            # "min_count": (SH.minCount, False),
            # "max_count": (SH.maxCount, False),
            "datatype": (SH.datatype, False),
            "node": (SH.node, False),
        }
        props = {
            prop: get_one(
                shacl_graph.objects(property_uri, predicate_uri),
                description=(
                    f"predicate {predicate_uri.n3()} on sh:property "
                    f"{property_uri.n3()}, sh:NodeShape {target_node_shape.n3()}."
                ),
                allow_empty=not required,
            )
            for prop, [predicate_uri, required] in prop_predicates.items()
        }
        if props["datatype"] and props["node"]:
            raise ValueError(
                "Cannot specify both sh:datatype and sh:node on a single sh:property."
                f"Subject URI: {subject_uri.n3()}. sh:property URI: {property_uri.n3()}."
            )

        json_value_list = json[props["variable"]]
        if type(json_value_list) != list:
            json_value_list = [json_value_list]
        for value in json_value_list:
            if props["node"]:
                json_to_graph(value, shacl_graph, props["node"], data_graph)
            elif props["datatype"]:
                object_uri = (
                    URIRef(value)
                    if props["datatype"] == XSD.anyURI
                    else Literal(value, datatype=props["datatype"])
                )
                data_graph.add((subject_uri, props["path"], object_uri))
            else:
                data_graph.add((subject_uri, props["path"], Literal(value)))

    return data_graph
