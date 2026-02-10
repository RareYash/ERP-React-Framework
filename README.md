# 📚 Student Review System

AI-Powered Student Insights Platform with Sentiment Analysis

## 🎯 Overview

This system is a modular component designed to integrate with existing school ERP systems. It provides **intelligent sentiment analysis** of teacher reviews, offering parents and teachers actionable insights about student performance.

### Key Features

- **🔍 Advanced Sentiment Analysis**: Uses VADER NLP to analyze teacher reviews
- **📊 Interactive Dashboards**: Separate views for parents and teachers
- **📈 Visual Analytics**: Charts showing sentiment trends and category breakdowns
- **✏️ Review Management**: Teachers can add/edit reviews with live sentiment preview
- **🔐 Role-Based Access**: Secure authentication for parents and teachers
- **⚡ Optimized Performance**: Caching and efficient data handling
- **📥 Export Reports**: Download detailed student reports

---

## 🏗️ Architecture

```
student-review-system/
│
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
│
├── modules/                    # Core business logic
│   ├── config.py              # Configuration & constants
│   ├── data_handler.py        # CSV operations with caching
│   ├── sentiment_analyzer.py # NLP sentiment analysis
│   ├── summarizer.py          # Generate insights
│   └── auth.py                # Authentication management
│
├── pages/                      # UI components
│   ├── parent_dashboard.py   # Parent view
│   └── teacher_dashboard.py  # Teacher view
│
└── data/                       # Data storage
    └── student_reviews.csv    # Student data & reviews
```

---

## 🚀 Quick Start

### 1. Installation

```bash
# Clone or navigate to project directory
cd student-review-system

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### 3. Login Credentials

**Parent Account:**
- Username: `parent1`
- Password: `pass1234`
- Can view: Student ID 01 (Sophia Chen)

**Teacher Account:**
- Username: `teacher`
- Password: `admin1234`
- Can: Add/edit all student reviews, view analytics

---

## 📖 Usage Guide

### For Parents

1. **Login** with parent credentials
2. **View Dashboard** showing:
   - Overall sentiment score
   - Category-wise performance
   - Key strengths & areas for growth
   - Full teacher review
3. **Download Report** as text file

### For Teachers

1. **Login** with teacher credentials
2. **Add Reviews**:
   - Select student
   - Enter review text
   - See live sentiment analysis
   - Submit review
3. **Edit Reviews**:
   - Select student
   - Modify existing review
   - Save changes
4. **View All Students**:
   - Filter by grade/archetype
   - See sentiment scores
   - Quick statistics
5. **Analytics**:
   - Sentiment distribution
   - Grade-wise comparison
   - Archetype analysis

---

## 🔧 Technical Details

### Sentiment Analysis

The system uses **VADER (Valence Aware Dictionary and sEntiment Reasoner)** with custom educational context adjustments:

- **Handles complex patterns**:
  - "Sandwich" feedback (praise → critique → praise)
  - Contrast words ("however", "but")
  - Soft critiques ("would benefit from")
  - Context-dependent meanings

- **Scoring**:
  - -1.0 to -0.6: Very Negative
  - -0.6 to -0.2: Negative
  - -0.2 to +0.2: Neutral
  - +0.2 to +0.6: Positive
  - +0.6 to +1.0: Very Positive

### Category Detection

Automatically categorizes reviews into:
- **Behavior**: Classroom conduct, attitude
- **Homework**: Assignment completion, quality
- **Participation**: Class engagement, discussions
- **Social Skills**: Teamwork, cooperation
- **Academic Performance**: Understanding, progress

### Performance Optimizations

- **Caching**: Uses Streamlit's `@st.cache_data` for CSV operations
- **Efficient Loading**: Lazy loading of data
- **Modular Design**: Separation of concerns for scalability

---

## 📊 Data Format

### CSV Structure (student_reviews.csv)

| Column | Description |
|--------|-------------|
| Student Number | Unique ID (01, 02, etc.) |
| Student Name | Full name |
| Grade | Grade level |
| Subject | Subject area |
| Archetype | Student personality type |
| Teacher Review | Detailed qualitative feedback |
| NLP Analysis | (Optional) Meta-commentary |

---

## 🔄 Extending the System

### Adding New Users

Edit `modules/config.py`:

```python
USERS = {
    "parent2": {
        "password": "pass5678",
        "role": "parent",
        "student_id": "02"
    },
    # Add more users...
}
```

### Adding Students

Simply add rows to `data/student_reviews.csv` with all required columns.

### Database Migration

To migrate from CSV to database (SQLite/PostgreSQL):

1. Modify `modules/data_handler.py`
2. Replace `pd.read_csv()` with database queries
3. Update `add_review()` and `update_review()` methods
4. Keep the same interface for backward compatibility

---

## 🎨 Customization

### Changing Colors

Edit `modules/config.py`:

```python
CHART_COLORS = {
    "positive": "#10B981",  # Your color
    "negative": "#EF4444",
    # ...
}
```

### Adjusting Sentiment Thresholds

Edit `modules/config.py`:

```python
SENTIMENT_THRESHOLDS = {
    "very_positive": 0.7,  # Adjust as needed
    # ...
}
```

---

## 🧪 Testing

Run basic tests:

```bash
# Test sentiment analyzer
python -c "from modules.sentiment_analyzer import SentimentAnalyzer; 
analyzer = SentimentAnalyzer(); 
print(analyzer.analyze_sentiment('Excellent student!'))"

# Test data handler
python -c "from modules.data_handler import DataHandler; 
handler = DataHandler(); 
print(handler.get_all_students()[:3])"
```

---

## 🚧 Future Enhancements

- [ ] Time-series trend analysis
- [ ] Email notifications for parents
- [ ] Mobile responsive design
- [ ] Multi-language support
- [ ] Integration with Google Classroom
- [ ] Automated report scheduling
- [ ] Machine learning for predicting student needs
- [ ] Teacher collaboration features

---

## 📝 License

Educational use only. Modify as needed for your institution.

---

## 🤝 Contributing

To contribute:
1. Follow PEP 8 coding standards
2. Add docstrings to all functions
3. Test thoroughly before committing
4. Update README with new features

---

## 💡 Tips

- **For Best Results**: Write detailed, specific teacher reviews
- **Review Length**: Aim for 100-300 words for accurate sentiment analysis
- **Be Balanced**: Include both strengths and areas for improvement
- **Regular Updates**: Add reviews weekly or bi-weekly

---

## 📞 Support

For issues or questions:
- Check the Help section in the login page
- Review this README
- Contact your system administrator

---

**Built with ❤️ for better student-teacher-parent communication**
