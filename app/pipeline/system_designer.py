import json
import os

# DEFAULT ENTITY FIELDS

ENTITY_FIELDS = {

    "users": [
        "name",
        "email",
        "password"
    ],

    "contacts": [
        "first_name",
        "last_name",
        "email",
        "phone"
    ],

    "products": [
        "title",
        "price",
        "description"
    ],

    "orders": [
        "user_id",
        "total_amount",
        "status"
    ],

    "patients": [
        "name",
        "age",
        "medical_history"
    ],

    "appointments": [
        "patient_id",
        "doctor_id",
        "appointment_date"
    ],

    "courses": [
        "title",
        "description",
        "teacher_id"
    ],

    "messages": [
        "sender_id",
        "receiver_id",
        "message"
    ],

    "subscriptions": [
        "user_id",
        "plan",
        "status"
    ],

    "analytics": [
        "event_name",
        "event_value"
    ]
}

# FEATURE → ENTITY MAPPING

FEATURE_ENTITY_MAP = {

    "payments": [
        "subscriptions",
        "orders"
    ],

    "analytics": [
        "analytics"
    ],

    "chat": [
        "messages"
    ]
}
# WORKFLOW BUILDERS

def build_auth_workflow():

    return {
        "name": "authentication_flow",
        "steps": [
            "user_login",
            "credential_validation",
            "session_creation"
        ]
    }


def build_payment_workflow():

    return {
        "name": "payment_flow",
        "steps": [
            "plan_selection",
            "payment_processing",
            "subscription_activation"
        ]
    }


def build_dashboard_workflow():

    return {
        "name": "dashboard_flow",
        "steps": [
            "fetch_metrics",
            "load_widgets",
            "render_dashboard"
        ]
    }


def build_chat_workflow():

    return {
        "name": "chat_flow",
        "steps": [
            "message_send",
            "message_store",
            "message_delivery"
        ]
    }

# ENTITY GENERATION

def generate_entities(intent):

    entities = []

    detected_entities = set(intent["entities"])

    # Always include users
    detected_entities.add("users")

    # Add entities from features
    for feature in intent["features"]:

        if feature in FEATURE_ENTITY_MAP:

            for entity in FEATURE_ENTITY_MAP[feature]:

                detected_entities.add(entity)

    # Build entity objects
    for entity_name in sorted(detected_entities):

        entity = {
            "name": entity_name,
            "fields": ENTITY_FIELDS.get(
                entity_name,
                ["name"]
            )
        }

        entities.append(entity)

    return entities

# RELATION GENERATION

def generate_relations(entities):

    relations = []

    entity_names = [
        entity["name"]
        for entity in entities
    ]

    if "users" in entity_names and "orders" in entity_names:

        relations.append({
            "from": "users",
            "to": "orders",
            "type": "one_to_many"
        })

    if "users" in entity_names and "subscriptions" in entity_names:

        relations.append({
            "from": "users",
            "to": "subscriptions",
            "type": "one_to_one"
        })

    if "patients" in entity_names and "appointments" in entity_names:

        relations.append({
            "from": "patients",
            "to": "appointments",
            "type": "one_to_many"
        })

    return relations

# WORKFLOW GENERATION

def generate_workflows(intent):

    workflows = []

    features = intent["features"]

    if "authentication" in features:

        workflows.append(
            build_auth_workflow()
        )

    if "payments" in features:

        workflows.append(
            build_payment_workflow()
        )

    if "dashboard" in features:

        workflows.append(
            build_dashboard_workflow()
        )

    if "chat" in features:

        workflows.append(
            build_chat_workflow()
        )

    return workflows

# ARCHITECTURE DESIGN

def design_architecture(intent):

    entities = generate_entities(intent)

    workflows = generate_workflows(intent)

    relations = generate_relations(entities)

    architecture = {

        "application_type": intent["application_type"],

        "entities": entities,

        "relations": relations,

        "workflows": workflows,

        "roles": intent["roles"],

        "assumptions": intent["assumptions"],

        "vague_prompt": intent["vague_prompt"]
    }

    os.makedirs(
        "artifacts",
        exist_ok=True
    )

    with open(
        "artifacts/architecture.json",
        "w"
    ) as f:

        json.dump(
            architecture,
            f,
            indent=4
        )

    return architecture