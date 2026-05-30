import json
import os

# HELPERS

def get_db_tables(config):

    return [

        table["table_name"]

        for table in config["db_schema"]["tables"]
    ]


def get_api_entities(config):

    return list(

        set(

            endpoint["entity"]

            for endpoint in config["api_schema"]["endpoints"]
        )

    )


def get_ui_pages(config):

    return [

        page["name"]

        for page in config["ui_schema"]["pages"]
    ]


def get_roles(config):

    return [

        permission["role"]

        for permission in config["auth_schema"]["permissions"]
    ]

# DB REPAIR

def repair_missing_tables(config):

    db_tables = set(
        get_db_tables(config)
    )

    api_entities = set(
        get_api_entities(config)
    )

    repaired = []

    for entity in api_entities:

        if entity not in db_tables:

            config["db_schema"]["tables"].append({

                "table_name": entity,

                "columns": [

                    {
                        "name": "id",
                        "type": "integer"
                    },

                    {
                        "name": "name",
                        "type": "string"
                    }
                ],

                "relations": []
            })

            repaired.append(
                f"Created table {entity}"
            )

    return repaired

# API REPAIR


def repair_missing_api(config):

    db_tables = set(
        get_db_tables(config)
    )

    api_entities = set(
        get_api_entities(config)
    )

    repaired = []

    for table in db_tables:

        if table not in api_entities:

            config["api_schema"]["endpoints"].extend([

                {
                    "path": f"/{table}",
                    "method": "GET",
                    "entity": table,
                    "validations": []
                },

                {
                    "path": f"/{table}",
                    "method": "POST",
                    "entity": table,
                    "validations": []
                }
            ])

            repaired.append(
                f"Created API for {table}"
            )

    return repaired

# UI REPAIR

def repair_missing_ui(config):

    api_entities = set(
        get_api_entities(config)
    )

    pages = set(
        get_ui_pages(config)
    )

    repaired = []

    ignored_pages = {
        "users"
    }

    for entity in api_entities:

        if entity in ignored_pages:
            continue

        if entity not in pages:

            config["ui_schema"]["pages"].append({

                "name": entity,

                "components": [

                    {
                        "type": "table",
                        "label": entity
                    }
                ]
            })

            repaired.append(
                f"Created UI page {entity}"
            )

    return repaired

# AUTH REPAIR

def repair_auth(config):

    permissions = config["auth_schema"]["permissions"]

    roles = set(
        get_roles(config)
    )

    repaired = []

    if "user" not in roles:

        permissions.append({

            "role": "user",

            "permissions": [
                "view_dashboard"
            ]
        })

        repaired.append(
            "Added user role"
        )

    return repaired

# BUSINESS RULE REPAIR

def repair_business_logic(config):

    repaired = []

    rules = config["business_logic"]["rules"]

    db_tables = set(
        get_db_tables(config)
    )

    has_subscription_rule = any(
        rule["name"] == "premium_access"
        for rule in rules
    )

    if (

        "subscriptions" in db_tables
        and not has_subscription_rule

    ):

        rules.append({

            "name": "premium_access",

            "condition":
                "subscription.status == active",

            "action":
                "allow_premium_features"
        })

        repaired.append(
            "Added premium access rule"
        )

    return repaired

# HALLUCINATION REPAIR

def repair_hallucinations(config):

    repaired = []

    db_tables = set(
        get_db_tables(config)
    )

    rules = config["business_logic"]["rules"]

    valid_rules = []

    for rule in rules:

        condition = rule["condition"]

        if (

            "subscription" in condition
            and "subscriptions" not in db_tables

        ):

            repaired.append(

                "Removed invalid subscription rule"

            )

            continue

        valid_rules.append(rule)

    config["business_logic"]["rules"] = valid_rules

    return repaired

# COLUMN TYPE REPAIR

def repair_column_types(config):

    repaired = []

    allowed_types = {

        "string",
        "integer",
        "float",
        "boolean",
        "datetime"
    }

    for table in config["db_schema"]["tables"]:

        for column in table["columns"]:

            if column["type"] not in allowed_types:

                old_type = column["type"]

                column["type"] = "string"

                repaired.append(

                    f"Fixed invalid type "
                    f"{old_type} -> string"

                )

    return repaired

# MASTER REPAIR


def repair_config(config, validation_result):

    repair_log = []

    repair_log.extend(
        repair_missing_tables(config)
    )

    repair_log.extend(
        repair_missing_api(config)
    )

    repair_log.extend(
        repair_missing_ui(config)
    )

    repair_log.extend(
        repair_auth(config)
    )

    repair_log.extend(
        repair_business_logic(config)
    )

    repair_log.extend(
        repair_hallucinations(config)
    )

    repair_log.extend(
        repair_column_types(config)
    )

    os.makedirs(
        "artifacts",
        exist_ok=True
    )

    with open(
        "artifacts/repair_log.json",
        "w"
    ) as f:

        json.dump(
            {
                "repairs": repair_log
            },
            f,
            indent=4
        )

    return config