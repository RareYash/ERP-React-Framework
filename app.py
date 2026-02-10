"""
Student Review System - Main Application
ERP Integration for School Student Review Management with Sentiment Analysis
"""
import streamlit as st
from modules.auth import AuthManager
#from pages.parent_dashboard import show_parent_dashboard
#from pages.teacher_dashboard import show_teacher_dashboard


# Page configuration
st.set_page_config(
    page_title="Student Review System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1F2937;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #6B7280;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)


def show_login_page():
    """Display login page"""
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 class='main-header'>📚 Student Review System</h1>", unsafe_allow_html=True)
        st.markdown("<p class='sub-header'>AI-Powered Student Insights Platform</p>", unsafe_allow_html=True)
        
        st.divider()
        
        # Login form
        with st.container():
            st.markdown("### 🔐 Login")
            
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            col_btn1, col_btn2 = st.columns(2)
            
            with col_btn1:
                if st.button("🚀 Login", type="primary", use_container_width=True):
                    if AuthManager.login(username, password):
                        st.success("✅ Login successful!")
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials")
            
            with col_btn2:
                if st.button("ℹ️ Help", use_container_width=True):
                    st.info("""
                    **Demo Credentials:**
                    
                    **Parent Account:**
                    - Username: `parent1`
                    - Password: `pass1234`
                    
                    **Teacher Account:**
                    - Username: `teacher`
                    - Password: `admin1234`
                    """)
        
        st.divider()
        
        # Features section
        st.markdown("### ✨ Features")
        
        col_f1, col_f2 = st.columns(2)
        
        with col_f1:
            st.markdown("""
            **For Parents:**
            - 📊 View student performance summaries
            - 📈 Interactive sentiment charts
            - ✅ Key strengths & improvements
            - 📥 Download detailed reports
            """)
        
        with col_f2:
            st.markdown("""
            **For Teachers:**
            - ✏️ Add and edit reviews
            - 🔍 Live sentiment analysis
            - 👥 Manage all students
            - 📊 Class-wide analytics
            """)


def show_sidebar():
    """Display sidebar with user info and navigation"""
    
    with st.sidebar:
        st.markdown("### 👤 User Information")
        
        username = AuthManager.get_current_username()
        role = AuthManager.get_current_role()
        
        st.info(f"""
        **Username:** {username}  
        **Role:** {role.capitalize()}
        """)
        
        st.divider()
        
        if st.button("🚪 Logout", type="primary", use_container_width=True):
            AuthManager.logout()
            st.rerun()
        
        st.divider()
        
        # Additional info
        st.markdown("### ℹ️ About")
        st.markdown("""
        This system uses **AI-powered sentiment analysis** to provide insights into student performance based on teacher reviews.
        
        **Technology Stack:**
        - Python 3.x
        - Streamlit
        - VADER Sentiment Analysis
        - Plotly Charts
        """)
        
        st.divider()
        
        st.markdown("### 📊 System Stats")
        from modules.data_handler import DataHandler
        
        data_handler = DataHandler()
        total_students = len(data_handler.get_all_students())
        
        st.metric("Total Students", total_students)
        st.metric("Active Users", "2")


def main():
    """Main application entry point"""
    
    # Initialize authentication
    AuthManager.initialize_session()
    
    # Check authentication
    if not AuthManager.is_authenticated():
        show_login_page()
    else:
        # Show sidebar
        show_sidebar()
        
        # Route to appropriate dashboard
        role = AuthManager.get_current_role()
        
        if role == "parent":
            show_parent_dashboard()
        elif role == "teacher":
            show_teacher_dashboard()
        else:
            st.error("Unknown role")


if __name__ == "__main__":
    main()
