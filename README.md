# Daleel Bot Backend

DaleelBot is a lightweight, secure, and Arabic-enabled Retrieval-Augmented Generation (RAG) AI assistant that empowers Saudi-based organizations to access and interact with their internal knowledge sources easily, without relying on external cloud AI platforms.

## 🏗️ Architecture

This project follows **Clean Architecture** principles with a modular, layered design that ensures separation of concerns, testability, and maintainability.

### Project Structure

```
src/
├── api/                           # 🌐 Presentation Layer (Controllers)
│   ├── v1/                        # Public API endpoints
│   │   ├── asset_controller.py    # Asset management (POST operations)
│   │   ├── category_controller.py # Category management (POST operations)  
│   │   ├── domain_controller.py   # Domain management (POST operations)
│   │   ├── user_controller.py     # User management (POST operations)
│   │   └── query_controller.py    # Query processing
│   └── admin/                     # Admin API endpoints
│       ├── asset_controller.py    # Asset viewing (GET operations)
│       ├── category_controller.py # Category viewing (GET operations)
│       ├── domain_controller.py   # Domain viewing (GET operations)
│       ├── user_controller.py     # User viewing (GET operations)
│       └── audit_controller.py    # Audit logs
├── application/                   # 💼 Application Layer (Business Services)
│   ├── services/                  # Business logic services
│   │   ├── user_service.py
│   │   ├── domain_service.py
│   │   ├── category_service.py
│   │   ├── asset_service.py
│   │   ├── auth_service.py
│   │   └── query_service.py
│   ├── integration/               # External service interfaces
│   │   └── llm_provider.py        # LLM provider contract
│   ├── vectordb/                  # Vector database interfaces
│   │   └── vector_db.py           # Vector database contract
│   └── dependencies.py            # Application DI configuration
├── domain/                        # 🎯 Domain Layer (Business Logic)
│   ├── entities/                  # Business entities
│   │   ├── user.py
│   │   ├── domain.py
│   │   ├── category.py
│   │   ├── asset.py
│   │   ├── query.py
│   │   ├── chunk.py
│   │   └── audit.py
│   ├── enums/                     # Business enumerations
│   │   ├── role.py
│   │   └── asset_type.py
│   ├── value_objects/             # Domain value objects
│   │   └── permissions.py
│   ├── persistence/               # Repository interfaces (domain contracts)
│   │   ├── user_repository.py
│   │   ├── domain_repository.py
│   │   ├── category_repository.py
│   │   └── asset_repository.py
│   └── dependencies.py            # Domain exports
├── infrastructure_persistence/    # 💾 Data Access Layer
│   ├── database/                  # Database connection management
│   │   └── mongodb.py
│   ├── mongo_*_repo.py           # MongoDB implementations
│   ├── memory_*_repo.py          # In-memory implementations
│   └── dependencies.py           # Repository DI configuration
├── infrastructure_integration/    # 🔌 External Services Layer
│   ├── cohere_llm.py             # Cohere LLM implementation
│   ├── openai_llm.py             # OpenAI LLM implementation
│   └── dependencies.py           # Integration DI configuration
├── infrastructure_vectordb/       # 🔍 Vector Database Layer
│   ├── memory_vector_db.py       # In-memory vector database
│   ├── qdrant_vector_db.py       # Qdrant vector database
│   └── dependencies.py           # VectorDB DI configuration
├── common/                        # 🛠️ Shared Utilities
│   ├── config.py                 # Application configuration
│   ├── dependencies.py           # Main DI orchestration
│   ├── logging.py                # Logging configuration
│   └── utils.py                  # Shared utilities
├── main.py                        # 🚀 Application entry point
├── asgi.py                        # ASGI server configuration
└── tests/                         # 🧪 Test suite
```

### Layer Responsibilities

#### 🎯 Domain Layer
- **Pure business logic** - no external dependencies
- **Business entities** and value objects
- **Repository interfaces** as domain contracts
- **Business rules** and invariants

#### 💼 Application Layer  
- **Use cases** and application services
- **Integration interfaces** for external services
- **Orchestrates** domain objects and repository operations
- **Transaction boundaries**

#### 🌐 Presentation Layer (API)
- **REST API endpoints** and controllers
- **Request/response** handling and validation
- **Authentication** and authorization
- **API versioning** (v1 for public, admin for management)

#### 💾 Infrastructure Layers
- **infrastructure_persistence**: Database and repository implementations
- **infrastructure_integration**: External service implementations (LLM providers)
- **infrastructure_vectordb**: Vector database implementations
- **Dependency injection** configurations

#### 🛠️ Common Layer
- **Shared utilities** and configuration
- **Main dependency injection** orchestration
- **Cross-cutting concerns** (logging, etc.)

## ⚙️ Configuration

The application uses environment variables for configuration:

### Core Settings
```bash
# Repository backend selection
USE_MONGODB=false                    # true for MongoDB, false for memory

# MongoDB settings (when USE_MONGODB=true)
MONGODB_URL=mongodb://localhost:27017
MONGODB_DATABASE=daleel_bot

# LLM Provider selection
LLM_PROVIDER=openai                  # "openai" or "cohere"
OPENAI_API_KEY=your_openai_key
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_EMBED_MODEL=text-embedding-ada-002

# Vector Database selection  
VECTOR_DB=memory                     # "qdrant" or "memory"
QDRANT_URL=http://localhost:6333
QDRANT_API_KEY=your_qdrant_key
QDRANT_COLLECTION=assets
```

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- MongoDB (optional, for persistent storage)
- Qdrant (optional, for vector search)

### Installation

1. **Clone and setup**:
```bash
git clone <repository-url>
cd daleel-bot-backend
pip install -r requirements.txt
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env with your settings
```

3. **Run the application**:
```bash
# For development
uvicorn src.main:create_app --factory --reload

# For production
uvicorn src.asgi:app --host 0.0.0.0 --port 8000
```

### API Access
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Public API**: http://localhost:8000/api/v1/
- **Admin API**: http://localhost:8000/admin/v1/

## 🧪 Testing

```bash
# Run all tests
pytest src/tests/ -v

# Run specific test categories
pytest src/tests/test_health.py -v          # Health checks
pytest src/tests/test_user_service.py -v    # User service tests
pytest src/tests/test_domain_service.py -v  # Domain service tests

# Run with coverage
pytest src/tests/ --cov=src --cov-report=html
```

## 🔧 Development Modes

### Memory Mode (Development)
- **Fast startup** - no external dependencies
- **Data in memory** - resets on restart
- **Perfect for testing** and development
```bash
USE_MONGODB=false
VECTOR_DB=memory
```

### Production Mode
- **Persistent storage** with MongoDB
- **Vector search** with Qdrant
- **External LLM** integration
```bash
USE_MONGODB=true
MONGODB_URL=mongodb://localhost:27017
VECTOR_DB=qdrant
QDRANT_URL=http://localhost:6333
LLM_PROVIDER=openai
OPENAI_API_KEY=your_key
```

## 📚 API Endpoints

### Public API (v1)
- `POST /api/v1/domains/` - Create domain
- `POST /api/v1/categories/` - Create category  
- `POST /api/v1/assets/` - Create asset
- `POST /api/v1/users/` - Create user
- `GET /api/v1/queries/` - Process queries

### Admin API
- `GET /admin/v1/domains/` - List domains
- `GET /admin/v1/categories/{domain_id}` - List categories
- `GET /admin/v1/assets/{domain_id}` - List assets
- `GET /admin/v1/users/` - List users
- `GET /admin/v1/audit/` - View audit logs

## 🏆 Architecture Benefits

### ✅ Clean Separation of Concerns
- Each layer has a single responsibility
- Clear boundaries between business logic and infrastructure
- Easy to understand and maintain

### ✅ Testability
- Pure domain logic without external dependencies
- Easy mocking of repositories and external services
- Isolated unit testing per layer

### ✅ Flexibility & Extensibility
- Easy to swap implementations (MongoDB ↔ Memory, OpenAI ↔ Cohere)
- Simple to add new repository types (PostgreSQL, Redis, etc.)
- Clear extension points for new features

### ✅ Scalability
- Modular infrastructure packages
- Independent deployment of layers
- Easy horizontal scaling

### ✅ Maintainability
- Self-documenting architecture
- Logical code organization
- Clear data flow and dependencies

## 🛣️ Next Steps

- [ ] Add comprehensive logging and monitoring
- [ ] Implement caching layers (Redis)
- [ ] Add more repository implementations (PostgreSQL)
- [ ] Extend integration providers (Azure OpenAI, etc.)
- [ ] Add authentication and authorization
- [ ] Implement rate limiting and security features
- [ ] Add Docker containerization
- [ ] Create CI/CD pipelines
