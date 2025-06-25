# Enterprise RAG Backend

## Table of Contents

* [1. Overview](#1-overview)
* [2. Business Requirements](#2-business-requirements)
* [3. Technical Requirements](#3-technical-requirements)
* [4. Folder & File Structure](#4-folder--file-structure)
* [5. Business Scenarios](#5-business-scenarios)
* [6. Non-Functional Requirements](#6-non-functional-requirements)
* [7. Recommendations & Next Steps](#7-recommendations--next-steps)

---

## 1. Overview

Codex is a backend system for enterprise knowledge retrieval and retrieval-augmented generation (RAG).
It supports multiple business domains (HR, Finance, Procurement, etc.) and a wide range of asset types (documents, links, audio, etc.), with secure, auditable, and permissioned access, as well as extensible support for LLMs and vector DBs.

---

## 2. Business Requirements

### 2.1. Asset Management

* Support for **multiple asset types**:

  * Documents (PDF, DOCX, TXT, etc.)
  * Web links (articles, pages)
  * Audio (future)
  * Images, Videos (future)
* **Categorization** under domains and (optional) categories.
* **Bulk upload**, delete, and re-indexing by admin users.

### 2.2. Domains & Categories

* Multiple **business domains** (HR, Finance, Procurement, etc.).
* **CRUD** operations for domains.
* **Categories** (optional): further classification within domains.
* Every asset **assigned** to a domain (and optionally a category).

### 2.3. User & Access Control

* **User profiles** with unique identifiers.
* **Roles**:

  * **Global Admin**: Manage all
  * **Domain Admin**: Manage assigned domains
  * **User**: Query/view assigned domains
* **Permissions**: Users only access assets within permitted domains.
* Domain Admins can **assign/remove users** to domains.

### 2.4. Query & Retrieval

* Users query assets they are permitted to access.
* System returns answers **with source attributions**.
* **Multilingual support** (Arabic/English).

### 2.5. Audit & Security

* **Audit trail**: log all admin/user actions.
* Secure storage, input validation, rate limiting, and prevention of unauthorized access.

---

## 3. Technical Requirements

### 3.1. Architecture

* **Python (>=3.10)**, **FastAPI**
* **Clean Architecture**:

  * API Layer
  * Application Layer (services, DTOs)
  * Domain Layer (entities, enums)
  * Infrastructure Layer (repos, providers)
* **MongoDB**: Asset, chunk, user, audit storage
* **Qdrant** (default, pluggable): Vector DB for embeddings
* **OpenAI** (default, pluggable): LLMs for completion/embedding
* **Extensibility** for new LLMs/vector DBs

### 3.2. Asset Ingestion

* **Chunking**: All assets chunked for embeddings/retrieval (configurable).
* **Metadata**: Store asset type, domain, category, owner, etc.

### 3.3. Query Flow

1. User submits query.
2. System determines user's permitted domains.
3. Chunks retrieved (via vector DB) only from permitted domains.
4. LLM generates answer (provider is configurable).
5. System returns answer + sources.

### 3.4. Admin APIs

* User management (CRUD, roles, domain assignments)
* Domain management (CRUD)
* Asset management (CRUD, bulk ops)
* Category management (CRUD)
* Audit log access

### 3.5. Security

* **JWT** authentication
* **RBAC** for roles/domains
* **Rate limiting**, input validation
* Secure file upload (size/type/virus scan)
* (Optional) SSO/LDAP integration

### 3.6. Observability & DevOps

* **Structured logging** (JSON)
* Metrics/tracing (OpenTelemetry optional)
* OpenAPI docs
* **Dockerfile** for containerization
* **pytest** for testing
* **Health check** endpoint

---

## 4. Folder & File Structure

```plaintext
src/
│
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── assets.py         # Asset ingestion, CRUD, search/query
│   │   │   ├── queries.py        # Query endpoints
│   │   │   ├── domains.py        # Domain CRUD
│   │   │   ├── categories.py     # Category CRUD
│   │   │   └── users.py          # User self-service/profile
│   │   └── admin/
│   │       ├── users.py          # User admin, assign roles/domains
│   │       ├── assets.py         # Bulk/admin asset ops
│   │       ├── domains.py        # Domain admin
│   │       ├── categories.py     # Category admin
│   │       └── audit.py          # Audit logs endpoints
│   ├── application/
│   │   ├── services/
│   │   │   ├── asset_service.py
│   │   │   ├── query_service.py
│   │   │   ├── user_service.py
│   │   │   ├── domain_service.py
│   │   │   ├── category_service.py
│   │   │   └── auth_service.py
│   │   ├── dtos/
│   │   │   ├── asset_dto.py
│   │   │   ├── user_dto.py
│   │   │   └── ...
│   │   └── interfaces/
│   │       ├── asset_repository.py
│   │       ├── user_repository.py
│   │       └── ...
│   ├── domain/
│   │   ├── entities/
│   │   │   ├── asset.py
│   │   │   ├── user.py
│   │   │   ├── domain.py
│   │   │   ├── category.py
│   │   │   ├── chunk.py
│   │   │   ├── query.py
│   │   │   └── audit.py
│   │   ├── enums/
│   │   │   ├── asset_type.py
│   │   │   ├── role.py
│   │   │   └── ...
│   │   └── value_objects/
│   │       ├── permissions.py
│   │       └── ...
│   ├── infrastructure/
│   │   ├── repositories/
│   │   │   ├── asset_mongo_repo.py
│   │   │   ├── user_mongo_repo.py
│   │   │   ├── chunk_mongo_repo.py
│   │   │   └── ...
│   │   ├── providers/
│   │   │   ├── openai_llm.py
│   │   │   ├── cohere_llm.py
│   │   │   ├── qdrant_vector_db.py
│   │   │   └── ...
│   │   ├── storage/
│   │   │   └── file_storage.py
│   │   └── auth/
│   │       ├── jwt.py
│   │       └── permissions.py
│   ├── core/
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── utils.py
│   ├── main.py                # FastAPI app factory/entrypoint
│   └── asgi.py                # ASGI entrypoint for deployment
│
├── tests/
│   ├── api/
│   ├── application/
│   ├── domain/
│   └── infrastructure/
│
├── Dockerfile
├── requirements.txt
├── README.md
└── .env.example
```

---

## 5. Business Scenarios

* **Asset Upload by HR Admin**
  HR Admin uploads a batch of policy PDFs under “HR > Policies.” Only HR users can access them.

* **Finance User Query**
  Finance user asks, “What is our expense policy?” Codex searches only Finance assets and replies with answer + source document reference.

* **Admin Adds New Category**
  Admin creates “Contracts” under Procurement. Procurement Admin uploads files and assigns users.

* **Audit Investigation**
  Security admin reviews logs for asset deletions or permission changes.

---

## 6. Non-Functional Requirements

* **Performance**: Sub-second search/query.
* **Scalability**: Horizontal scaling via ASGI/gunicorn.
* **Security**: JWT, RBAC, secure uploads, secrets management.
* **Testability**: >85% code coverage on critical logic.
* **Observability**: Trace key flows, structured logs.

---

## 7. Recommendations & Next Steps

* Build API endpoints to be dashboard-friendly for future UI/admin console.
* Use `/api/v1/` and `/admin/v1/` route prefixes.
* Prepare for i18n (Arabic/English).
* Implement health checks for deployments.
* Ensure extensibility for new asset/LLM/vector DB types.

---

**For detailed API specs, ERDs, DTO samples, or workflow diagrams, see `/docs/` or request from your technical team.**

---

**Last Updated:** 2025-06-25

---

