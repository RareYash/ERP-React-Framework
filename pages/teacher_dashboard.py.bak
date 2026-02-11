"""
Teacher Dashboard
Add, edit, and view student reviews
"""
import streamlit as st
import pandas as pd
from modules.auth import AuthManager
from modules.data_handler import DataHandler
from modules.sentiment_analyzer import SentimentAnalyzer
from modules.summarizer import ReviewSummarizer


def show_teacher_dashboard():
    """Display teacher dashboard"""
    
    st.title("👨‍🏫 Teacher Dashboard")
    st.markdown("*Manage student reviews and track sentiment*")
    st.divider()
    
    # Initialize handlers
    data_handler = DataHandler()
    analyzer = SentimentAnalyzer()
    summarizer = ReviewSummarizer()
    
    # Tabs for different functions
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Add Review",
        "✏️ Edit Review",
        "👥 View All Students",
        "📊 Analytics"
    ])
    
    # TAB 1: Add Review
    with tab1:
        st.markdown("### Add New Review Entry")
        
        # Get all students
        students = data_handler.get_all_students()
        student_options = {f"{s['name']} (ID: {s['id']})": s['id'] for s in students}
        
        selected_student = st.selectbox(
            "Select Student",
            options=list(student_options.keys())
        )
        
        teacher_name = st.text_input("Your Name", value="Teacher")
        
        review_text = st.text_area(
            "Review Text",
            height=200,
            placeholder="Enter your observations about the student..."
        )
        
        # Live sentiment preview
        if review_text:
            st.markdown("#### 🔍 Live Sentiment Preview")
            sentiment = analyzer.analyze_sentiment(review_text)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Sentiment", sentiment['label'])
            with col2:
                st.metric("Score", f"{sentiment['compound']:.2f}")
            
            # Category detection
            categories = analyzer.categorize_review(review_text)
            if categories:
                st.markdown("**Detected Categories:**")
                for cat, score in categories.items():
                    st.write(f"- {cat}: {score:.2f}")
        
        if st.button("➕ Add Review", type="primary"):
            if review_text.strip():
                student_id = student_options[selected_student]
                success = data_handler.add_review(student_id, review_text, teacher_name)
                
                if success:
                    st.success("✅ Review added successfully!")
                    st.balloons()
                else:
                    st.error("❌ Failed to add review")
            else:
                st.warning("⚠️ Please enter review text")
    
    # TAB 2: Edit Review
    with tab2:
        st.markdown("### Edit Existing Review")
        
        students = data_handler.get_all_students()
        student_options = {f"{s['name']} (ID: {s['id']})": s['id'] for s in students}
        
        selected_student_edit = st.selectbox(
            "Select Student to Edit",
            options=list(student_options.keys()),
            key="edit_student"
        )
        
        student_id = student_options[selected_student_edit]
        student_data = data_handler.get_student_by_id(student_id)
        
        if student_data:
            st.markdown(f"**Current Review for {student_data['Student Name']}:**")
            
            current_review = student_data['Teacher Review']
            
            # Show current sentiment
            current_sentiment = analyzer.analyze_sentiment(current_review)
            st.info(f"Current Sentiment: {current_sentiment['label']} ({current_sentiment['compound']:.2f})")
            
            # Editable text area
            new_review = st.text_area(
                "Edit Review",
                value=current_review,
                height=300,
                key="edit_review"
            )
            
            if st.button("💾 Save Changes", type="primary"):
                if new_review.strip():
                    success = data_handler.update_review(student_id, new_review)
                    
                    if success:
                        st.success("✅ Review updated successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to update review")
                else:
                    st.warning("⚠️ Review cannot be empty")
    
    # TAB 3: View All Students
    with tab3:
        st.markdown("### 👥 All Students Overview")
        
        # Filters
        col1, col2 = st.columns(2)
        
        with col1:
            grades = data_handler.get_unique_grades()
            selected_grade = st.selectbox(
                "Filter by Grade",
                options=["All"] + grades
            )
        
        with col2:
            archetypes = data_handler.get_unique_archetypes()
            selected_archetype = st.selectbox(
                "Filter by Archetype",
                options=["All"] + archetypes
            )
        
        # Load and filter data
        df = data_handler.load_reviews()
        
        if selected_grade != "All":
            df = df[df['Grade'] == selected_grade]
        
        if selected_archetype != "All":
            df = df[df['Archetype'] == selected_archetype]
        
        # Add sentiment analysis
        df['Sentiment Score'] = df['Teacher Review'].apply(
            lambda x: analyzer.analyze_sentiment(x)['compound']
        )
        df['Sentiment Label'] = df['Teacher Review'].apply(
            lambda x: analyzer.analyze_sentiment(x)['label']
        )
        
        # Display table
        st.dataframe(
            df[['Student Number', 'Student Name', 'Grade', 'Archetype', 
                'Sentiment Label', 'Sentiment Score']],
            use_container_width=True,
            hide_index=True
        )
        
        # Quick stats
        st.markdown("#### 📊 Quick Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Students", len(df))
        with col2:
            avg_sentiment = df['Sentiment Score'].mean()
            st.metric("Average Sentiment", f"{avg_sentiment:.2f}")
        with col3:
            positive_count = len(df[df['Sentiment Score'] > 0.2])
            st.metric("Positive Reviews", positive_count)
    
    # TAB 4: Analytics
    with tab4:
        st.markdown("### 📊 Class-wide Analytics")
        
        df = data_handler.load_reviews()
        
        # Calculate sentiments for all students
        df['Sentiment'] = df['Teacher Review'].apply(
            lambda x: analyzer.analyze_sentiment(x)['compound']
        )
        
        # Sentiment Distribution
        st.markdown("#### Sentiment Distribution")
        
        import plotly.express as px
        
        fig = px.histogram(
            df,
            x='Sentiment',
            nbins=20,
            title="Distribution of Student Sentiments",
            labels={'Sentiment': 'Sentiment Score'},
            color_discrete_sequence=['#3B82F6']
        )
        
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Grade-wise comparison
        st.markdown("#### Average Sentiment by Grade")
        
        grade_sentiment = df.groupby('Grade')['Sentiment'].mean().reset_index()
        
        fig2 = px.bar(
            grade_sentiment,
            x='Grade',
            y='Sentiment',
            title="Average Sentiment by Grade",
            color='Sentiment',
            color_continuous_scale='RdYlGn',
            range_color=[-1, 1]
        )
        
        fig2.update_layout(height=400)
        st.plotly_chart(fig2, use_container_width=True)
        
        # Archetype analysis
        st.markdown("#### Top Student Archetypes")
        
        archetype_counts = df['Archetype'].value_counts().head(10)
        
        fig3 = px.pie(
            values=archetype_counts.values,
            names=archetype_counts.index,
            title="Distribution of Student Archetypes"
        )
        
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, use_container_width=True)
