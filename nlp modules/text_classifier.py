"""
Text Classification Module
Classifies text into predefined categories using TextBlob and basic heuristics
"""
import streamlit as st
from textblob import TextBlob
import re
from typing import Dict, Any

class TextClassifier:
    def __init__(self):
        self.categories = {
            "technology": ["computer", "software", "tech", "programming", "code", "app", "digital", "internet", "ai", "machine learning"],
            "business": ["company", "market", "finance", "money", "profit", "sales", "business", "corporate", "investment"],
            "sports": ["game", "player", "team", "score", "match", "sport", "football", "basketball", "soccer", "tennis"],
            "health": ["doctor", "medicine", "hospital", "health", "disease", "treatment", "medical", "patient", "therapy"],
            "education": ["school", "student", "teacher", "learn", "education", "university", "study", "class", "academic"],
            "entertainment": ["movie", "music", "show", "actor", "celebrity", "film", "concert", "entertainment", "tv"],
            "news": ["breaking", "report", "news", "journalist", "headline", "story", "media", "press"],
            "personal": ["i", "me", "my", "myself", "personal", "life", "family", "friend", "relationship"]
        }
    
    def classify_text(self, text: str) -> Dict[str, Any]:
        """
        Classify text into categories based on keyword matching and sentiment
        """
        try:
            if not text or len(text.strip()) < 3:
                return {
                    "category": "unknown",
                    "confidence": 0.0,
                    "error": "Text too short for classification"
                }
            
            text_lower = text.lower()
            blob = TextBlob(text)
            
            # Calculate category scores
            category_scores = {}
            for category, keywords in self.categories.items():
                score = 0
                for keyword in keywords:
                    # Count keyword occurrences (with word boundaries)
                    matches = len(re.findall(r'\b' + re.escape(keyword) + r'\b', text_lower))
                    score += matches
                
                # Normalize score by text length
                if len(text.split()) > 0:
                    category_scores[category] = score / len(text.split())
                else:
                    category_scores[category] = 0
            
            # Find the category with highest score
            if max(category_scores.values()) > 0:
                best_category = max(category_scores, key=category_scores.get)
                confidence = min(category_scores[best_category] * 2, 1.0)  # Scale confidence
            else:
                # Fallback: use sentiment to determine if it's personal or general
                sentiment = blob.sentiment.polarity
                if abs(sentiment) > 0.3:  # Strong sentiment suggests personal content
                    best_category = "personal"
                    confidence = abs(sentiment) * 0.7
                else:
                    best_category = "general"
                    confidence = 0.3
            
            return {
                "category": best_category,
                "confidence": confidence,
                "all_scores": category_scores,
                "text_length": len(text),
                "word_count": len(text.split())
            }
            
        except Exception as e:
            return {
                "category": "error",
                "confidence": 0.0,
                "error": f"Classification failed: {str(e)}"
            }
    
    def get_category_description(self, category: str) -> str:
        """
        Get description for a category
        """
        descriptions = {
            "technology": "Technology-related content including computers, software, and digital topics",
            "business": "Business and finance-related content",
            "sports": "Sports and athletics-related content",
            "health": "Health and medical-related content",
            "education": "Educational and academic content",
            "entertainment": "Entertainment industry and media content",
            "news": "News and journalism content",
            "personal": "Personal experiences and opinions",
            "general": "General content that doesn't fit specific categories",
            "unknown": "Unable to classify the content"
        }
        return descriptions.get(category, "No description available")

# Streamlit interface for text classification
def create_text_classification_interface():
    """
    Create the Streamlit interface for text classification
    """
    st.header("📝 Text Classification")
    st.write("Classify your text into different categories to understand its content type.")
    
    classifier = TextClassifier()
    
    # Input options
    input_method = st.radio("Choose input method:", ["Text Input", "File Upload"])
    
    text_to_classify = ""
    
    if input_method == "Text Input":
        text_to_classify = st.text_area(
            "Enter text to classify:",
            height=150,
            placeholder="Type or paste your text here..."
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload a text file:",
            type=['txt'],
            help="Upload a .txt file to classify its content"
        )
        if uploaded_file:
            from utils.helpers import handle_file_upload
            text_to_classify = handle_file_upload(uploaded_file)
    
    if st.button("Classify Text", type="primary"):
        if text_to_classify and len(text_to_classify.strip()) > 0:
            with st.spinner("Classifying text..."):
                results = classifier.classify_text(text_to_classify)
                
                if "error" not in results:
                    # Display main result
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Category", results["category"].title())
                    with col2:
                        st.metric("Confidence", f"{results['confidence']:.1%}")
                    
                    # Display category description
                    description = classifier.get_category_description(results["category"])
                    st.info(f"**Category Description:** {description}")
                    
                    # Display detailed scores
                    if "all_scores" in results:
                        st.subheader("Detailed Category Scores")
                        scores_df = pd.DataFrame([
                            {"Category": cat.title(), "Score": score}
                            for cat, score in results["all_scores"].items()
                        ]).sort_values("Score", ascending=False)
                        
                        st.dataframe(scores_df, use_container_width=True)
                        
                        # Show text statistics
                        st.subheader("Text Statistics")
                        stat_col1, stat_col2 = st.columns(2)
                        with stat_col1:
                            st.metric("Characters", results.get("text_length", 0))
                        with stat_col2:
                            st.metric("Words", results.get("word_count", 0))
                else:
                    from utils.helpers import display_error
                    display_error(results["error"])
        else:
            from utils.helpers import display_error
            display_error("Please enter some text to classify.")

if __name__ == "__main__":
    import pandas as pd
    create_text_classification_interface()
  
