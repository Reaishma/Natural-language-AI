"""
Sentiment Analysis Module
Analyzes sentiment using TextBlob and provides detailed emotional insights
"""
import streamlit as st
from textblob import TextBlob
import pandas as pd
from typing import Dict, Any, List
import re

class SentimentAnalyzer:
    def __init__(self):
        # Emotion keywords for detailed analysis
        self.emotion_keywords = {
            "joy": ["happy", "joy", "excited", "wonderful", "amazing", "fantastic", "great", "excellent", "love", "perfect"],
            "sadness": ["sad", "depressed", "unhappy", "disappointed", "terrible", "awful", "horrible", "hate", "worst", "miserable"],
            "anger": ["angry", "furious", "annoyed", "irritated", "mad", "frustrated", "outraged", "livid", "rage", "disgusted"],
            "fear": ["afraid", "scared", "worried", "anxious", "nervous", "terrified", "frightened", "panic", "concern", "stress"],
            "surprise": ["surprised", "shocked", "amazed", "astonished", "unexpected", "sudden", "wow", "incredible", "unbelievable"],
            "disgust": ["disgusting", "revolting", "sick", "gross", "awful", "repulsive", "horrible", "nasty", "terrible"]
        }
        
        # Intensity modifiers
        self.intensifiers = ["very", "extremely", "really", "quite", "so", "too", "incredibly", "absolutely", "totally"]
        self.diminishers = ["slightly", "somewhat", "rather", "fairly", "pretty", "kind of", "sort of", "a bit"]
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """
        Analyze sentiment using TextBlob and provide detailed insights
        """
        try:
            if not text or len(text.strip()) < 1:
                return {"error": "Text is empty or too short for analysis"}
            
            blob = TextBlob(text)
            
            # Basic sentiment analysis
            polarity = blob.sentiment.polarity  # -1 to 1
            subjectivity = blob.sentiment.subjectivity  # 0 to 1
            
            # Determine sentiment label
            if polarity > 0.1:
                sentiment_label = "Positive"
            elif polarity < -0.1:
                sentiment_label = "Negative"
            else:
                sentiment_label = "Neutral"
            
            # Determine confidence based on absolute polarity
            confidence = abs(polarity)
            
            # Analyze emotions
            emotion_scores = self.analyze_emotions(text)
            
            # Analyze intensity
            intensity_analysis = self.analyze_intensity(text)
            
            # Sentence-by-sentence analysis
            sentence_sentiments = []
            for sentence in blob.sentences:
                sent_polarity = sentence.sentiment.polarity
                sent_subjectivity = sentence.sentiment.subjectivity
                sentence_sentiments.append({
                    "text": str(sentence),
                    "polarity": sent_polarity,
                    "subjectivity": sent_subjectivity,
                    "sentiment": "Positive" if sent_polarity > 0.1 else "Negative" if sent_polarity < -0.1 else "Neutral"
                })
            
            return {
                "sentiment": sentiment_label,
                "polarity": polarity,
                "subjectivity": subjectivity,
                "confidence": confidence,
                "emotion_scores": emotion_scores,
                "intensity": intensity_analysis,
                "sentence_analysis": sentence_sentiments,
                "text_length": len(text),
                "word_count": len(text.split()),
                "sentence_count": len(sentence_sentiments)
            }
            
        except Exception as e:
            return {"error": f"Sentiment analysis failed: {str(e)}"}
    
    def analyze_emotions(self, text: str) -> Dict[str, float]:
        """
        Analyze specific emotions in the text
        """
        text_lower = text.lower()
        emotion_scores = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = 0
            for keyword in keywords:
                # Count occurrences with word boundaries
                matches = len(re.findall(r'\b' + re.escape(keyword) + r'\b', text_lower))
                score += matches
            
            # Normalize by text length
            if len(text.split()) > 0:
                emotion_scores[emotion] = score / len(text.split())
            else:
                emotion_scores[emotion] = 0
        
        return emotion_scores
    
    def analyze_intensity(self, text: str) -> Dict[str, Any]:
        """
        Analyze the intensity of emotions in the text
        """
        text_lower = text.lower()
        words = text_lower.split()
        
        intensifier_count = sum(1 for word in words if word in self.intensifiers)
        diminisher_count = sum(1 for word in words if word in self.diminishers)
        
        # Calculate intensity score
        total_modifiers = intensifier_count + diminisher_count
        if total_modifiers > 0:
            intensity_ratio = intensifier_count / total_modifiers
        else:
            intensity_ratio = 0.5  # Neutral
        
        # Determine intensity level
        if intensity_ratio > 0.7:
            intensity_level = "High"
        elif intensity_ratio > 0.4:
            intensity_level = "Medium"
        else:
            intensity_level = "Low"
        
        return {
            "level": intensity_level,
            "intensifiers": intensifier_count,
            "diminishers": diminisher_count,
            "ratio": intensity_ratio
        }
    
    def compare_sentiments(self, texts: List[str]) -> Dict[str, Any]:
        """
        Compare sentiments across multiple texts
        """
        try:
            results = []
            for i, text in enumerate(texts):
                analysis = self.analyze_sentiment(text)
                if "error" not in analysis:
                    results.append({
                        "text_id": f"Text {i+1}",
                        "preview": text[:50] + "..." if len(text) > 50 else text,
                        "sentiment": analysis["sentiment"],
                        "polarity": analysis["polarity"],
                        "subjectivity": analysis["subjectivity"],
                        "confidence": analysis["confidence"]
                    })
            
            if not results:
                return {"error": "No valid texts to compare"}
            
            # Calculate statistics
            polarities = [r["polarity"] for r in results]
            avg_polarity = sum(polarities) / len(polarities)
            
            return {
                "comparisons": results,
                "average_polarity": avg_polarity,
                "most_positive": max(results, key=lambda x: x["polarity"]),
                "most_negative": min(results, key=lambda x: x["polarity"]),
                "total_texts": len(results)
            }
            
        except Exception as e:
            return {"error": f"Sentiment comparison failed: {str(e)}"}

# Streamlit interface for sentiment analysis
def create_sentiment_analysis_interface():
    """
    Create the Streamlit interface for sentiment analysis
    """
    st.header("😊 Sentiment Analysis")
    st.write("Analyze the emotional tone and sentiment of your text with detailed insights.")
    
    analyzer = SentimentAnalyzer()
    
    # Analysis mode selection
    analysis_mode = st.selectbox(
        "Choose analysis mode:",
        ["Single Text Analysis", "Multiple Text Comparison", "Batch File Analysis"]
    )
    
    if analysis_mode == "Single Text Analysis":
        st.subheader("📝 Single Text Analysis")
        
        # Input options
        input_method = st.radio("Choose input method:", ["Text Input", "File Upload"])
        
        text_to_analyze = ""
        
        if input_method == "Text Input":
            text_to_analyze = st.text_area(
                "Enter text to analyze:",
                height=150,
                placeholder="Type or paste your text here..."
            )
        else:
            uploaded_file = st.file_uploader(
                "Upload a text file:",
                type=['txt'],
                help="Upload a .txt file to analyze sentiment"
            )
            if uploaded_file:
                from utils.helpers import handle_file_upload
                text_to_analyze = handle_file_upload(uploaded_file)
        
        if st.button("Analyze Sentiment", type="primary"):
            if text_to_analyze and len(text_to_analyze.strip()) > 0:
                with st.spinner("Analyzing sentiment..."):
                    result = analyzer.analyze_sentiment(text_to_analyze)
                    
                    if "error" not in result:
                        # Main sentiment result
                        st.subheader("🎯 Overall Sentiment")
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            sentiment_color = "🟢" if result["sentiment"] == "Positive" else "🔴" if result["sentiment"] == "Negative" else "🟡"
                            st.metric("Sentiment", f"{sentiment_color} {result['sentiment']}")
                        
                        with col2:
                            st.metric("Polarity", f"{result['polarity']:.3f}")
                            st.caption("(-1 = Very Negative, +1 = Very Positive)")
                        
                        with col3:
                            st.metric("Subjectivity", f"{result['subjectivity']:.3f}")
                            st.caption("(0 = Objective, 1 = Subjective)")
                        
                        # Emotion analysis
                        st.subheader("🎭 Emotion Analysis")
                        emotion_scores = result["emotion_scores"]
                        if any(score > 0 for score in emotion_scores.values()):
                            # Create emotion dataframe
                            emotion_df = pd.DataFrame([
                                {"Emotion": emotion.title(), "Score": score}
                                for emotion, score in emotion_scores.items()
                                if score > 0
                            ]).sort_values("Score", ascending=False)
                            
                            if not emotion_df.empty:
                                st.dataframe(emotion_df, use_container_width=True)
                            else:
                                st.info("No specific emotions detected in the text.")
                        else:
                            st.info("No specific emotions detected in the text.")
                        
                        # Intensity analysis
                        st.subheader("⚡ Intensity Analysis")
                        intensity = result["intensity"]
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Intensity Level", intensity["level"])
                        with col2:
                            st.metric("Intensifiers", intensity["intensifiers"])
                        with col3:
                            st.metric("Diminishers", intensity["diminishers"])
                        
                        # Sentence-by-sentence analysis
                        if len(result["sentence_analysis"]) > 1:
                            st.subheader("📄 Sentence-by-Sentence Analysis")
                            
                            sentence_df = pd.DataFrame(result["sentence_analysis"])
                            sentence_df["text"] = sentence_df["text"].str[:100] + "..."
                            sentence_df.columns = ["Text Preview", "Polarity", "Subjectivity", "Sentiment"]
                            
                            st.dataframe(sentence_df, use_container_width=True)
                        
                        # Text statistics
                        st.subheader("📊 Text Statistics")
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Characters", result["text_length"])
                        with col2:
                            st.metric("Words", result["word_count"])
                        with col3:
                            st.metric("Sentences", result["sentence_count"])
                    
                    else:
                        from utils.helpers import display_error
                        display_error(result["error"])
            else:
                from utils.helpers import display_error
                display_error("Please enter some text to analyze.")
    
    elif analysis_mode == "Multiple Text Comparison":
        st.subheader("📊 Multiple Text Comparison")
        
        num_texts = st.slider("Number of texts to compare:", min_value=2, max_value=5, value=2)
        
        texts = []
        for i in range(num_texts):
            text = st.text_area(f"Text {i+1}:", height=100, key=f"text_{i}")
            if text:
                texts.append(text)
        
        if st.button("Compare Sentiments", type="primary"):
            if len(texts) >= 2:
                with st.spinner("Comparing sentiments..."):
                    result = analyzer.compare_sentiments(texts)
                    
                    if "error" not in result:
                     # Comparison overview
                        st.subheader("📈 Comparison Overview")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.metric("Average Polarity", f"{result['average_polarity']:.3f}")
                        with col2:
                            st.metric("Texts Analyzed", result["total_texts"])
                        
                        # Detailed comparison
                        st.subheader("📋 Detailed Comparison")
                        comparison_df = pd.DataFrame(result["comparisons"])
                        st.dataframe(comparison_df, use_container_width=True)
                        
                        # Highlights
                        st.subheader("🏆 Highlights")
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.success("**Most Positive:**")
                            st.write(f"**{result['most_positive']['text_id']}** (Polarity: {result['most_positive']['polarity']:.3f})")
                            st.caption(result['most_positive']['preview'])
                        
                        with col2:
                            st.error("**Most Negative:**")
                            st.write(f"**{result['most_negative']['text_id']}** (Polarity: {result['most_negative']['polarity']:.3f})")
                            st.caption(result['most_negative']['preview'])
                    
                    else:
                        from utils.helpers import display_error
                        display_error(result["error"])
            else:
                from utils.helpers import display_error
                display_error("Please enter at least 2 texts to compare.")
    
    elif analysis_mode == "Batch File Analysis":
        st.subheader("📁 Batch File Analysis")
        st.info("Upload multiple text files to analyze their sentiments in batch.")
        
        uploaded_files = st.file_uploader(
            "Upload text files:",
            type=['txt'],
            accept_multiple_files=True,
            help="Upload multiple .txt files for batch analysis"
        )
        
        if uploaded_files and st.button("Analyze All Files", type="primary"):
            if len(uploaded_files) > 0:
                with st.spinner(f"Analyzing {len(uploaded_files)} files..."):
                    batch_results = []
                    
                    for uploaded_file in uploaded_files:
                        from utils.helpers import handle_file_upload
                        file_content = handle_file_upload(uploaded_file)
                        
                        if file_content:
                            result = analyzer.analyze_sentiment(file_content)
                            if "error" not in result:
                                batch_results.append({
                                    "filename": uploaded_file.name,
                                    "sentiment": result["sentiment"],
                                    "polarity": result["polarity"],
                                    "subjectivity": result["subjectivity"],
                                    "confidence": result["confidence"],
                                    "word_count": result["word_count"]
                                })
                    
                    if batch_results:
                        st.subheader("📊 Batch Analysis Results")
                        
                        # Create results dataframe
                        results_df = pd.DataFrame(batch_results)
                        st.dataframe(results_df, use_container_width=True)
                        
                        # Summary statistics
                        st.subheader("📈 Summary Statistics")
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            positive_count = len([r for r in batch_results if r["sentiment"] == "Positive"])
                            st.metric("Positive Files", positive_count)
                        
                        with col2:
                            negative_count = len([r for r in batch_results if r["sentiment"] == "Negative"])
                            st.metric("Negative Files", negative_count)
                        
                        with col3:
                            neutral_count = len([r for r in batch_results if r["sentiment"] == "Neutral"])
                            st.metric("Neutral Files", neutral_count)
                        
                        with col4:
                            avg_polarity = sum(r["polarity"] for r in batch_results) / len(batch_results)
                            st.metric("Avg Polarity", f"{avg_polarity:.3f}")
                        
                        # Download results
                        csv_data = results_df.to_csv(index=False)
                        st.download_button(
                            label="📥 Download Results as CSV",
                            data=csv_data,
                            file_name="sentiment_analysis_results.csv",
                            mime="text/csv"
                        )
                    else:
                        from utils.helpers import display_error
                        display_error("No valid files could be analyzed.")

if __name__ == "__main__":
    create_sentiment_analysis_interface()
