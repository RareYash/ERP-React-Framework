"""
Parent Dashboard
View student summaries, charts, and insights
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from modules.auth import AuthManager
from modules.data_handler import DataHandler
from modules.summarizer import ReviewSummarizer


def show_parent_dashboard():
    """Display parent dashboard"""
    
    # Get student ID for this parent
    student_id = AuthManager.get_student_id()
    
    if not student_id:
        st.error("No student associated with this account")
        return
    
    # Initialize handlers
    data_handler = DataHandler()
    summarizer = ReviewSummarizer()
    
    # Load student data
    student = data_handler.get_student_by_id(student_id)
    
    if not student:
        st.error(f"Student {student_id} not found")
        return
    
    # Header
    st.title("📊 Student Performance Dashboard")
    st.markdown(f"### {student['Student Name']} ({student['Grade']})")
    st.divider()
    
    # Generate summary
    summary = summarizer.generate_summary(student)
    
    # Overall Sentiment Card
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("### 📈 Overall Assessment")
        sentiment_score = summary['overall_sentiment']['compound']
        sentiment_label = summary['overall_sentiment']['label']
        
        # Color-coded metric
        if sentiment_score >= 0.6:
            color = "green"
        elif sentiment_score >= 0.2:
            color = "blue"
        elif sentiment_score >= -0.2:
            color = "orange"
        else:
            color = "red"
        
        st.markdown(
            f"<h2 style='color: {color};'>{sentiment_label}</h2>",
            unsafe_allow_html=True
        )
        st.metric("Sentiment Score", f"{sentiment_score:.2f}", delta=None)
    
    with col2:
        st.markdown("### 🎭 Profile")
        st.info(summary['archetype'])
    
    with col3:
        st.markdown("### 📚 Subject")
        st.info(student['Subject'])
    
    st.divider()
    
    # Summary Text
    st.markdown("### 📝 Summary Insights")
    st.markdown(summary['summary_text'])
    
    st.divider()
    
    # Category Breakdown Chart
    if summary['category_scores']:
        st.markdown("### 📊 Performance by Category")
        
        # Create bar chart
        categories = list(summary['category_scores'].keys())
        scores = list(summary['category_scores'].values())
        
        # Color code bars
        colors = ['green' if s > 0.2 else 'red' if s < -0.2 else 'gray' for s in scores]
        
        fig = go.Figure(data=[
            go.Bar(
                x=categories,
                y=scores,
                marker_color=colors,
                text=[f"{s:.2f}" for s in scores],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Category-wise Sentiment Analysis",
            xaxis_title="Category",
            yaxis_title="Sentiment Score",
            yaxis_range=[-1, 1],
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # Strengths and Improvements
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### ✅ Key Strengths")
        if summary['strengths']:
            for i, strength in enumerate(summary['strengths'], 1):
                st.success(f"**{i}.** {strength}")
        else:
            st.info("No specific strengths highlighted")
    
    with col2:
        st.markdown("### 📈 Areas for Growth")
        if summary['improvements']:
            for i, improvement in enumerate(summary['improvements'], 1):
                st.warning(f"**{i}.** {improvement}")
        else:
            st.info("No specific areas for improvement noted")
    
    st.divider()
    
    # Full Teacher Review (Expandable)
    with st.expander("📖 View Full Teacher Review"):
        st.markdown(student['Teacher Review'])
    
    # Sentiment Gauge
    st.markdown("### 🎯 Sentiment Gauge")
    
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=sentiment_score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Overall Sentiment"},
        gauge={
            'axis': {'range': [-1, 1]},
            'bar': {'color': color},
            'steps': [
                {'range': [-1, -0.6], 'color': "lightpink"},
                {'range': [-0.6, -0.2], 'color': "lightyellow"},
                {'range': [-0.2, 0.2], 'color': "lightgray"},
                {'range': [0.2, 0.6], 'color': "lightblue"},
                {'range': [0.6, 1], 'color': "lightgreen"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': sentiment_score
            }
        }
    ))
    
    fig_gauge.update_layout(height=300)
    st.plotly_chart(fig_gauge, use_container_width=True)
    
    # Download Report Button
    st.divider()
    if st.button("📥 Download Summary Report"):
        # Generate text report
        report = f"""
STUDENT PERFORMANCE REPORT
==========================

Student: {student['Student Name']}
Grade: {student['Grade']}
Subject: {student['Subject']}
Archetype: {summary['archetype']}

Overall Sentiment: {sentiment_label} ({sentiment_score:.2f})

{summary['summary_text']}

--- FULL TEACHER REVIEW ---
{student['Teacher Review']}

Generated by Student Review System
        """
        
        st.download_button(
            label="Download TXT Report",
            data=report,
            file_name=f"{student['Student Name']}_report.txt",
            mime="text/plain"
        )
