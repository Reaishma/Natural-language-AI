"""
Text Summarization Module
Summarizes text using extractive summarization techniques with NLTK
"""
import streamlit as st
import nltk
from textblob import TextBlob
import re
from typing import Dict, Any, List
from collections import Counter
import math

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize

class TextSummarizer:
    def __init__(self):
        try:
            self.stop_words = set(stopwords.words('english'))
        except:
            # Fallback stop words if NLTK download fails
            self.stop_words = set([
                'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours',
                'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers',
                'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves',
                'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are',
                'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does',
                'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until',
                'while', 'of', 'at', 'by', 'for', 'with', 'through', 'during', 'before', 'after',
                'above', 'below', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
                'further', 'then', 'once'
            ])
    
    def preprocess_text(self, text: str) -> List[str]:
        """
        Preprocess text by cleaning and tokenizing into sentences
        """
        # Clean text
        text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespace with single space
        text = text.strip()
        
        # Tokenize into sentences
        try:
            sentences = sent_tokenize(text)
        except:
            # Fallback sentence splitting
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
        
        return sentences
    
    def calculate_word_frequencies(self, text: str) -> Dict[str, float]:
        """
        Calculate normalized word frequencies
        """
        try:
            words = word_tokenize(text.lower())
        except:
            # Fallback word tokenization
            words = re.findall(r'\b\w+\b', text.lower())
        
        # Remove stop words and punctuation
        words = [word for word in words if word.isalpha() and word not in self.stop_words]
        
        # Calculate frequencies
        word_freq = Counter(words)
        
        # Normalize frequencies
        max_freq = max(word_freq.values()) if word_freq else 1
        for word in word_freq:
            word_freq[word] = word_freq[word] / max_freq
        
        return word_freq
    
    def score_sentences(self, sentences: List[str], word_freq: Dict[str, float]) -> Dict[int, float]:
        """
        Score sentences based on word frequencies
        """
        sentence_scores = {}
        
        for i, sentence in enumerate(sentences):
            try:
                words = word_tokenize(sentence.lower())
            except:
                words = re.findall(r'\b\w+\b', sentence.lower())
            
            words = [word for word in words if word.isalpha() and word not in self.stop_words]
            
            if len(words) > 0:
                score = 0
                for word in words:
                    if word in word_freq:
                        score += word_freq[word]
                
                # Normalize by sentence length
                sentence_scores[i] = score / len(words)
            else:
                sentence_scores[i] = 0
        
        return sentence_scores
    
    def extractive_summarize(self, text: str, summary_ratio: float = 0.3) -> Dict[str, Any]:
        """
        Create extractive summary by selecting top-scoring sentences
        """
        try:
            if not text or len(text.strip()) < 50:
                return {
                    "summary": text,
                    "summary_ratio": 1.0,
                    "sentences_selected": 1,
                    "compression_ratio": 1.0,
                    "error": "Text too short for summarization"
                }
            
            # Preprocess text
            sentences = self.preprocess_text(text)
            
            if len(sentences) <= 2:
                return {
                    "summary": text,
                    "summary_ratio": 1.0,
                    "sentences_selected": len(sentences),
                    "compression_ratio": 1.0,
                    "original_sentences": len(sentences)
                }
            
            # Calculate word frequencies
            word_freq = self.calculate_word_frequencies(text)
            
            # Score sentences
            sentence_scores = self.score_sentences(sentences, word_freq)
            
            # Select top sentences
            num_sentences = max(1, int(len(sentences) * summary_ratio))
            top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
            
            # Sort selected sentences by original order
            selected_indices = sorted([idx for idx, score in top_sentences])
            summary_sentences = [sentences[i] for i in selected_indices]
            
            summary = ' '.join(summary_sentences)
            
            return {
                "summary": summary,
                "original_length": len(text.split()),
                "summary_length": len(summary.split()),
                "original_sentences": len(sentences),
                "sentences_selected": num_sentences,
                "compression_ratio": len(summary) / len(text),
                "summary_ratio": summary_ratio
            }
            
        except Exception as e:
            return {"error": f"Summarization failed: {str(e)}"}
    
    def bullet_point_summary(self, text: str, max_points: int = 5) -> Dict[str, Any]:
        """
        Create bullet point summary with key insights
        """
        try:
            sentences = self.preprocess_text(text)
            
            if len(sentences) <= max_points:
                return {
                    "bullet_points": [f"• {sentence}" for sentence in sentences],
                    "num_points": len(sentences),
                    "type": "bullet_point"
                }
            
            word_freq = self.calculate_word_frequencies(text)
            sentence_scores = self.score_sentences(sentences, word_freq)
            
            # Select top sentences for bullet points
            top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:max_points]
            selected_indices = sorted([idx for idx, score in top_sentences])
            
            bullet_points = [f"• {sentences[i]}" for i in selected_indices]
            
            return {
                "bullet_points": bullet_points,
                "num_points": len(bullet_points),
                "original_sentences": len(sentences),
                "type": "bullet_point"
            }
            
        except Exception as e:
            return {"error": f"Bullet point summarization failed: {str(e)}"}
    
    def keyword_summary(self, text: str, num_keywords: int = 10) -> Dict[str, Any]:
        """
        Extract key terms and phrases from text
        """
        try:
            blob = TextBlob(text)
            
            # Get word frequencies
            word_freq = self.calculate_word_frequencies(text)
            
            # Get top keywords
            top_keywords = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:num_keywords]
            
            # Extract noun phrases
            noun_phrases = list(blob.noun_phrases)
            
            # Get top noun phrases by frequency
            phrase_freq = Counter(noun_phrases)
            top_phrases = [phrase for phrase, count in phrase_freq.most_common(5)]
            
            return {
                "keywords": [word for word, freq in top_keywords],
                "key_phrases": top_phrases,
                "word_frequencies": dict(top_keywords),
                "total_unique_words": len(word_freq),
                "type": "keyword"
            }
            
        except Exception as e:
            return {"error": f"Keyword extraction failed: {str(e)}"}

# Streamlit interface for text summarization
def create_text_summarization_interface():
    """
    Create the Streamlit interface for text summarization
    """
    st.header("📄 Text Summarization")
    st.write("Summarize long documents and extract key information using advanced NLP techniques.")
    
    summarizer = TextSummarizer()
    
    # Input options
    input_method = st.radio("Choose input method:", ["Text Input", "File Upload"])
    
    text_to_summarize = ""
    
    if input_method == "Text Input":
        text_to_summarize = st.text_area(
            "Enter text to summarize:",
            height=200,
            placeholder="Paste your long text here..."
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload a text file:",
            type=['txt'],
            help="Upload a .txt file to summarize"
        )
        if uploaded_file:
            from utils.helpers import handle_file_upload
            text_to_summarize = handle_file_upload(uploaded_file)
    
    if text_to_summarize:
        # Display text statistics
        st.subheader("📊 Text Statistics")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Characters", len(text_to_summarize))
        with col2:
            st.metric("Words", len(text_to_summarize.split()))
        with col3:
            st.metric("Sentences", len(summarizer.preprocess_text(text_to_summarize)))
        with col4:
            st.metric("Paragraphs", text_to_summarize.count('\n\n') + 1)
        
        # Summarization options
        st.subheader("🎯 Summarization Options")
        
        summary_type = st.selectbox(
            "Choose summary type:",
            ["Extractive Summary", "Bullet Points", "Keywords & Phrases"]
        )
        
        if summary_type == "Extractive Summary":
            col1, col2 = st.columns(2)
            with col1:
                summary_ratio = st.slider(
                    "Summary length (% of original):",
                    min_value=10,
                    max_value=80,
                    value=30,
                    step=10
                ) / 100
            with col2:
                st.metric("Target sentences", int(len(summarizer.preprocess_text(text_to_summarize)) * summary_ratio))
            
            if st.button("Generate Summary", type="primary"):
                with st.spinner("Creating summary..."):
                    result = summarizer.extractive_summarize(text_to_summarize, summary_ratio)
                    
                    if "error" not in result:
                        st.subheader("📝 Summary")
                        st.write(result["summary"])
                        
                        # Summary statistics
                        st.subheader("📊 Summary Statistics")
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric("Original Words", result.get("original_length", 0))
                        with col2:
                            st.metric("Summary Words", result.get("summary_length", 0))
                        with col3:
                            st.metric("Compression Ratio", f"{result.get('compression_ratio', 0):.1%}")
                        with col4:
                            st.metric("Sentences Used", f"{result.get('sentences_selected', 0)}/{result.get('original_sentences', 0)}")
                        
                        from utils.helpers import create_download_link
                        create_download_link(
                            result["summary"],
                            "summary.txt",
                            "📥 Download Summary"
                        )
                    else:
                        from utils.helpers import display_error
                        display_error(result["error"])
        
        elif summary_type == "Bullet Points":
            max_points = st.slider("Maximum bullet points:", min_value=3, max_value=10, value=5)
            
            if st.button("Generate Bullet Points", type="primary"):
                with st.spinner("Creating bullet points..."):
                    result = summarizer.bullet_point_summary(text_to_summarize, max_points)
                    
                    if "error" not in result:
                        st.subheader("🔸 Key Points")
                        for point in result["bullet_points"]:
                            st.write(point)
                        
                        st.info(f"Generated {result['num_points']} bullet points from {result.get('original_sentences', 0)} sentences.")
                        
                        bullet_text = "\n".join(result["bullet_points"])
                        from utils.helpers import create_download_link
                        create_download_link(
                            bullet_text,
                            "bullet_points.txt",
                            "📥 Download Bullet Points"
                        )
                    else:
                        from utils.helpers import display_error
                        display_error(result["error"])
        
        elif summary_type == "Keywords & Phrases":
            num_keywords = st.slider("Number of keywords:", min_value=5, max_value=20, value=10)
            
            if st.button("Extract Keywords", type="primary"):
                with st.spinner("Extracting keywords..."):
                    result = summarizer.keyword_summary(text_to_summarize, num_keywords)
                    
                    if "error" not in result:
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.subheader("🔑 Top Keywords")
                            for i, keyword in enumerate(result["keywords"], 1):
                                st.write(f"{i}. {keyword}")
                        
                        with col2:
                            st.subheader("💭 Key Phrases")
                            for i, phrase in enumerate(result["key_phrases"], 1):
                                st.write(f"{i}. {phrase}")
                        
                        st.info(f"Found {result['total_unique_words']} unique words in the text.")
                        
                        # Create downloadable content
                        keywords_text = "Keywords:\n" + "\n".join([f"- {kw}" for kw in result["keywords"]])
                        keywords_text += "\n\nKey Phrases:\n" + "\n".join([f"- {phrase}" for phrase in result["key_phrases"]])
                        
                        from utils.helpers import create_download_link
                        create_download_link(
                            keywords_text,
                            "keywords_and_phrases.txt",
                            "📥 Download Keywords & Phrases"
                        )
                    else:
                        from utils.helpers import display_error
                        display_error(result["error"])

if __name__ == "__main__":
    import pandas as pd
    create_text_summarization_interface()
