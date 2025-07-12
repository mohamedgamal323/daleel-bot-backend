# DaleelBot - AI-Powered Knowledge Management System (Monorepo)

DaleelBot is a comprehensive knowledge management system that allows users to store, organize, and query documents using AI-powered search capabilities. The system is built as a monorepo containing both the backend API and frontend web application.

## 🏗️ Architecture

### Monorepo Structure
```
├── src/
│   ├── backend/               # FastAPI backend application
│   │   ├── api/              # API endpoints
│   │   ├── application/      # Application services and DTOs
│   │   ├── core/             # Core configuration and utilities
│   │   ├── domain/           # Domain entities and business logic
│   │   ├── infrastructure/   # External integrations and repositories
│   │   └── tests/            # Backend tests
│   ├── frontend/             # Vue.js frontend application
│   │   ├── src/
│   │   │   ├── components/   # Vue components
│   │   │   ├── views/        # Page views
│   │   │   ├── stores/       # Pinia stores
│   │   │   ├── services/     # API services
│   │   │   └── types/        # TypeScript types
│   │   └── demo.html         # Standalone demo
│   └── shared/               # Shared types and utilities
│       └── types.ts          # TypeScript interfaces
├── scripts/                  # Development and build scripts
├── requirements.txt          # Python dependencies
└── package.json             # Node.js scripts and dependencies
```

## 🚀 Quick Start

### Prerequisites
- **Backend**: Python 3.9+, pip
- **Frontend**: Node.js 20+, npm
- **Database**: PostgreSQL (for production) or SQLite (for development)
- **Vector Database**: Qdrant (optional, for AI features)

### Development Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd daleel-bot-backend
   ```

2. **Install dependencies**
   ```bash
   # Install Python dependencies
   pip install -r requirements.txt
   
   # Install Node.js dependencies
   npm install
   ```

3. **Start development environment**
   ```bash
   # Start both backend and frontend
   npm run dev
   
   # Or start individually
   npm run dev:backend    # Backend only
   npm run dev:frontend   # Frontend only
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - **Demo**: Open `src/frontend/demo.html` in your browser

## 🔧 Development Scripts

### Root Package.json Scripts
- `npm run dev` - Start both backend and frontend
- `npm run build` - Build both applications
- `npm run test` - Run all tests
- `npm run lint` - Lint both codebases
- `npm run format` - Format code

### Backend Scripts
- `npm run dev:backend` - Start FastAPI development server
- `npm run test:backend` - Run backend tests
- `npm run lint:backend` - Lint Python code

### Frontend Scripts
- `npm run dev:frontend` - Start Vue development server
- `npm run build:frontend` - Build frontend for production
- `npm run test:frontend` - Run frontend tests
- `npm run lint:frontend` - Lint frontend code

## 📁 Backend Structure

### Clean Architecture
The backend follows Clean Architecture principles:

- **Domain Layer**: Core business entities and rules
- **Application Layer**: Use cases and application services
- **Infrastructure Layer**: External concerns (databases, APIs)
- **API Layer**: HTTP endpoints and request/response handling

### Key Features
- **Authentication**: JWT-based user authentication
- **Authorization**: Role-based access control
- **Domain Management**: Organize content by domains
- **Category Management**: Categorize content within domains
- **Asset Management**: Store and manage documents/files
- **AI-Powered Search**: Vector-based similarity search
- **RESTful API**: OpenAPI/Swagger documentation

## 🎨 Frontend Structure

### Vue.js 3 + TypeScript
The frontend is built with modern Vue.js 3 features:

- **Composition API**: For better TypeScript support
- **Pinia**: State management
- **Vue Router**: Client-side routing
- **Tailwind CSS**: Utility-first styling
- **Axios**: HTTP client

### Key Features
- **Responsive Design**: Mobile-first approach
- **Authentication**: Login/logout with JWT
- **Dashboard**: Overview of system statistics
- **Domain Management**: CRUD operations for domains
- **Category Management**: CRUD operations for categories
- **Asset Management**: Upload and manage files
- **Search Interface**: Query the knowledge base

## 🔗 Shared Types

The `src/shared/types.ts` file contains TypeScript interfaces shared between frontend and backend:

- **Authentication Types**: Login, registration, user management
- **Domain Types**: Domain creation, updates, responses
- **Category Types**: Category management interfaces
- **Asset Types**: Asset upload, metadata, responses
- **API Types**: Standard API response formats

## 🛠️ API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/logout` - User logout
- `GET /api/auth/profile` - Get user profile

### Domains
- `GET /api/domains` - List domains
- `POST /api/domains` - Create domain
- `GET /api/domains/{id}` - Get domain
- `PUT /api/domains/{id}` - Update domain
- `DELETE /api/domains/{id}` - Delete domain

### Categories
- `GET /api/categories` - List categories
- `POST /api/categories` - Create category
- `GET /api/categories/{id}` - Get category
- `PUT /api/categories/{id}` - Update category
- `DELETE /api/categories/{id}` - Delete category

### Assets
- `GET /api/assets` - List assets
- `POST /api/assets` - Create asset
- `POST /api/assets/upload` - Upload file
- `GET /api/assets/{id}` - Get asset
- `PUT /api/assets/{id}` - Update asset
- `DELETE /api/assets/{id}` - Delete asset

### Query
- `POST /api/query` - Search assets
- `GET /api/queries` - Get query history

## 🔒 Security

### Authentication
- JWT tokens for stateless authentication
- Secure password hashing with bcrypt
- Token refresh mechanism

### Authorization
- Role-based access control (RBAC)
- Three user roles: `user`, `domain_admin`, `global_admin`
- Granular permissions for different operations

### Data Protection
- Input validation and sanitization
- CORS configuration
- SQL injection prevention
- XSS protection

## 🗄️ Database Schema

### Users
- User authentication and profile information
- Role-based access control

### Domains
- Top-level organization units
- Access control and permissions

### Categories
- Subcategories within domains
- Hierarchical organization

### Assets
- Document storage and metadata
- File paths and content indexing

### Queries
- Search history and analytics
- Query performance tracking

## 🤖 AI Features

### Vector Search
- Document embedding with OpenAI/Cohere
- Similarity search with Qdrant
- Semantic query understanding

### LLM Integration
- Multiple LLM providers supported
- Configurable model selection
- Response generation and summarization

## 🚀 Deployment

### Production Build
```bash
# Build both applications
npm run build

# Or build individually
npm run build:backend
npm run build:frontend
```

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

### Environment Variables
```env
# Backend
DATABASE_URL=postgresql://user:pass@localhost/daleel
JWT_SECRET=your-secret-key
OPENAI_API_KEY=your-openai-key
QDRANT_URL=http://localhost:6333

# Frontend
VITE_API_URL=http://localhost:8000
```

## 🧪 Testing

### Backend Tests
```bash
# Run all backend tests
pytest

# Run with coverage
pytest --cov=src/backend
```

### Frontend Tests
```bash
# Run frontend tests
npm run test:frontend

# Run with coverage
npm run test:frontend -- --coverage
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

### Code Style
- **Python**: Follow PEP 8, use Black for formatting
- **TypeScript**: Use ESLint + Prettier
- **Vue**: Follow Vue.js style guide

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the API documentation at `/docs`
- Review the frontend demo at `src/frontend/demo.html`

## 🔄 Monorepo Migration

This project has been restructured into a monorepo:
- **Previous**: Backend-only FastAPI application
- **Current**: Full-stack application with Vue.js frontend
- **Structure**: `src/backend/` + `src/frontend/` + `src/shared/`
- **Benefits**: Shared types, unified development, better integration

## 📊 Current Status

- ✅ **Backend**: FastAPI application with Clean Architecture
- ✅ **Frontend**: Vue 3 + TypeScript with Tailwind CSS
- ✅ **Shared Types**: Common TypeScript interfaces
- ✅ **Development Scripts**: Unified build and dev commands
- ✅ **Demo**: Standalone HTML demo available
- ⚠️ **Node.js Compatibility**: Requires Node.js 20+ for full frontend build
- 📋 **TODO**: Complete implementation of remaining views and features

## 🔄 Updates

- **v1.0.0**: Initial monorepo setup with Vue 3 + FastAPI
- **v1.1.0**: Added AI-powered search capabilities
- **v1.2.0**: Enhanced UI/UX with Tailwind CSS
- **v1.3.0**: Added comprehensive authentication system
