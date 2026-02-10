"""
Sentiment Analyzer Module
Advanced sentiment analysis with VADER and custom rules for educational context
"""
import re
from typing import Dict, List, Tuple
from collections import Counter
import streamlit as st

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    VADER_AVAILABLE = True
except ImportError:
    VADER_AVAILABLE = False
    st.warning("VADER not installed. Using basic sentiment analysis.")

from modules.config import CATEGORY_KEYWORDS, SENTIMENT_THRESHOLDS


class SentimentAnalyzer:
    """
    Advanced sentiment analyzer for teacher reviews
    Handles complex educational feedback patterns
    """
    
    def __init__(self):
        self.vader = SentimentIntensityAnalyzer() if VADER_AVAILABLE else None
        
        # Contextual modifiers that flip sentiment
        self.negation_words = {
            "not", "no", "never", "neither", "nobody", "nothing",
            "nowhere", "rarely", "seldom", "hardly"
        }
        
        # Pivot words that introduce contrast
        self.contrast_words = {
            "however", "but", "although", "though", "yet",
            "nevertheless", "nonetheless", "still", "while"
        }
        
        # Positive indicators in educational context
        self.positive_indicators = {
            "excellent", "outstanding", "exceptional", "strong", "great",
            "wonderful", "impressive", "talented", "gifted", "stellar",
            "enthusiastic", "motivated", "conscientious", "diligent"
        }
        
        # Negative indicators with educational nuance
        self.negative_indicators = {
            "struggle", "difficulty", "challenge", "needs improvement",
            "disruptive", "distract", "careless", "rushed", "neglect",
            "impatient", "interrupt", "dominate", "bossy", "abrasive"
        }
        
        # Soft critique phrases (less severe)
        self.soft_critiques = {
            "would benefit from", "could improve", "encouraged to",
            "needs to practice", "working on", "developing"
        }
    
    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Analyze sentiment of review text
        
        Args:
            text: Review text
            
        Returns:
            Dictionary with sentiment scores
        """
        if self.vader:
            scores = self.vader.polarity_scores(text)
            compound = scores['compound']
        else:
            # Fallback basic sentiment
            compound = self._basic_sentiment(text)
        
        # Adjust for educational context
        adjusted_score = self._adjust_for_context(text, compound)
        
        return {
            "compound": adjusted_score,
            "label": self._get_sentiment_label(adjusted_score),
            "raw_score": compound,
            "has_contrast": self._detect_contrast(text)
        }
    
    def _basic_sentiment(self, text: str) -> float:
        """
        Fallback sentiment analysis without VADER
        
        Args:
            text: Review text
            
        Returns:
            Sentiment score between -1 and 1
        """
        text_lower = text.lower()
        words = text_lower.split()
        
        positive_count = sum(1 for word in words if word in self.positive_indicators)
        negative_count = sum(1 for word in words if word in self.negative_indicators)
        
        total = positive_count + negative_count
        if total == 0:
            return 0.0
        
        score = (positive_count - negative_count) / total
        return max(-1.0, min(1.0, score))
    
    def _adjust_for_context(self, text: str, base_score: float) -> float:
        """
        Adjust sentiment based on educational context
        
        Args:
            text: Review text
            base_score: Initial sentiment score
            
        Returns:
            Adjusted sentiment score
        """
        text_lower = text.lower()
        adjustment = 0.0
        
        # Detect soft critiques (reduce negative impact)
        for phrase in self.soft_critiques:
            if phrase in text_lower:
                adjustment += 0.1  # Soften the blow
        
        # Detect contrast structure
        if self._detect_contrast(text):
            # Reviews with "but" are typically mixed
            # Reduce extreme scores
            if abs(base_score) > 0.5:
                adjustment -= 0.2 * (base_score / abs(base_score))
        
        # Detect "sandwich" pattern (positive-negative-positive)
        sentences = self._split_sentences(text)
        if len(sentences) >= 3:
            sent_scores = [self._basic_sentiment(s) for s in sentences]
            if sent_scores[0] > 0 and sent_scores[-1] > 0:
                if any(s < 0 for s in sent_scores[1:-1]):
                    # Sandwich pattern detected
                    adjustment += 0.15
        
        return max(-1.0, min(1.0, base_score + adjustment))
    
    def _detect_contrast(self, text: str) -> bool:
        """Detect if text contains contrasting statements"""
        text_lower = text.lower()
        return any(word in text_lower for word in self.contrast_words)
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitter
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _get_sentiment_label(self, score: float) -> str:
        """Convert numerical score to label"""
        if score >= SENTIMENT_THRESHOLDS["very_positive"]:
            return "Very Positive"
        elif score >= SENTIMENT_THRESHOLDS["positive"]:
            return "Positive"
        elif score >= SENTIMENT_THRESHOLDS["neutral"]:
            return "Neutral"
        elif score >= SENTIMENT_THRESHOLDS["negative"]:
            return "Negative"
        else:
            return "Very Negative"
    
    def categorize_review(self, text: str) -> Dict[str, float]:
        """
        Categorize review into different aspects with sentiment scores
        
        Args:
            text: Review text
            
        Returns:
            Dictionary with category scores
        """
        text_lower = text.lower()
        category_scores = {}
        
        for category, keywords in CATEGORY_KEYWORDS.items():
            # Check if category is mentioned
            mentions = sum(1 for keyword in keywords if keyword in text_lower)
            
            if mentions > 0:
                # Extract sentences related to this category
                sentences = self._split_sentences(text)
                relevant_sentences = [
                    s for s in sentences
                    if any(keyword in s.lower() for keyword in keywords)
                ]
                
                if relevant_sentences:
                    # Analyze sentiment of relevant sentences
                    category_text = " ".join(relevant_sentences)
                    sentiment = self.analyze_sentiment(category_text)
                    category_scores[category] = sentiment['compound']
        
        return category_scores
    
    def extract_key_phrases(self, text: str, sentiment_type: str = "all") -> List[str]:
        """
        Extract key phrases from review based on sentiment
        
        Args:
            text: Review text
            sentiment_type: "positive", "negative", or "all"
            
        Returns:
            List of key phrases
        """
        sentences = self._split_sentences(text)
        key_phrases = []
        
        for sentence in sentences:
            sent_sentiment = self.analyze_sentiment(sentence)
            
            if sentiment_type == "all":
                key_phrases.append(sentence)
            elif sentiment_type == "positive" and sent_sentiment['compound'] > 0.2:
                key_phrases.append(sentence)
            elif sentiment_type == "negative" and sent_sentiment['compound'] < -0.2:
                key_phrases.append(sentence)
        
        return key_phrases
    
    def get_strengths_and_improvements(self, text: str) -> Tuple[List[str], List[str]]:
        """
        Extract strengths and areas for improvement
        
        Args:
            text: Review text
            
        Returns:
            Tuple of (strengths, improvements)
        """
        strengths = self.extract_key_phrases(text, "positive")
        improvements = self.extract_key_phrases(text, "negative")
        
        return (strengths[:3], improvements[:3])  # Limit to top 3
