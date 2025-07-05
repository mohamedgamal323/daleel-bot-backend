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
│   ├── dtos/                      # Data Transfer Objects
│   │   ├── auth_dtos.py           # Authentication DTOs
│   │   ├── category_dtos.py       # Category DTOs
│   │   ├── domain_dtos.py         # Domain DTOs
│   │   ├── asset_dtos.py          # Asset DTOs
│   │   ├── user_dtos.py           # User DTOs
│   │   └── query_dtos.py          # Query DTOs
│   ├── services/                  # Business logic services
│   │   ├── user_service.py
│   │   ├── domain_service.py
│   │   ├── category_service.py
│   │   ├── asset_service.py
│   │   ├── auth_service.py
│   │   └── query_service.py
│   ├── integration/               # External service interfaces
│   │   ├── llm_provider.py        # LLM provider contract
│   │   └── dependencies.py        # Integration DI providers
│   ├── vectordb/                  # Vector database interfaces
│   │   └── vector_db.py           # Vector database contract
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
│   │   ├── asset_repository.py
│   │   └── dependencies.py        # Repository DI providers
│   └── dependencies.py            # Domain exports
├── infrastructure_persistence/    # 💾 Data Access Layer
│   ├── database/                  # Database connection management
│   │   └── mongodb.py
│   ├── mongo_*_repo.py           # MongoDB implementations
│   └── memory_*_repo.py          # In-memory implementations
├── infrastructure_integration/    # 🔌 External Services Layer
│   ├── cohere_llm.py             # Cohere LLM implementation
│   └── openai_llm.py             # OpenAI LLM implementation
├── infrastructure_vectordb/       # 🔍 Vector Database Layer
│   ├── memory_vector_db.py       # In-memory vector database
│   └── qdrant_vector_db.py       # Qdrant vector database
├── common/                        # 🛠️ Shared Utilities
│   ├── config.py                 # Application configuration
│   ├── logging.py                # Logging configuration
│   └── utils.py                  # Shared utilities
├── main.py                        # 🚀 Application entry point
├── asgi.py                        # ASGI server configuration
├── tests/                         # 🧪 Test suite
└── dependencies.py                # 🔌 Optional root-level DI config
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

### 📦 Data Transfer Objects (DTOs)

**DTOs are mandatory** for all API communication between controllers and services. This ensures proper separation of concerns and API contract management.

#### DTO Organization
DTOs are organized in `src/application/dtos/` using the following patterns:

```
src/application/dtos/
├── auth_dtos.py           # Authentication & authorization DTOs
├── category_dtos.py       # Category management DTOs  
├── domain_dtos.py         # Domain management DTOs
├── asset_dtos.py          # Asset management DTOs
├── user_dtos.py           # User management DTOs
└── query_dtos.py          # Query processing DTOs
```

#### DTO Naming Conventions
- **Request DTOs**: `Create{Entity}RequestDto`, `Update{Entity}RequestDto`
- **Response DTOs**: `{Entity}ResponseDto`
- **Special DTOs**: `Login{Operation}Dto`, `{Action}RequestDto`

#### DTO Implementation Rules
1. **All DTOs must have "Dto" suffix** in their class names
2. **Use `@dataclass`** for DTO implementation (not Pydantic models)
3. **Controllers must never define request/response models** - always use DTOs
4. **Services must accept DTOs** for create/update operations (not individual parameters)
5. **One file per domain** (e.g., all category-related DTOs in `category_dtos.py`)
6. **DTOs should only contain data** - no business logic

#### Example DTO Usage
```python
# ✅ Correct: Using DTOs end-to-end
from src.application.dtos.category_dtos import CreateCategoryRequestDto, CategoryResponseDto

# Controller passes DTO to service
@router.post("/")
async def create_category(
    request: CreateCategoryRequestDto,
    service: CategoryService = Depends(),
):
    category = await service.create_category(request)  # DTO passed directly
    dto = category_to_response_dto(category)
    return category_response_dto_to_dict(dto)

# Service accepts DTO
async def create_category(self, dto: CreateCategoryRequestDto) -> Category:
    category = Category(name=dto.name, domain_id=dto.domain_id)
    # ... business logic
    return category

# ❌ Wrong: Defining models in controller
class CreateCategoryRequest(BaseModel):  # Don't do this!
    name: str

# ❌ Wrong: Service with individual parameters  
async def create_category(self, name: str, domain_id: UUID):  # Don't do this!
    # Should accept DTO instead
```

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

## 🔌 Enhanced Constructor-Based Dependency Injection

This project implements **true constructor-based dependency injection** using FastAPI's built-in DI system for ultra-clean, testable, and maintainable code.

### Dependency Injection Flow

```
Controller → Service → Repository/Provider
     ↓         ↓            ↓
   Depends   Constructor   Factory
     ↓         ↓            ↓
   Auto-resolved in constructor
```

### How It Works

#### 1. **Services Use Constructor-Based DI**
Services declare their dependencies directly in the constructor with `Depends()`:

```python
# application/services/category_service.py
from fastapi import Depends
from src.domain.persistence.dependencies import get_category_repository

class CategoryService:
    def __init__(self, repo: CategoryRepository = Depends(get_category_repository)):
        self._repo = repo
```

#### 2. **Controllers Use Simple Depends()**
Controllers just declare the service dependency with an empty `Depends()`:

```python
# api/v1/category_controller.py
@router.post("/")
async def create_category(
    name: str,
    domain_id: UUID,
    service: CategoryService = Depends()  # FastAPI auto-resolves everything!
):
    return await service.create_category(name, domain_id)
```

#### 3. **Repository Dependencies by Layer**
Each layer handles its own dependency resolution:

```python
# domain/persistence/dependencies.py - Repository providers
def get_category_repository() -> CategoryRepository:
    settings = get_settings()
    if settings.USE_MONGODB:
        return MongoCategoryRepository()
    else:
        return MemoryCategoryRepository()
```

### Benefits

- **🧹 Ultra-Clean**: No manual factory functions in controllers
- **🔄 Automatic Resolution**: FastAPI resolves entire dependency chains
- **🧪 Easy Testing**: Direct instantiation with mock dependencies
- **🏗️ True Clean Architecture**: Each layer manages its own dependencies
- **📦 Zero Boilerplate**: Services work both in FastAPI and in tests
- **⚡ Performance**: Dependencies are resolved once per request automatically

### Testing with Constructor DI

```python
# Direct instantiation for testing - clean and simple
def test_category_service():
    repo = MemoryCategoryRepository()
    service = CategoryService(repo)  # Works perfectly!
    # Test service logic...

def test_asset_service_with_integrations():
    repo = MemoryAssetRepository()
    llm = MockLLMProvider()
    vector_db = MockVectorDB()
    service = AssetService(repo, llm=llm, vector_db=vector_db)
    # Test with all dependencies...
```

### Dependency Resolution Layers

- **Repository Layer**: `src.domain.persistence.dependencies` - Repository implementations
- **Integration Layer**: `src.application.integration.dependencies` - External service providers
- **Services**: Use constructor injection with `Depends()` 
- **Controllers**: Use simple `Depends()` - everything auto-resolves!

This approach completely eliminates the need for manual service factory functions while maintaining full type safety and testability.

## 🛣️ Next Steps

- [ ] Add comprehensive logging and monitoring
- [ ] Implement caching layers (Redis)
- [ ] Add more repository implementations (PostgreSQL)
- [ ] Extend integration providers (Azure OpenAI, etc.)
- [ ] Add authentication and authorization
- [ ] Implement rate limiting and security features
- [ ] Add Docker containerization
- [ ] Create CI/CD pipelines
