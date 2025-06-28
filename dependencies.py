"""Root-level dependency injection configuration
This file can be used for any application-wide dependency overrides or additional DI setup.
For now, all dependencies are handled directly in their respective layers.
"""

# This file can be used for:
# - Dependency overrides for testing
# - Application-wide singleton dependencies
# - Cross-cutting concerns like logging, metrics, etc.

# Currently, all dependencies are resolved through the services' constructor injection:
# - Repository dependencies: src.domain.persistence.dependencies
# - Integration dependencies: src.application.integration.dependencies
# - Services use these in their constructors with Depends()
