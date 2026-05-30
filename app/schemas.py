from pydantic import BaseModel
from typing import List, Dict, Optional


# ==========================================================
# Intent Layer
# ==========================================================

class IntentSchema(BaseModel):
    application_type: str
    features: List[str]
    roles: List[str]
    entities: List[str]
    assumptions: List[str]


# ==========================================================
# Architecture Layer
# ==========================================================

class EntitySchema(BaseModel):
    name: str
    fields: List[str]


class WorkflowSchema(BaseModel):
    name: str
    steps: List[str]


class ArchitectureSchema(BaseModel):
    entities: List[EntitySchema]
    workflows: List[WorkflowSchema]
    roles: List[str]


# ==========================================================
# UI Layer
# ==========================================================

class UIComponent(BaseModel):
    type: str
    label: str
    api_binding: Optional[str] = None


class UIPage(BaseModel):
    name: str
    components: List[UIComponent]


class UISchema(BaseModel):
    pages: List[UIPage]


# ==========================================================
# API Layer
# ==========================================================

class ValidationRule(BaseModel):
    field: str
    rule: str


class APIEndpoint(BaseModel):
    path: str
    method: str
    entity: str
    validations: List[ValidationRule]


class APISchema(BaseModel):
    endpoints: List[APIEndpoint]


# ==========================================================
# Database Layer
# ==========================================================

class ColumnSchema(BaseModel):
    name: str
    type: str


class RelationSchema(BaseModel):
    table: str
    relation_type: str


class TableSchema(BaseModel):
    table_name: str
    columns: List[ColumnSchema]
    relations: List[RelationSchema] = []


class DatabaseSchema(BaseModel):
    tables: List[TableSchema]


# ==========================================================
# Auth Layer
# ==========================================================

class PermissionSchema(BaseModel):
    role: str
    permissions: List[str]


class AuthSchema(BaseModel):
    permissions: List[PermissionSchema]


# ==========================================================
# Business Logic Layer
# ==========================================================

class BusinessRule(BaseModel):
    name: str
    condition: str
    action: str


class BusinessLogicSchema(BaseModel):
    rules: List[BusinessRule]


# ==========================================================
# Validation Layer
# ==========================================================

class ValidationReport(BaseModel):
    valid: bool
    errors: List[str]
    warnings: List[str]


# ==========================================================
# Runtime Layer
# ==========================================================

class RuntimeResult(BaseModel):
    runtime_status: str
    database_created: bool
    tables_created: List[str]


# ==========================================================
# Final Application Config
# ==========================================================

class AppConfig(BaseModel):

    ui_schema: UISchema

    api_schema: APISchema

    db_schema: DatabaseSchema

    auth_schema: AuthSchema

    business_logic: BusinessLogicSchema


# ==========================================================
# Evaluation Metrics
# ==========================================================

class MetricsSchema(BaseModel):

    total_requests: int

    success_count: int

    failure_count: int

    average_latency_ms: float

    retry_count: int

    failure_types: Dict[str, int]
