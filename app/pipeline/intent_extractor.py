import json
import os
import re

# APPLICATION TYPE DETECTION

APPLICATION_PATTERNS = {

    "CRM": [
        "crm",
        "customer",
        "lead",
        "contact"
    ],

    "E_COMMERCE": [
        "ecommerce",
        "e-commerce",
        "store",
        "shopping",
        "product",
        "order"
    ],

    "HOSPITAL": [
        "hospital",
        "doctor",
        "patient",
        "appointment"
    ],

    "LMS": [
        "learning",
        "course",
        "student",
        "teacher"
    ],

    "INVENTORY": [
        "inventory",
        "warehouse",
        "stock"
    ],

    "CHAT": [
        "chat",
        "message",
        "conversation"
    ]
}

# FEATURES

FEATURE_PATTERNS = {

    "authentication": [
        "login",
        "signup",
        "authentication",
        "register"
    ],

    "dashboard": [
        "dashboard"
    ],

    "analytics": [
        "analytics",
        "reports",
        "insights"
    ],

    "payments": [
        "payment",
        "payments",
        "subscription",
        "premium"
    ],

    "notifications": [
        "notification",
        "email",
        "sms"
    ],

    "chat": [
        "chat",
        "message"
    ]
}

# ROLES

ROLE_PATTERNS = {

    "admin": [
        "admin",
        "administrator"
    ],

    "manager": [
        "manager"
    ],

    "teacher": [
        "teacher"
    ],

    "student": [
        "student"
    ],

    "customer": [
        "customer"
    ],

    "doctor": [
        "doctor"
    ]
}

# ENTITIES

ENTITY_PATTERNS = {

    "users": [
        "user",
        "users"
    ],

    "contacts": [
        "contact",
        "contacts"
    ],

    "products": [
        "product",
        "products"
    ],

    "orders": [
        "order",
        "orders"
    ],

    "patients": [
        "patient",
        "patients"
    ],

    "appointments": [
        "appointment",
        "appointments"
    ],

    "courses": [
        "course",
        "courses"
    ],

    "messages": [
        "message",
        "messages"
    ]
}

# UTILITIES

def find_matches(text, mapping):

    results = []

    for key, keywords in mapping.items():

        for keyword in keywords:

            if keyword in text:

                results.append(key)
                break

    return sorted(list(set(results)))

# APPLICATION DETECTION

def detect_application_type(text):

    scores = {}

    for app_type, keywords in APPLICATION_PATTERNS.items():

        score = 0

        for keyword in keywords:

            if keyword in text:
                score += 1

        scores[app_type] = score

    best_match = max(scores, key=scores.get)

    if scores[best_match] == 0:
        return "GENERIC"

    return best_match

# ASSUMPTIONS ENGINE

def generate_assumptions(features, roles):

    assumptions = []

    if "authentication" not in features:

        assumptions.append(
            "Authentication assumed for secure access."
        )

    if len(roles) == 0:

        assumptions.append(
            "User role assumed."
        )

    return assumptions

# VAGUE PROMPT DETECTION


def detect_vagueness(prompt):

    word_count = len(prompt.split())

    if word_count < 4:
        return True

    vague_terms = [
        "something",
        "app",
        "system",
        "platform"
    ]

    matches = 0

    for term in vague_terms:

        if term in prompt:
            matches += 1

    return matches >= 2

# MAIN EXTRACTION

def extract_intent(prompt: str):

    text = prompt.lower()

    application_type = detect_application_type(text)

    features = find_matches(
        text,
        FEATURE_PATTERNS
    )

    roles = find_matches(
        text,
        ROLE_PATTERNS
    )

    entities = find_matches(
        text,
        ENTITY_PATTERNS
    )

    assumptions = generate_assumptions(
        features,
        roles
    )

    vague = detect_vagueness(text)

    if vague:

        assumptions.append(
            "Prompt is vague. Default architecture will be generated."
        )

    if "user" not in roles:
        roles.append("user")

    intent = {

        "application_type": application_type,

        "features": features,

        "roles": roles,

        "entities": entities,

        "assumptions": assumptions,

        "vague_prompt": vague
    }

    os.makedirs("artifacts", exist_ok=True)

    with open(
        "artifacts/intent.json",
        "w"
    ) as f:

        json.dump(
            intent,
            f,
            indent=4
        )

    return intent