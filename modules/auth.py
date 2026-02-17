"""
Authentication Module
Simple role-based authentication for the application
"""
try:
    import streamlit as st
except ImportError:
    class MockStreamlit:
        session_state = {}
        def warning(self, msg): pass
        def error(self, msg): pass
        def stop(self): raise Exception("Streamlit stop call in non-streamlit env")
    st = MockStreamlit()

from typing import Optional, Dict
from modules.config import USERS


class AuthManager:
    """Manage user authentication and sessions"""
    
    @staticmethod
    def initialize_session():
        """Initialize session state variables"""
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'username' not in st.session_state:
            st.session_state.username = None
        if 'role' not in st.session_state:
            st.session_state.role = None
        if 'student_id' not in st.session_state:
            st.session_state.student_id = None
    
    @staticmethod
    def login(username: str, password: str) -> bool:
        """
        Authenticate user
        
        Args:
            username: Username
            password: Password
            
        Returns:
            True if authentication successful
        """
        user = USERS.get(username)
        
        if user and user['password'] == password:
            st.session_state.authenticated = True
            st.session_state.username = username
            st.session_state.role = user['role']
            st.session_state.student_id = user.get('student_id')
            return True
        
        return False
    
    @staticmethod
    def logout():
        """Logout current user"""
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None
        st.session_state.student_id = None
    
    @staticmethod
    def is_authenticated() -> bool:
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)
    
    @staticmethod
    def get_current_role() -> Optional[str]:
        """Get current user's role"""
        return st.session_state.get('role')
    
    @staticmethod
    def get_current_username() -> Optional[str]:
        """Get current username"""
        return st.session_state.get('username')
    
    @staticmethod
    def get_student_id() -> Optional[str]:
        """Get student ID for parent users"""
        return st.session_state.get('student_id')
    
    @staticmethod
    def require_auth(allowed_roles: list = None):
        """
        Decorator to require authentication for a page
        
        Args:
            allowed_roles: List of roles allowed to access (None = all authenticated)
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                if not AuthManager.is_authenticated():
                    st.warning("⚠️ Please login to access this page")
                    st.stop()
                
                if allowed_roles and AuthManager.get_current_role() not in allowed_roles:
                    st.error("🚫 You don't have permission to access this page")
                    st.stop()
                
                return func(*args, **kwargs)
            return wrapper
        return decorator
