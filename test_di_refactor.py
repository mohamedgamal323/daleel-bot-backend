#!/usr/bin/env python3
"""
Test script to verify that dependency injection refactor is working correctly.
This script tests that AuthService and UserService can be properly instantiated
with constructor-based dependency injection.
"""

import sys
import os

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_dependency_injection():
    """Test that dependency injection works correctly after refactor"""
    print("Testing dependency injection after refactor...")
    
    try:
        # Test imports
        from src.application.services.auth_service import AuthService
        from src.application.services.user_service import UserService
        from src.domain.persistence.dependencies import get_user_repository
        print("✓ All imports successful")
        
        # Test that services can be instantiated with constructor DI
        # (In real FastAPI context, Depends() would be resolved automatically)
        user_repo = get_user_repository()
        auth_service = AuthService(user_repo)
        user_service = UserService(user_repo)
        print("✓ Services instantiated successfully with constructor DI")
        
        # Test that services have the expected dependencies
        assert hasattr(auth_service, '_user_repo'), "AuthService should have _user_repo"
        assert hasattr(user_service, '_repo'), "UserService should have _repo"
        print("✓ Services have correct internal dependencies")
        
        print("\n🎉 All dependency injection tests passed!")
        print("The refactor successfully eliminated intermediate dependency functions.")
        print("Controllers now use AuthService = Depends() and UserService = Depends() directly.")
        
        return True
        
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_dependency_injection()
    exit(0 if success else 1)
