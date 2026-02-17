"""
Data Handler Module
Handles all CSV operations with caching for performance.
Works in both Streamlit and standalone (FastAPI) contexts.
"""
import pandas as pd
from pathlib import Path
from typing import Optional, List, Dict, Any
from datetime import datetime
from modules.config import REVIEWS_CSV

# --- Streamlit-safe imports ---
# Allow the module to work when Streamlit is not running (e.g. under FastAPI).
try:
    import streamlit as st
    _HAS_STREAMLIT = hasattr(st, "runtime") and st.runtime.exists()
except Exception:
    _HAS_STREAMLIT = False


def _report_error(msg: str):
    """Show an error via Streamlit if available, otherwise raise."""
    if _HAS_STREAMLIT:
        st.error(msg)
    else:
        print(f"[DataHandler] {msg}")


def _clear_cache():
    """Clear the Streamlit data cache if available."""
    if _HAS_STREAMLIT:
        try:
            st.cache_data.clear()
        except Exception:
            pass


class DataHandler:
    """Optimized data handler with caching for CSV operations"""
    
    def __init__(self, csv_path: Path = REVIEWS_CSV):
        self.csv_path = csv_path
        
    def load_reviews(self) -> pd.DataFrame:
        """
        Load student reviews from CSV.
        
        Returns:
            DataFrame with all student reviews
        """
        try:
            # Explicitly set dtype for 'Student Number' to string
            df = pd.read_csv(self.csv_path, dtype={'Student Number': str})
            # Clean column names
            df.columns = df.columns.str.strip()
            return df
        except FileNotFoundError:
            _report_error(f"CSV file not found: {self.csv_path}")
            return pd.DataFrame()
        except Exception as e:
            _report_error(f"Error loading CSV: {str(e)}")
            return pd.DataFrame()
    
    def get_student_by_id(self, student_id: str) -> Optional[Dict[str, Any]]:
        """
        Get student data by ID
        
        Args:
            student_id: Student number (e.g., "01")
            
        Returns:
            Dictionary with student data or None
        """
        df = self.load_reviews()
        
        # Ensure student_id is string and padded
        student_id = str(student_id).zfill(2)
        
        student_data = df[df['Student Number'] == student_id]
        
        if student_data.empty:
            return None
        
        return student_data.iloc[0].to_dict()
    
    def get_student_by_name(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get student data by name (case-insensitive)
        
        Args:
            name: Student name
            
        Returns:
            Dictionary with student data or None
        """
        df = self.load_reviews()
        student_data = df[df['Student Name'].str.lower() == name.lower()]
        
        if student_data.empty:
            return None
        
        return student_data.iloc[0].to_dict()
    
    def get_all_students(self) -> List[Dict[str, str]]:
        """
        Get list of all students (ID and Name only)
        
        Returns:
            List of dictionaries with student_id and name
        """
        df = self.load_reviews()
        return [
            {"id": row['Student Number'], "name": row['Student Name']}
            for _, row in df.iterrows()
        ]
    
    def add_review(self, student_id: str, review_text: str, 
                   teacher_name: str = "Teacher") -> bool:
        """
        Add a new review for a student (appends to existing review)
        
        Args:
            student_id: Student number
            review_text: New review text
            teacher_name: Name of the teacher
            
        Returns:
            True if successful, False otherwise
        """
        try:
            df = pd.read_csv(self.csv_path, dtype={'Student Number': str})
            student_id = str(student_id).zfill(2)
            
            # Find student row
            mask = df['Student Number'] == student_id
            
            if not mask.any():
                _report_error(f"Student {student_id} not found")
                return False
            
            # Append to existing review with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d")
            new_review = f"\n\n[{timestamp} - {teacher_name}]: {review_text}"
            df.loc[mask, 'Teacher Review'] += new_review
            
            # Save back to CSV
            df.to_csv(self.csv_path, index=False)
            
            # Clear cache
            _clear_cache()
            
            return True
            
        except Exception as e:
            _report_error(f"Error adding review: {str(e)}")
            return False
    
    def update_review(self, student_id: str, new_review: str) -> bool:
        """
        Replace entire review for a student
        
        Args:
            student_id: Student number
            new_review: New review text
            
        Returns:
            True if successful, False otherwise
        """
        try:
            df = pd.read_csv(self.csv_path, dtype={'Student Number': str})
            student_id = str(student_id).zfill(2)
            
            mask = df['Student Number'] == student_id
            
            if not mask.any():
                _report_error(f"Student {student_id} not found")
                return False
            
            df.loc[mask, 'Teacher Review'] = new_review
            df.to_csv(self.csv_path, index=False)
            
            # Clear cache
            _clear_cache()
            
            return True
            
        except Exception as e:
            _report_error(f"Error updating review: {str(e)}")
            return False
    
    def search_students(self, query: str) -> List[Dict[str, Any]]:
        """
        Search students by name or ID
        
        Args:
            query: Search query
            
        Returns:
            List of matching students
        """
        df = self.load_reviews()
        query_lower = query.lower()
        
        mask = (
            df['Student Name'].str.lower().str.contains(query_lower, na=False) |
            df['Student Number'].astype(str).str.contains(query, na=False)
        )
        
        results = df[mask]
        return results.to_dict('records')
    
    def get_students_by_grade(self, grade: str) -> List[Dict[str, Any]]:
        """
        Get all students in a specific grade
        
        Args:
            grade: Grade level (e.g., "5th Grade")
            
        Returns:
            List of students in that grade
        """
        df = self.load_reviews()
        grade_students = df[df['Grade'].str.contains(grade, case=False, na=False)]
        return grade_students.to_dict('records')
    
    def get_unique_grades(self) -> List[str]:
        """Get list of all unique grades"""
        df = self.load_reviews()
        return sorted(df['Grade'].unique().tolist())
    
    def get_unique_archetypes(self) -> List[str]:
        """Get list of all unique archetypes"""
        df = self.load_reviews()
        return sorted(df['Archetype'].unique().tolist())

    def update_student_details(
        self, student_id: str, name: str = None, grade: str = None, archetype: str = None
    ) -> bool:
        """
        Update student details (name, grade, archetype).

        Args:
            student_id: Student number
            name: New name (optional)
            grade: New grade (optional)
            archetype: New archetype (optional)

        Returns:
            True if successful, False otherwise
        """
        try:
            df = pd.read_csv(self.csv_path, dtype={'Student Number': str})
            student_id = str(student_id).zfill(2)
            mask = df['Student Number'] == student_id

            if not mask.any():
                _report_error(f"Student {student_id} not found")
                return False

            if name is not None:
                df.loc[mask, 'Student Name'] = name
            if grade is not None:
                df.loc[mask, 'Grade'] = grade
            if archetype is not None:
                df.loc[mask, 'Archetype'] = archetype

            df.to_csv(self.csv_path, index=False)
            _clear_cache()
            return True

        except Exception as e:
            _report_error(f"Error updating student details: {str(e)}")
            return False
