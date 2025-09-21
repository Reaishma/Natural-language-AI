NLP Virtual Assistant - Main Application
A comprehensive NLP tool with multiple capabilities built with Streamlit
"""
import streamlit as st
import time
from datetime import datetime

# Import all NLP modules
from nlp_modules.text_classifier import create_text_classification_interface
from nlp_modules.text_generator import create_text_generation_interface
from nlp_modules.summarizer import create_text_summarization_interface
from nlp_modules.sentiment_analyzer import create_sentiment_analysis_interface
from nlp_modules.translator import create_translation_interface
from nlp_modules.question_answerer import create_question_answering_interface
from nlp_modules.ner_extractor import create_ner_interface



def main():
    """
    Main application function
    """
    # Configure page
    st.set_page_config(
        page_title="NLP Virtual Assistant",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    
    # Sidebar navigation
    with st.sidebar:
        st.image("https://via.placeholder.com/200x100/4CAF50/FFFFFF?text=NLP+Assistant", width=200)
        st.title("🤖 NLP Assistant")
        st.markdown("---")

        # Navigation menu
        selected_tool = st.selectbox(
            "Choose NLP Tool:",
            [
                "🏠 Home",
                "📝 Text Classification", 
                "✍️ Text Generation",
                "📄 Text Summarization",
                "😊 Sentiment Analysis",
                "🌍 Language Translation",
                "❓ Question Answering",
                "🏷️ Named Entity Recognition"
            ]
        )

        st.markdown("---")

        # About section
        with st.expander("ℹ️ About"):
            st.write("""
            **NLP Virtual Assistant** is a comprehensive tool that provides:
            
            - **Text Classification**: Categorize text content
            - **Text Generation**: Create stories, emails, blogs
            - **Summarization**: Extract key information
            - **Sentiment Analysis**: Analyze emotional tone
            - **Translation**: Multi-language support
            - **Question Answering**: Get answers from context
            - **NER**: Extract entities from text
            """)

        # Statistics (if available in session state)
        if hasattr(st.session_state, 'usage_stats'):
            with st.expander("📊 Usage Statistics"):
                stats = st.session_state.usage_stats
                for tool, count in stats.items():
                    st.metric(tool, count)

    # Main content area
    if selected_tool == "🏠 Home":
        show_home_page()
    elif selected_tool == "📝 Text Classification":
        track_usage("Text Classification")
        create_text_classification_interface()
    elif selected_tool == "✍️ Text Generation":
        track_usage("Text Generation")
        create_text_generation_interface()
    elif selected_tool == "📄 Text Summarization":
        track_usage("Text Summarization")
        create_text_summarization_interface()
    elif selected_tool == "😊 Sentiment Analysis":
        track_usage("Sentiment Analysis")
        create_sentiment_analysis_interface()
    elif selected_tool == "🌍 Language Translation":
        track_usage("Language Translation")
        create_translation_interface()
    elif selected_tool == "❓ Question Answering":
        track_usage("Question Answering")
        create_question_answering_interface()
    elif selected_tool == "🏷️ Named Entity Recognition":
        track_usage("Named Entity Recognition")
        create_ner_interface()


def show_home_page():
    """
    Display the home page with overview and features
    """
    # Main header
    st.markdown('<div class="main-header">', unsafe_allow_html=True)
    st.title("🤖 NLP Virtual Assistant")
    st.markdown("**Your Complete Natural Language Processing Toolkit**")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Welcome message
    st.markdown("""
    Welcome to the **NLP Virtual Assistant** - a powerful, all-in-one natural language processing tool 
    that helps you analyze, understand, and generate text content with ease.
    """)

    # Feature overview
    st.subheader("🚀 Available Features")

    # Create feature cards in columns
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 📝 **Text Classification**
        Automatically categorize your text into different topics like technology, business, sports, health, and more.
        
        ### ✍️ **Text Generation**
        Create engaging content including stories, professional emails, blog posts, and text continuations.
        
        ### 📄 **Text Summarization**
        Extract key information from long documents with extractive summarization and bullet points.
        
        ### 😊 **Sentiment Analysis**
        Analyze the emotional tone of text with detailed emotion detection and intensity analysis.
        """)

    with col2:
        st.markdown("""
        ### 🌍 **Language Translation**
        Translate text between multiple languages with automatic language detection.
        
        ### ❓ **Question Answering**
        Get intelligent answers to questions based on provided context documents.
        
        ### 🏷️ **Named Entity Recognition**
        Extract and identify people, organizations, locations, dates, and other entities from text.
        
        ### 🔧 **Batch Processing**
        Process multiple texts or files at once for efficient workflow management.
        """)

    # Quick start guide
    st.subheader("🎯 Quick Start Guide")

    with st.expander("📖 How to Get Started"):
        st.markdown("""
        1. **Select a Tool**: Use the sidebar to choose the NLP feature you want to use
        2. **Input Your Text**: Either type directly or upload a text file
        3. **Configure Options**: Adjust settings based on your needs
        4. **Get Results**: View comprehensive analysis and download results
        5. **Try Different Tools**: Experiment with various NLP capabilities
        
        ### 💡 Tips for Best Results:
        - Use clear, well-formatted text for better analysis
        - For question answering, provide comprehensive context
        - Try different summarization ratios to find the optimal length
        - Use batch processing for multiple documents
        """)

    # Sample use cases
    st.subheader("💼 Common Use Cases")

    use_case_tabs = st.tabs(["📊 Business", "🎓 Education", "📰 Content", "🔬 Research"])

    with use_case_tabs[0]:
        st.markdown("""
        **Business Applications:**
        - Analyze customer feedback sentiment
        - Classify support tickets automatically
        - Generate professional email responses
        - Summarize meeting notes and reports
        - Translate content for global audiences
        """)

    with use_case_tabs[1]:
        st.markdown("""
        **Educational Use:**
        - Summarize academic papers and articles
        - Extract key concepts from textbooks
        - Analyze essay sentiment and tone
        - Generate study questions from content
        - Translate educational materials
        """)

    with use_case_tabs[2]:
        st.markdown("""
        **Content Creation:**
        - Generate blog post ideas and outlines
        - Analyze content sentiment for audience targeting
        - Create multilingual content versions
        - Extract entities for SEO optimization
        - Summarize competitor content
        """)

    with use_case_tabs[3]:
        st.markdown("""
        **Research Applications:**
        - Extract entities from research papers
        - Summarize literature reviews
        - Classify research topics
        - Analyze survey responses
        - Generate research questions
        """)

    # Recent updates or announcements
    st.subheader("📢 System Information")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info("**Status**: ✅ All systems operational")

    with col2:
        st.info(f"**Last Updated**: {datetime.now().strftime('%Y-%m-%d')}")

    with col3:
        st.info("**Version**: 1.0.0")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        Built using Streamlit | Powered by Advanced NLP Libraries
    </div>
    """, unsafe_allow_html=True)

def track_usage(tool_name):
    """
    Track usage statistics for analytics
    """
    if 'usage_stats' not in st.session_state:
        st.session_state.usage_stats = {}

    if tool_name not in st.session_state.usage_stats:
        st.session_state.usage_stats[tool_name] = 0

    st.session_state.usage_stats[tool_name] += 1

def show_error_page(error_message):
    
    Display error page when something goes wrong
    
    st.error("🚨 Application Error")
    st.write(f"An error occurred: {error_message}")
    st.write("Please try refreshing the page or contact support if the issue persists.")

    if st.button("🔄 Refresh Page"):
        st.rerun()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        show_error_page(str(e))
