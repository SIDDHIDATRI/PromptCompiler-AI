import json
import os

# UI GENERATION

def generate_ui_schema(architecture):

    pages = []

    entity_names = [
        entity["name"]
        for entity in architecture["entities"]
    ]

    # Dashboard
    if any(
        workflow["name"] == "dashboard_flow"
        for workflow in architecture["workflows"]
    ):

        pages.append({
            "name": "dashboard",
            "components": [
                {
                    "type": "sidebar",
                    "label": "Navigation"
                },
                {
                    "type": "analytics_chart",
                    "label": "Analytics"
                }
            ]
        })

    # Login
    if any(
        workflow["name"] == "authentication_flow"
        for workflow in architecture["workflows"]
    ):

        pages.append({
            "name": "login",
            "components": [
                {
                    "type": "input",
                    "label": "email"
                },
                {
                    "type": "input",
                    "label": "password"
                },
                {
                    "type": "button",
                    "label": "Login"
                }
            ]
        })

    # Entity Pages
    for entity in entity_names:

        if entity == "users":
            continue

        pages.append({
            "name": entity,
            "components": [
                {
                    "type": "table",
                    "label": entity
                },
                {
                    "type": "create_button",
                    "label": f"Create {entity}"
                }
            ]
        })

    return {
        "pages": pages
    }

# API GENERATION

def generate_api_schema(architecture):

    endpoints = []

    entity_names = [
        entity["name"]
        for entity in architecture["entities"]
    ]

    # Authentication
    if any(
        workflow["name"] == "authentication_flow"
        for workflow in architecture["workflows"]
    ):

        endpoints.append({
            "path": "/login",
            "method": "POST",
            "entity": "users",
            "validations": [
                {
                    "field": "email",
                    "rule": "required"
                },
                {
                    "field": "password",
                    "rule": "required"
                }
            ]
        })

    # CRUD APIs
    for entity in entity_names:

        endpoints.extend([

            {
                "path": f"/{entity}",
                "method": "GET",
                "entity": entity,
                "validations": []
            },

            {
                "path": f"/{entity}",
                "method": "POST",
                "entity": entity,
                "validations": []
            },

            {
                "path": f"/{entity}/{{id}}",
                "method": "PUT",
                "entity": entity,
                "validations": []
            },

            {
                "path": f"/{entity}/{{id}}",
                "method": "DELETE",
                "entity": entity,
                "validations": []
            }
        ])

    return {
        "endpoints": endpoints
    }

# DATABASE GENERATION

def generate_db_schema(architecture):

    tables = []

    for entity in architecture["entities"]:

        columns = []

        for field in entity["fields"]:

            columns.append({
                "name": field,
                "type": "string"
            })

        tables.append({

            "table_name": entity["name"],

            "columns": columns,

            "relations": []
        })

    # Relations
    for relation in architecture["relations"]:

        for table in tables:

            if table["table_name"] == relation["from"]:

                table["relations"].append({

                    "table": relation["to"],

                    "relation_type": relation["type"]
                })

    return {
        "tables": tables
    }

# AUTH GENERATION

def generate_auth_schema(architecture):

    permissions = []

    roles = architecture["roles"]

    for role in roles:

        role_permissions = []

        role_permissions.append(
            "view_dashboard"
        )

        if role == "admin":

            role_permissions.extend([
                "manage_users",
                "manage_system",
                "view_analytics"
            ])

        if role == "manager":

            role_permissions.extend([
                "manage_records"
            ])

        permissions.append({

            "role": role,

            "permissions": role_permissions
        })

    return {
        "permissions": permissions
    }

# BUSINESS LOGIC GENERATION


def generate_business_logic(architecture):

    rules = []

    entity_names = [
        entity["name"]
        for entity in architecture["entities"]
    ]

    # Premium Gating
    if "subscriptions" in entity_names:

        rules.append({

            "name": "premium_access",

            "condition":
                "subscription.status == active",

            "action":
                "allow_premium_features"
        })

    # Analytics Restriction
    if "admin" in architecture["roles"]:

        rules.append({

            "name": "analytics_access",

            "condition":
                "role == admin",

            "action":
                "allow_analytics"
        })

    # Authentication
    if any(
        workflow["name"] == "authentication_flow"
        for workflow in architecture["workflows"]
    ):

        rules.append({

            "name": "authenticated_access",

            "condition":
                "user.logged_in",

            "action":
                "grant_access"
        })

    return {
        "rules": rules
    }

# COMPLETE CONFIG

def generate_complete_schema(architecture):

    config = {

        "ui_schema":
            generate_ui_schema(
                architecture
            ),

        "api_schema":
            generate_api_schema(
                architecture
            ),

        "db_schema":
            generate_db_schema(
                architecture
            ),

        "auth_schema":
            generate_auth_schema(
                architecture
            ),

        "business_logic":
            generate_business_logic(
                architecture
            )
    }

    os.makedirs(
        "artifacts",
        exist_ok=True
    )

    with open(
        "artifacts/final_config.json",
        "w"
    ) as f:

        json.dump(
            config,
            f,
            indent=4
        )

    return config