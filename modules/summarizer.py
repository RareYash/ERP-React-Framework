"""
Summarizer Module
Generates intelligent summaries and insights from student reviews
"""
from typing import Dict, List, Any
from modules.sentiment_analyzer import SentimentAnalyzer
from modules.config import SENTIMENT_LABELS


class ReviewSummarizer:
    """Generate comprehensive summaries from student reviews"""
    
    def __init__(self):
        self.analyzer = SentimentAnalyzer()
    
    def generate_summary(self, student_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate comprehensive summary for a student
        
        Args:
            student_data: Dictionary with student information
            
        Returns:
            Dictionary with summary data
        """
        review_text = student_data.get('Teacher Review', '')
        archetype = student_data.get('Archetype', 'Unknown')
        
        # Overall sentiment
        overall_sentiment = self.analyzer.analyze_sentiment(review_text)
        
        # Category breakdown
        category_scores = self.analyzer.categorize_review(review_text)
        
        # Extract strengths and improvements
        strengths, improvements = self.analyzer.get_strengths_and_improvements(review_text)
        
        # Generate natural language summary
        summary_text = self._generate_text_summary(
            archetype, overall_sentiment, category_scores, strengths, improvements
        )
        
        return {
            "overall_sentiment": overall_sentiment,
            "category_scores": category_scores,
            "strengths": strengths,
            "improvements": improvements,
            "summary_text": summary_text,
            "archetype": archetype
        }
    
    def _generate_text_summary(
        self,
        archetype: str,
        overall_sentiment: Dict,
        category_scores: Dict,
        strengths: List[str],
        improvements: List[str]
    ) -> str:
        """
        Generate natural language summary
        
        Args:
            archetype: Student archetype
            overall_sentiment: Overall sentiment scores
            category_scores: Category-wise scores
            strengths: List of strengths
            improvements: List of areas for improvement
            
        Returns:
            Natural language summary
        """
        sentiment_label = overall_sentiment['label']
        score = overall_sentiment['compound']
        
        # Intro based on sentiment
        if score >= 0.6:
            intro = f"Your child is performing **excellently** overall."
        elif score >= 0.2:
            intro = f"Your child is showing **good progress**."
        elif score >= -0.2:
            intro = f"Your child is making **steady progress**."
        else:
            intro = f"Your child **needs additional support**."
        
        # Archetype insight
        archetype_text = f" Teachers describe them as **{archetype}**."
        
        # Category highlights
        if category_scores:
            top_category = max(category_scores.items(), key=lambda x: x[1])
            bottom_category = min(category_scores.items(), key=lambda x: x[1])
            
            category_text = f"\n\n**Strongest Area:** {top_category[0]} "
            category_text += f"(Score: {top_category[1]:.2f})\n"
            category_text += f"**Needs Attention:** {bottom_category[0]} "
            category_text += f"(Score: {bottom_category[1]:.2f})"
        else:
            category_text = ""
        
        # Strengths
        strengths_text = ""
        if strengths:
            strengths_text = "\n\n**Key Strengths:**\n"
            for i, strength in enumerate(strengths[:2], 1):
                strengths_text += f"{i}. {strength}\n"
        
        # Improvements
        improvements_text = ""
        if improvements:
            improvements_text = "\n\n**Areas for Growth:**\n"
            for i, improvement in enumerate(improvements[:2], 1):
                improvements_text += f"{i}. {improvement}\n"
        
        return intro + archetype_text + category_text + strengths_text + improvements_text
    
    def compare_students(self, students_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Compare multiple students (useful for grade-level analysis)
        
        Args:
            students_data: List of student data dictionaries
            
        Returns:
            Comparison statistics
        """
        all_sentiments = []
        all_categories = {}
        
        for student in students_data:
            review = student.get('Teacher Review', '')
            sentiment = self.analyzer.analyze_sentiment(review)
            all_sentiments.append(sentiment['compound'])
            
            categories = self.analyzer.categorize_review(review)
            for cat, score in categories.items():
                if cat not in all_categories:
                    all_categories[cat] = []
                all_categories[cat].append(score)
        
        # Calculate averages
        avg_sentiment = sum(all_sentiments) / len(all_sentiments) if all_sentiments else 0
        category_averages = {
            cat: sum(scores) / len(scores)
            for cat, scores in all_categories.items()
        }
        
        return {
            "average_sentiment": avg_sentiment,
            "category_averages": category_averages,
            "student_count": len(students_data)
        }
    
    def get_trend_analysis(self, reviews: List[str]) -> Dict[str, Any]:
        """
        Analyze trends over multiple reviews (for future: time-series analysis)
        
        Args:
            reviews: List of review texts
            
        Returns:
            Trend analysis data
        """
        sentiments = [self.analyzer.analyze_sentiment(r)['compound'] for r in reviews]
        
        if len(sentiments) < 2:
            return {"trend": "insufficient_data"}
        
        # Simple trend detection
        first_half_avg = sum(sentiments[:len(sentiments)//2]) / (len(sentiments)//2)
        second_half_avg = sum(sentiments[len(sentiments)//2:]) / (len(sentiments) - len(sentiments)//2)
        
        if second_half_avg > first_half_avg + 0.1:
            trend = "improving"
        elif second_half_avg < first_half_avg - 0.1:
            trend = "declining"
        else:
            trend = "stable"
        
        return {
            "trend": trend,
            "first_period_avg": first_half_avg,
            "second_period_avg": second_half_avg,
            "overall_avg": sum(sentiments) / len(sentiments)
        }
