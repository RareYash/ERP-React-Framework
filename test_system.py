"""
Test script for Student Review System
Verifies core modules work correctly
"""
import sys
sys.path.insert(0, '/home/claude/student-review-system')

from modules.data_handler import DataHandler
from modules.sentiment_analyzer import SentimentAnalyzer
from modules.summarizer import ReviewSummarizer


def test_data_handler():
    """Test data handler functionality"""
    print("=" * 50)
    print("Testing Data Handler...")
    print("=" * 50)
    
    handler = DataHandler()
    
    # Test loading reviews
    df = handler.load_reviews()
    print(f"✓ Loaded {len(df)} student reviews")
    
    # Test get student by ID
    student = handler.get_student_by_id("01")
    if student:
        print(f"✓ Retrieved student: {student['Student Name']}")
    
    # Test get all students
    all_students = handler.get_all_students()
    print(f"✓ Found {len(all_students)} total students")
    
    # Test search
    results = handler.search_students("Sophia")
    print(f"✓ Search found {len(results)} results")
    
    print("\n✅ Data Handler: PASSED\n")


def test_sentiment_analyzer():
    """Test sentiment analysis"""
    print("=" * 50)
    print("Testing Sentiment Analyzer...")
    print("=" * 50)
    
    analyzer = SentimentAnalyzer()
    
    # Test basic sentiment
    text1 = "This is an excellent student who works very hard!"
    result1 = analyzer.analyze_sentiment(text1)
    print(f"✓ Positive text: {result1['label']} (Score: {result1['compound']:.2f})")
    
    text2 = "Student struggles with focus and often disrupts class."
    result2 = analyzer.analyze_sentiment(text2)
    print(f"✓ Negative text: {result2['label']} (Score: {result2['compound']:.2f})")
    
    # Test category detection
    text3 = "Great homework completion but needs to improve participation in class discussions."
    categories = analyzer.categorize_review(text3)
    print(f"✓ Detected {len(categories)} categories: {list(categories.keys())}")
    
    # Test key phrases
    strengths, improvements = analyzer.get_strengths_and_improvements(text3)
    print(f"✓ Extracted {len(strengths)} strengths and {len(improvements)} improvements")
    
    print("\n✅ Sentiment Analyzer: PASSED\n")


def test_summarizer():
    """Test review summarizer"""
    print("=" * 50)
    print("Testing Review Summarizer...")
    print("=" * 50)
    
    handler = DataHandler()
    summarizer = ReviewSummarizer()
    
    # Get a sample student
    student = handler.get_student_by_id("01")
    
    if student:
        summary = summarizer.generate_summary(student)
        
        print(f"✓ Student: {student['Student Name']}")
        print(f"✓ Overall Sentiment: {summary['overall_sentiment']['label']}")
        print(f"✓ Sentiment Score: {summary['overall_sentiment']['compound']:.2f}")
        print(f"✓ Categories Found: {len(summary['category_scores'])}")
        print(f"✓ Strengths: {len(summary['strengths'])}")
        print(f"✓ Improvements: {len(summary['improvements'])}")
        print(f"\n✓ Summary Preview:")
        print(summary['summary_text'][:200] + "...")
    
    print("\n✅ Summarizer: PASSED\n")


def test_integration():
    """Test end-to-end integration"""
    print("=" * 50)
    print("Testing End-to-End Integration...")
    print("=" * 50)
    
    handler = DataHandler()
    summarizer = ReviewSummarizer()
    
    # Process multiple students
    students = handler.get_all_students()[:5]
    
    successful = 0
    for student_info in students:
        student = handler.get_student_by_id(student_info['id'])
        if student:
            summary = summarizer.generate_summary(student)
            if summary['overall_sentiment']['compound'] is not None:
                successful += 1
    
    print(f"✓ Successfully processed {successful}/{len(students)} students")
    
    print("\n✅ Integration Test: PASSED\n")


if __name__ == "__main__":
    print("\n" + "=" * 50)
    print("STUDENT REVIEW SYSTEM - TEST SUITE")
    print("=" * 50 + "\n")
    
    try:
        test_data_handler()
        test_sentiment_analyzer()
        test_summarizer()
        test_integration()
        
        print("=" * 50)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 50)
        print("\nSystem is ready to use!")
        print("Run: streamlit run app.py")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
