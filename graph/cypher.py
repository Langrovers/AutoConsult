def generate_cypher(json_obj):
    """Generates Cypher statements for Neo4j graph database from a JSON object.

        Processes each entity and relationship in the JSON object to create Cypher MERGE statements.
        Entities are added with their attributes, and relationships are established between them.

        Args:
            json_obj (list of dict): A list of dictionaries representing entities and relationships in the JSON object.

        Returns:
            list: A list of Cypher statements generated from the JSON object.

        Writes:
            A file 'cyphers.txt' containing all generated Cypher statements.
        """
    e_statements = []
    r_statements = []

    e_label_map = {}

    # loop through our json object
    for i, obj in enumerate(json_obj):
        print(f"Generating cypher for file {i+1} of {len(json_obj)}")
        for entity in obj["entities"]:
            label = entity["label"]
            id = entity["id"]
            id = id.replace("-", "").replace("_", "")
            properties = {k: v for k, v in entity.items() if k not in ["label", "id"]}

            cypher = f'MERGE (n:{label} {{id: "{id}"}})'
            if properties:
                props_str = ", ".join(
                    [f'n.{key} = "{val}"' for key, val in properties.items()]
                )
                cypher += f" ON CREATE SET {props_str}"
            e_statements.append(cypher)
            e_label_map[id] = label

        for rs in obj["relationships"]:
            src_id, rs_type, tgt_id = rs.split("|")
            src_id = src_id.replace("-", "").replace("_", "")
            tgt_id = tgt_id.replace("-", "").replace("_", "")

            src_label = e_label_map[src_id]
            tgt_label = e_label_map[tgt_id]

            cypher = f'MERGE (a:{src_label} {{id: "{src_id}"}}) MERGE (b:{tgt_label} {{id: "{tgt_id}"}}) MERGE (a)-[:{rs_type}]->(b)'
            r_statements.append(cypher)

    with open("cyphers.txt", "w") as outfile:
        outfile.write("\n".join(e_statements + r_statements))

    return e_statements + r_statements