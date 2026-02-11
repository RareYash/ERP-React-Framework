"""
Student Review System - Main Application
ERP Integration for School Student Review Management with Sentiment Analysis
"""
import streamlit as st
from modules.auth import AuthManager
from pages.parent_dashboard import show_parent_dashboard
from pages.teacher_dashboard import show_teacher_dashboard
from pages.loading_page import show_loading_page
import time


# Page configuration
st.set_page_config(
    page_title="Student Review System",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Hide sidebar completely
st.markdown("""
    <style>
    /* Hide Streamlit sidebar navigation */
    [data-testid="stSidebar"] {
        display: none;
    }
    section[data-testid="stSidebar"] {
        display: none !important;
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #171717;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        text-align: center;
        color: #6B7280;
        margin-bottom: 2rem;
    }
    /* Modern Button Styling from Uiverse.io */
    .stButton>button {
        width: 100%;
        color: rgba(255, 255, 255, 0.692);
        padding: 10px 15px;
        display: flex;
        justify-content: center;
        align-items: center;
        text-shadow: 0 0 20px rgba(255, 255, 255, 0.397);
        background: rgba(255, 255, 255, 0.068);
        overflow: hidden;
        font-size: 0.9rem;
        font-weight: 600;
        gap: 8px;
        border-radius: 5px;
        margin: 0 5px;
        transition: 0.2s;
        border: 1px solid transparent;
    }
    
    .stButton>button:hover {
        border-color: rgba(255, 255, 255, 0.623);
        background: linear-gradient(
            to bottom,
            rgba(255, 255, 255, 0.144),
            rgba(255, 255, 255, 0.247),
            rgba(255, 255, 255, 0.39)
        );
        box-shadow: 0 6px rgba(255, 255, 255, 0.623);
        transform: translateY(-6px);
    }
    
    .stButton>button:active {
        transform: translateY(2px);
        box-shadow: none;
    }
    
    /* Optimized Input Field Styling from Uiverse.io */
    .stTextInput > div > div > input,
    input[type="password"] {
        font-family: "Montserrat", sans-serif !important;
        width: 100% !important;
        height: 45px !important;
        padding: 10px 20px !important;
        box-shadow: 0 0 0 1.5px #2b2c37, 0 0 25px -17px #000 !important;
        border: 0 !important;
        border-radius: 12px !important;
        background-color: #16171d !important;
        outline: none !important;
        color: #bdbecb !important;
        transition: all 0.25s cubic-bezier(0.19, 1, 0.22, 1) !important;
        cursor: text !important;
    }
    
    .stTextInput > div > div > input::placeholder,
    input[type="password"]::placeholder {
        color: #bdbecb !important;
    }
    
    .stTextInput > div > div > input:hover,
    input[type="password"]:hover {
        box-shadow: 0 0 0 2.5px #2f303d, 0px 0px 25px -15px #000 !important;
    }
    
    .stTextInput > div > div > input:active,
    input[type="password"]:active {
        transform: scale(0.95) !important;
    }
    
    .stTextInput > div > div > input:focus,
    input[type="password"]:focus {
        box-shadow: 0 0 0 2.5px #2f303d !important;
    }
    
    /* Book Loading Animation */
    .loading-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 60vh;
        flex-direction: column;
        gap: 2rem;
    }
    
    .loading-text {
        color: #bdbecb;
        font-size: 1.5rem;
        font-weight: 600;
        text-align: center;
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 0.6; }
        50% { opacity: 1; }
    }
    
    .book,
    .book__pg-shadow,
    .book__pg {
        animation: cover 5s ease-in-out infinite;
    }
    
    .book {
        background-color: hsl(268, 90%, 65%);
        border-radius: 0.25em;
        box-shadow: 0 0.25em 0.5em hsla(0, 0%, 0%, 0.3),
                    0 0 0 0.25em hsl(278, 100%, 57%) inset;
        padding: 0.25em;
        perspective: 37.5em;
        position: relative;
        width: 8em;
        height: 6em;
        transform: translate3d(0, 0, 0);
        transform-style: preserve-3d;
    }
    
    .book__pg-shadow,
    .book__pg {
        position: absolute;
        left: 0.25em;
        width: calc(50% - 0.25em);
    }
    
    .book__pg-shadow {
        animation-name: shadow;
        background-image: linear-gradient(-45deg, hsla(0, 0%, 0%, 0) 50%, hsla(0, 0%, 0%, 0.3) 50%);
        filter: blur(0.25em);
        top: calc(100% - 0.25em);
        height: 3.75em;
        transform: scaleY(0);
        transform-origin: 100% 0%;
    }
    
    .book__pg {
        animation-name: pg1;
        background-color: hsl(223, 10%, 100%);
        background-image: linear-gradient(90deg, hsla(223, 10%, 90%, 0) 87.5%, hsl(223, 10%, 90%));
        height: calc(100% - 0.5em);
        transform-origin: 100% 50%;
    }
    
    .book__pg--2,
    .book__pg--3,
    .book__pg--4 {
        background-image: repeating-linear-gradient(hsl(223, 10%, 10%) 0 0.125em, hsla(223, 10%, 10%, 0) 0.125em 0.5em),
                          linear-gradient(90deg, hsla(223, 10%, 90%, 0) 87.5%, hsl(223, 10%, 90%));
        background-repeat: no-repeat;
        background-position: center;
        background-size: 2.5em 4.125em, 100% 100%;
    }
    
    .book__pg--2 { animation-name: pg2; }
    .book__pg--3 { animation-name: pg3; }
    .book__pg--4 { animation-name: pg4; }
    .book__pg--5 { animation-name: pg5; }
    
    @keyframes cover {
        from, 5%, 45%, 55%, 95%, to {
            animation-timing-function: ease-out;
            background-color: hsl(278, 84%, 67%);
        }
        10%, 40%, 60%, 90% {
            animation-timing-function: ease-in;
            background-color: hsl(271, 90%, 45%);
        }
    }
    
    @keyframes shadow {
        from, 10.01%, 20.01%, 30.01%, 40.01% {
            animation-timing-function: ease-in;
            transform: translate3d(0, 0, 1px) scaleY(0) rotateY(0);
        }
        5%, 15%, 25%, 35%, 45%, 55%, 65%, 75%, 85%, 95% {
            animation-timing-function: ease-out;
            transform: translate3d(0, 0, 1px) scaleY(0.2) rotateY(90deg);
        }
        10%, 20%, 30%, 40%, 50%, to {
            animation-timing-function: ease-out;
            transform: translate3d(0, 0, 1px) scaleY(0) rotateY(180deg);
        }
        50.01%, 60.01%, 70.01%, 80.01%, 90.01% {
            animation-timing-function: ease-in;
            transform: translate3d(0, 0, 1px) scaleY(0) rotateY(180deg);
        }
        60%, 70%, 80%, 90%, to {
            animation-timing-function: ease-out;
            transform: translate3d(0, 0, 1px) scaleY(0) rotateY(0);
        }
    }
    
    @keyframes pg1 {
        from, to {
            animation-timing-function: ease-in-out;
            background-color: hsl(223, 10%, 100%);
            transform: translate3d(0, 0, 1px) rotateY(0.4deg);
        }
        10%, 15% {
            animation-timing-function: ease-out;
            background-color: hsl(223, 10%, 100%);
            transform: translate3d(0, 0, 1px) rotateY(180deg);
        }
        20%, 80% {
            animation-timing-function: ease-in;
            background-color: hsl(223, 10%, 45%);
            transform: translate3d(0, 0, 1px) rotateY(180deg);
        }
        85%, 90% {
            animation-timing-function: ease-in-out;
            background-color: hsl(223, 10%, 100%);
            transform: translate3d(0, 0, 1px) rotateY(180deg);
        }
    }
    
    @keyframes pg2 {
        from, to {
            animation-timing-function: ease-in;
            background-color: hsl(223, 10%, 45%);
            transform: translate3d(0, 0, 1px) rotateY(0.3deg);
        }
        5%, 10% {
            animation-timing-function: ease-in-out;
            background-color: hsl(223, 10%, 100%);
            transform: translate3d(0, 0, 1px) rotateY(0.3deg);
        }
        20%, 25% {
            animation-timing-function: ease-out;
            background-color: hsl(223, 10%, 100%);
            transform: translate3d(0, 0, 1px) rotateY(179.9deg);
        }
        30%, 70% {
            animation-timing-function: ease-in;
            background-color: hsl(223, 10%, 45%);
            transform: translate3d(0, 0, 1px) rotateY(179.9deg);
        }
        75%, 80% {
            animation-timing-function: ease-in-out;
            background-color: hsl(223, 10%, 100%);
            transform: translate3d(0, 0, 1px) rotateY(179.9deg);
        }
        90%, 95% {
            animation-timing-function: ease-out;
            background-color: hsl(223, 10%, 100%);
            transform: translate3d(0, 0, 1px) rotateY(0.3deg);
        }
    }
    
    @keyframes pg3 {
        from, 10%, 90%, to {
            animation-timing-function: ease-in;
            background-color: hsl(223, 10%, 45%);
            transform: translate3d(0, 0, 1px) rotateY(0.2deg);
        }
        15%, 20% {
            animation-timing-function: ease-in-out;
            background-color: hsl(223, 10%, 100%);
            transform: translate3d(0, 0, 1px) rotateY(0.2deg);
        }
        30%, 35% {
            animation-timing-function: ease-out;
            background-color: hsl(223, 10%, 100%);
            transform: translate3d(0, 0, 1px) rotateY(179.8deg);
        }
        40%, 60% {
            animation-timing-function: ease-in;
            background-color: hsl(223, 10%, 45%);
            transform: translate3d(0, 0, 1px) rotateY(179.8deg);
        }
        65%, 70% {
            animation-timing-function: ease-in-out;
            background-color: hsl(223, 10%, 100%);
            transform: translate3d(0, 0, 1px) rotateY(179.8deg);
        }
        80%, 85% {
            animation-timing-function: ease-out;
            background-color: hsl(223, 10%, 100%);
            transform: translate3d(0, 0, 1px) rotateY(0.2deg);
        }
    }
    
    @keyframes pg4 {
        from, 20%, 80%, to {
            animation-timing-function: ease-in;
            background-color: hsl(223, 10%, 45%);
            transform: translate3d(0, 0, 1px) rotateY(0.1deg);
        }
        25%, 30% {
            animation-timing-function: ease-in-out;
            background-color: hsl(223, 10%, 100%);
            transform: translate3d(0, 0, 1px) rotateY(0.1deg);
        }
        40%, 45% {
            animation-timing-function: ease-out;
            background-color: hsl(223, 10%, 100%);
            transform: translate3d(0, 0, 1px) rotateY(179.7deg);
        }
        50% {
            animation-timing-function: ease-in;
            background-color: hsl(223, 10%, 45%);
            transform: translate3d(0, 0, 1px) rotateY(179.7deg);
        }
        55%, 60% {
            animation-timing-function: ease-in-out;
            background-color: hsl(223, 10%, 100%);
            transform: translate3d(0, 0, 1px) rotateY(179.7deg);
        }
        70%, 75% {
            animation-timing-function: ease-out;
            background-color: hsl(223, 10%, 100%);
            transform: translate3d(0, 0, 1px) rotateY(0.1deg);
        }
    }
    
    @keyframes pg5 {
        from, 30%, 70%, to {
            animation-timing-function: ease-in;
            background-color: hsl(223, 10%, 45%);
            transform: translate3d(0, 0, 1px) rotateY(0);
        }
        35%, 40% {
            animation-timing-function: ease-in-out;
            background-color: hsl(223, 10%, 100%);
            transform: translate3d(0, 0, 1px) rotateY(0deg);
        }
        50% {
            animation-timing-function: ease-in-out;
            background-color: hsl(223, 10%, 100%);
            transform: translate3d(0, 0, 1px) rotateY(179.6deg);
        }
        60%, 65% {
            animation-timing-function: ease-out;
            background-color: hsl(223, 10%, 100%);
            transform: translate3d(0, 0, 1px) rotateY(0);
        }
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
                        st.session_state.page = "loading" # Transition to loading page
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

    # Initialize page state if not already set
    if 'page' not in st.session_state:
        st.session_state.page = "login"
    
    # Check authentication status
    if not AuthManager.is_authenticated():
        st.session_state.page = "login" # Always go to login if not authenticated

    # Route based on session state page
    if st.session_state.page == "login":
        show_login_page()
    elif st.session_state.page == "loading":
        show_loading_page()
    elif st.session_state.page == "parent_dashboard":
        show_parent_dashboard()
    elif st.session_state.page == "teacher_dashboard":
        show_teacher_dashboard()
    else:
        st.error("Invalid page state.")
        st.session_state.page = "login" # Fallback to login
        st.rerun()

    # The sidebar is intentionally commented out as per existing code, 
    # but could be re-enabled if needed for dashboards.
    # if AuthManager.is_authenticated():
    #     show_sidebar()


if __name__ == "__main__":
    main()
