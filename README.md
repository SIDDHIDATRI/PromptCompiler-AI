# Prompt Compiler AI

A compiler-style AI system that converts natural language software requirements into structured, validated, and executable application configurations.

## Overview

Prompt Compiler AI transforms user requirements such as:

> "Build a CRM with login, contacts, dashboard, role-based access, premium plans, and analytics."

into a complete application specification containing:

* UI Schema
* API Schema
* Database Schema
* Authentication Rules
* Business Logic Rules

The system follows a multi-stage compiler architecture instead of relying on a single LLM prompt, resulting in higher reliability, consistency, and execution readiness.

---

## Problem Statement

Modern AI application generators often produce inconsistent or incomplete outputs.

This project addresses that challenge by implementing:

* Multi-stage generation pipeline
* Strict schema enforcement
* Cross-layer validation
* Automatic repair mechanisms
* Runtime execution simulation
* Evaluation framework with metrics

---

## System Architecture

Natural Language Prompt

↓

Intent Extraction

↓

System Design Layer

↓

Schema Generation

↓

Validation Engine

↓

Repair Engine

↓

Runtime Simulation

↓

Final Executable Configuration

---

## Pipeline Stages

### 1. Intent Extraction

Extracts:

* Application Type
* Features
* User Roles
* Business Entities
* Assumptions

Example:

Input:

Build CRM with login and analytics

Output:

* CRM
* Authentication
* Dashboard
* Analytics
* Admin Role

---

### 2. System Design Layer

Generates:

* Entities
* Relationships
* Workflows
* User Roles

Example:

* Users
* Contacts
* Orders
* Subscriptions

---

### 3. Schema Generation

Produces:

#### UI Schema

* Pages
* Components
* Layouts

#### API Schema

* Endpoints
* Methods
* Validations

#### Database Schema

* Tables
* Columns
* Relationships

#### Auth Schema

* Roles
* Permissions

#### Business Logic

* Access Rules
* Premium Gating
* Analytics Restrictions

---

### 4. Validation Engine

Validates:

* Required fields
* Missing keys
* Schema correctness
* Cross-layer consistency
* Hallucinated references
* Type safety

Examples:

* API entities must exist in database schema
* UI pages must have API support
* Business rules must reference valid entities

---

### 5. Repair Engine

Automatically repairs:

* Missing tables
* Missing APIs
* Missing UI pages
* Missing roles
* Invalid business logic
* Incorrect data types

Instead of regenerating the entire configuration, only the problematic sections are repaired.

---

### 6. Runtime Simulation

Executes validation against a simulated runtime environment.

Checks:

* Database deployment
* API compatibility
* Business logic execution
* Authentication rules
* UI readiness

SQLite is used to simulate application deployment.

---

## Evaluation Framework

Datasets:

### Real Product Prompts

* CRM
* E-Commerce
* LMS
* Hospital Management
* Inventory Management
* SaaS Platforms

### Edge Cases

* Vague Requirements
* Conflicting Requirements
* Missing Information
* Invalid Business Constraints

Metrics Tracked:

* Success Rate
* Retry Count
* Average Latency
* Failure Types

---

## Tech Stack

### Backend

* FastAPI
* Python

### Validation

* Pydantic

### Runtime Simulation

* SQLite

### Deployment

* Railway

---

## Project Structure

```text
PromptCompiler-AI/
│
├── app/
│   ├── main.py
│   └── pipeline/
│       ├── intent_extractor.py
│       ├── system_designer.py
│       ├── schema_generator.py
│       ├── validator.py
│       ├── repair_engine.py
│       ├── runtime_simulator.py
│       └── metrics_tracker.py
│
├── datasets/
│   ├── real_prompts.json
│   └── edge_cases.json
│
├── artifacts/
├── runtime/
├── requirements.txt
└── README.md
```

---

## Running Locally

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Start FastAPI Server

```bash
uvicorn app.main:app --reload
```

### Open Swagger Documentation

```text
http://127.0.0.1:8000/docs
```

---

## Live Demo

Swagger API Documentation:

https://promptcompiler-ai-production.up.railway.app/docs

---

## Example API Request

POST /generate

```json
{
  "prompt": "Build CRM with login, contacts, dashboard, role-based access, and premium plan with payments. Admins can see analytics."
}
```

---

## Key Features

~ Multi-stage compiler architecture

~ Deterministic pipeline

~ Strict schema enforcement

~ Validation and repair engine

~ Runtime execution simulation

~ Evaluation framework

~ Metrics tracking

~ Railway deployment

---

## Author

Siddhi Datri

MCA Student(NATIONAL INSTITUTE OF TECHNOLOGY PATNA) | AI & Data Science Enthusiast

GitHub:
https://github.com/SIDDHIDATRI

---
