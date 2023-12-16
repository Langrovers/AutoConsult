# Prompt for processing customers' profiles
customer_prompt_template = """Automotive Customer and Vehicle Relationship Template
Extract the following Entities & relationships described in the mentioned format 
0. ALWAYS FINISH THE OUTPUT. Never send partial responses
1. First, look for these Entity types in the text and generate as comma-separated format similar to entity type.
    - label: 'Customer', id: string, name: string, age: int, sex: string, occupation: string, dealer: string, action: string, licenseDuration: int, customerTenure: int
    - label: 'Vehicle', id: string, model: string

2. Next generate each relationships as triples of head, relationship and tail. To refer the head and tail entity, use their respective `id` property. 
Relationship property should be mentioned within brackets as comma-separated. 
They should follow these relationship types below. You will have to generate as many relationships as needed as defined below:

    - customer|OWNS|vehicle

3. Output Example:

{
    "entities": [
        {"label": "Customer", "id": "custCanan", "name": "Canan Yilmaz", "age": 28, "sex": "Female", "occupation": "Chef", "dealer": "Izmir", "action": "Vehicle Purchase", "licenseDuration": 10, "customerTenure": 2},
        {"label": "Vehicle", "id": "vehicleI8", "model": "BMW i8"},
    ],
    "relationships": [
        "custCanan|OWNS|vehicleI8",
    ]
}

Case Sheet:
$ctext
"""

# Prompt for processing dealers
action_dealer_template = """Automotive Dealer Interaction Analysis Template

Analyze dealer interactions with the following entities and relationships:
Extract the following Entities & relationships described in the mentioned format 
0. ALWAYS FINISH THE OUTPUT. Never send partial responses
1. First, look for these Entity types in the text and generate as comma-separated format similar to entity type.
Do NOT add any car type to dealer "id". it should be dealer and dealer location example: (dealerAnkara, dealerIzmir)
    - label: 'Dealer', id: string, name: string
    - label: 'Vehicle', id: string, model: string
    - label: 'Service', id: string, type: string
    - label: 'Feedback', id: string, comment: string


2. Next generate each relationships as triples of head, relationship and tail. To refer the head and tail entity, use their respective `id` property. 
Relationship property should be mentioned within brackets as comma-separated. 
They should follow these relationship types below. You will have to generate as many relationships as needed as defined below:

    - dealer|PROVIDES_SERVICE_FOR_VEHICLE|vehicle
    - vehicle|HAS_SERVICE|service

3. Output Example:

{
    "entities": [
        {"label": "Dealer", "id": "dealerAnkara", "name": "Ankara"},
        {"label": "Vehicle", "id": "vehicleI8", "model": "BMW i8"},
        {"label": "Service", "id": "service0823", "type": "Scheduled Maintenance"},
        {"label": "Feedback", "id": "feedback0823", "comment": "Efficient service"}
    ],
    "relationships": [
        "dealerAnkara|PROVIDES_SERVICE_FOR_VEHICLE|vehicleI8",
        "vehicleI8|HAS_SERVICE|service0823",
    ]
}

Case Sheet:
$ctext
"""
CYPHER_QA_TEMPLATE = """You are an assistant that helps to form nice and human understandable answers.
The information part contains the provided information that you must use to construct an answer.
The provided information is authoritative, you must never doubt it or try to use your internal knowledge to correct it.
Make the answer sound as a response to the question. Do not mention that you based the result on the given information.
If the provided information is empty, say that you don't know the answer.
Final answer should be easily readable and structured.
Information:
{context}

Question: {question}
Helpful Answer:"""

cypher_generation_template = """Cypher Generation Template for Vehicle Dealership Database:

You are a skilled Neo4j Cypher query creator who transforms natural language requests into Cypher queries based on a specific Neo4j schema related to a vehicle dealership database. Follow these instructions for query creation:
1. The Cypher queries should be compatible with Neo4j Version 5.
2. Avoid using EXISTS, SIZE, HAVING keywords. Use aliases when employing the WITH keyword.
3. Only use Nodes and relationships that are present in the provided schema.
4. Conduct case-insensitive and fuzzy searches for property-related queries. For example, use `toLower(customer.name) contains 'john doe'` for customer searches.
5. Do not use relationships not mentioned in the given schema.


schema: {schema}

Schema Details:
- Customer (id, name, age, sex, occupation, dealer, action, licenseDuration, customerTenure)
- Vehicle (id, model)
- Dealer (id, name)
- Service (id, type)
- Feedback (id, comment)
- Relationships: Customer-[OWNS]->Vehicle, Dealer-[PROVIDES_SERVICE_FOR_VEHICLE]->Vehicle, Vehicle-[HAS_SERVICE]->Service

Example Questions and Cypher Answers:

Question: Find all vehicles owned by customers over 40 years old.
Answer: ```MATCH (c:Customer)-[:OWNS]->(v:Vehicle) WHERE c.age > 40 RETURN v.model AS VehicleModel, c.name AS OwnerName```

Question: Which dealers provide service for BMW vehicles?
Answer: ```MATCH (d:Dealer)-[:PROVIDES_SERVICE_FOR_VEHICLE]->(v:Vehicle) WHERE toLower(v.model) contains 'bmw' RETURN d.name AS DealerName, v.model AS VehicleModel```

Your Question: {question}
"""

