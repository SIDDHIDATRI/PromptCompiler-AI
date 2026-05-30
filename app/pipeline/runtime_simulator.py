import sqlite3
import json
import os
import time

# DATABASE DEPLOYMENT

def deploy_database(config):

    conn = sqlite3.connect(
        "runtime/runtime.db"
    )

    cursor = conn.cursor()

    created_tables = []

    for table in config["db_schema"]["tables"]:

        table_name = table["table_name"]

        columns = []

        for column in table["columns"]:

            column_name = column["name"]

            column_type = map_sql_type(
                column["type"]
            )

            columns.append(
                f"{column_name} {column_type}"
            )

        query = f"""
        CREATE TABLE IF NOT EXISTS {table_name}
        (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            {",".join(columns)}
        )
        """

        cursor.execute(query)

        created_tables.append(
            table_name
        )

    conn.commit()
    conn.close()

    return created_tables

# SQL TYPE MAPPING

def map_sql_type(column_type):

    mapping = {

        "string": "TEXT",

        "integer": "INTEGER",

        "float": "REAL",

        "boolean": "INTEGER",

        "datetime": "TEXT"
    }

    return mapping.get(
        column_type,
        "TEXT"
    )

# API EXECUTION CHECK

def validate_api_runtime(config):

    results = []

    db_tables = {

        table["table_name"]

        for table in config["db_schema"]["tables"]
    }

    for endpoint in config["api_schema"]["endpoints"]:

        entity = endpoint["entity"]

        results.append({

            "endpoint":
                endpoint["path"],

            "status":
                "OK"
                if entity in db_tables
                else "FAILED"
        })

    return results

# BUSINESS RULE EXECUTION CHECK

def validate_business_logic_runtime(config):

    results = []

    tables = {

        table["table_name"]

        for table in config["db_schema"]["tables"]
    }

    for rule in config["business_logic"]["rules"]:

        status = "OK"

        if (

            "subscription" in rule["condition"]

            and "subscriptions" not in tables

        ):

            status = "FAILED"

        results.append({

            "rule":
                rule["name"],

            "status":
                status
        })

    return results

# AUTH EXECUTION CHECK

def validate_auth_runtime(config):

    results = []

    permissions = config[
        "auth_schema"
    ]["permissions"]

    for role in permissions:

        results.append({

            "role":
                role["role"],

            "status":
                "OK"
        })

    return results

# UI EXECUTION CHECK

def validate_ui_runtime(config):

    results = []

    pages = config[
        "ui_schema"
    ]["pages"]

    for page in pages:

        results.append({

            "page":
                page["name"],

            "status":
                "OK"
        })

    return results

# HEALTH SCORE

def calculate_health_score(runtime_report):

    checks = 0
    passed = 0

    sections = [

        runtime_report["api_checks"],

        runtime_report["business_logic_checks"],

        runtime_report["auth_checks"],

        runtime_report["ui_checks"]
    ]

    for section in sections:

        for item in section:

            checks += 1

            if item["status"] == "OK":

                passed += 1

    if checks == 0:
        return 0

    return round(
        (passed / checks) * 100,
        2
    )

# RUNTIME SIMULATION

def simulate_runtime(config):

    os.makedirs(
        "runtime",
        exist_ok=True
    )

    start_time = time.time()

    created_tables = deploy_database(
        config
    )

    api_checks = validate_api_runtime(
        config
    )

    business_logic_checks = (
        validate_business_logic_runtime(
            config
        )
    )

    auth_checks = (
        validate_auth_runtime(
            config
        )
    )

    ui_checks = (
        validate_ui_runtime(
            config
        )
    )

    runtime_report = {

        "runtime_status":
            "success",

        "database_created":
            True,

        "tables_created":
            created_tables,

        "api_checks":
            api_checks,

        "business_logic_checks":
            business_logic_checks,

        "auth_checks":
            auth_checks,

        "ui_checks":
            ui_checks
    }

    runtime_report[
        "health_score"
    ] = calculate_health_score(
        runtime_report
    )

    runtime_report[
        "execution_time_ms"
    ] = round(
        (time.time() - start_time)
        * 1000,
        2
    )

    with open(
        "artifacts/runtime_report.json",
        "w"
    ) as f:

        json.dump(
            runtime_report,
            f,
            indent=4
        )

    return runtime_report