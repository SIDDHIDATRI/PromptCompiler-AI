from typing import Dict, List

# REQUIRED ROOT KEYS

REQUIRED_CONFIG_KEYS = [

    "ui_schema",

    "api_schema",

    "db_schema",

    "auth_schema",

    "business_logic"
]

# HELPER FUNCTIONS

def get_table_names(config):

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


# ROOT STRUCTURE VALIDATION


def validate_root_structure(config, errors):

    for key in REQUIRED_CONFIG_KEYS:

        if key not in config:

            errors.append(
                f"Missing root key: {key}"
            )


# DATABASE VALIDATION

def validate_database(config, errors):

    tables = config["db_schema"]["tables"]

    if len(tables) == 0:

        errors.append(
            "Database contains no tables"
        )

    for table in tables:

        if "table_name" not in table:

            errors.append(
                "Table missing table_name"
            )

        if "columns" not in table:

            errors.append(
                f"{table.get('table_name')} missing columns"
            )

        if len(table.get("columns", [])) == 0:

            errors.append(
                f"{table['table_name']} has no columns"
            )

# API VALIDATION

def validate_api(config, errors):

    endpoints = config["api_schema"]["endpoints"]

    if len(endpoints) == 0:

        errors.append(
            "No API endpoints generated"
        )

    for endpoint in endpoints:

        if "path" not in endpoint:

            errors.append(
                "API endpoint missing path"
            )

        if "method" not in endpoint:

            errors.append(
                "API endpoint missing method"
            )

        if "entity" not in endpoint:

            errors.append(
                "API endpoint missing entity"
            )


# UI VALIDATION

def validate_ui(config, errors):

    pages = config["ui_schema"]["pages"]

    if len(pages) == 0:

        errors.append(
            "No UI pages generated"
        )

    for page in pages:

        if "name" not in page:

            errors.append(
                "Page missing name"
            )

        if "components" not in page:

            errors.append(
                f"{page.get('name')} missing components"
            )

# AUTH VALIDATION

def validate_auth(config, errors):

    permissions = config["auth_schema"]["permissions"]

    if len(permissions) == 0:

        errors.append(
            "No auth permissions generated"
        )

    for permission in permissions:

        if "role" not in permission:

            errors.append(
                "Permission missing role"
            )

        if "permissions" not in permission:

            errors.append(
                "Permission list missing"
            )

# BUSINESS RULE VALIDATION

def validate_business_logic(config, errors):

    rules = config["business_logic"]["rules"]

    for rule in rules:

        if "name" not in rule:

            errors.append(
                "Business rule missing name"
            )

        if "condition" not in rule:

            errors.append(
                "Business rule missing condition"
            )

        if "action" not in rule:

            errors.append(
                "Business rule missing action"
            )

# API ↔ DATABASE CONSISTENCY

def validate_api_db_consistency(config, errors):

    db_tables = set(
        get_table_names(config)
    )

    api_entities = set(
        get_api_entities(config)
    )

    for entity in api_entities:

        if entity not in db_tables:

            errors.append(

                f"API entity '{entity}' "
                f"does not exist in DB schema"

            )

# UI ↔ API CONSISTENCY

def validate_ui_api_consistency(config, errors):

    ui_pages = set(
        get_ui_pages(config)
    )

    api_entities = set(
        get_api_entities(config)
    )

    ignored_pages = {
        "login",
        "dashboard"
    }

    for page in ui_pages:

        if page in ignored_pages:
            continue

        if page not in api_entities:

            errors.append(

                f"UI page '{page}' "
                f"has no API support"

            )

# AUTH ↔ BUSINESS LOGIC CONSISTENCY

def validate_auth_business_logic(config, errors):

    roles = set(
        get_roles(config)
    )

    rules = config["business_logic"]["rules"]

    for rule in rules:

        condition = rule["condition"]

        if "role ==" in condition:

            role = (

                condition
                .replace("role ==", "")
                .strip()

            )

            if role not in roles:

                errors.append(

                    f"Business rule "
                    f"references unknown role '{role}'"

                )

# HALLUCINATION DETECTION

def validate_hallucinations(config, errors):

    db_tables = set(
        get_table_names(config)
    )

    rules = config["business_logic"]["rules"]

    for rule in rules:

        condition = rule["condition"]

        if "subscription" in condition:

            if "subscriptions" not in db_tables:

                errors.append(

                    "Business logic references "
                    "subscriptions table "
                    "that does not exist"

                )

# TYPE SAFETY CHECK

def validate_column_types(config, errors):

    allowed_types = {

        "string",

        "integer",

        "float",

        "boolean",

        "datetime"
    }

    tables = config["db_schema"]["tables"]

    for table in tables:

        for column in table["columns"]:

            if column["type"] not in allowed_types:

                errors.append(

                    f"Invalid type "
                    f"'{column['type']}' "
                    f"in table "
                    f"'{table['table_name']}'"

                )

# MASTER VALIDATION

def validate_config(config):

    errors = []

    warnings = []

    validate_root_structure(
        config,
        errors
    )

    if errors:

        return {

            "valid": False,

            "errors": errors,

            "warnings": warnings
        }

    validate_database(
        config,
        errors
    )

    validate_api(
        config,
        errors
    )

    validate_ui(
        config,
        errors
    )

    validate_auth(
        config,
        errors
    )

    validate_business_logic(
        config,
        errors
    )

    validate_api_db_consistency(
        config,
        errors
    )

    validate_ui_api_consistency(
        config,
        errors
    )

    validate_auth_business_logic(
        config,
        errors
    )

    validate_hallucinations(
        config,
        errors
    )

    validate_column_types(
        config,
        errors
    )

    return {

        "valid": len(errors) == 0,

        "errors": errors,

        "warnings": warnings
    }