# NLP Virtual Assistant

This a comprehensive Natural Language Processing (NLP) Virtual OvermodularrThis built with Streamlit. The application provides multiple NLP capabilities including text classification, sentiment analysis, text generation, summarization, named entity recognition, question answering, and language translation. The system is designed as a modular web application that allows users to interact with various NLP tools through a unified interface.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a modular architecture with clear separation of concerns:

- **Frontend**: Streamlit-based web interface providing an interactive user experience
- **Backend**: Python-based NLP processing modules using libraries like TextBlob, NLTK, and googletrans
- **Module Structure**: Each NLP capability is implemented as a separate module in the `nlp_modules` package
- **Utilities**: Helper functions for result display and data formatting

## Key Components

### Frontend Layer
- **Main Application** (`app.py`): Streamlit-based web interface with sidebar navigation and responsive layout
- **UI Configuration**: Wide layout with expandable sidebar, custom CSS styling, and placeholder branding

### NLP Processing Modules
- **Text Classifier** (`text_classifier.py`): Categorizes text into predefined topics (technology, business, sports, health, education, entertainment, news, personal)
- **Sentiment Analyzer** (`sentiment_analyzer.py`): Analyzes emotional tone using TextBlob with detailed emotion keyword detection
- **Text Generator** (`text_generator.py`): Creates content using template-based generation for stories, emails, and blog posts
- **Text Summarizer** (`summarizer.py`): Performs extractive summarization using NLTK with TF-IDF scoring
- **Named Entity Recognizer** (`ner_extractor.py`): Extracts entities using rule-based patterns and NLTK
- **Question Answerer** (`question_answerer.py`): Basic Q&A using pattern matching and text search
- **Language Translator** (`translator.py`): Multi-language translation using Google Translate API

### Utility Layer
- **Helper Functions** (`utils/helpers.py`): Display formatting and result presentation utilities

## Data Flow

1. **User Input**: Text input through Streamlit interface
2. **Module Selection**: User selects specific NLP capability from sidebar navigation
3. **Processing**: Selected module processes input using appropriate NLP libraries
4. **Result Generation**: Processed data is formatted into structured results
5. **Display**: Results are presented through utility functions with appropriate visualizations

## External Dependencies

### Core Libraries
- **Streamlit**: Web application framework for the frontend interface
- **TextBlob**: Primary NLP library for sentiment analysis and basic text processing
- **NLTK**: Advanced NLP processing for tokenization, stopwords, and entity recognition
- **googletrans**: Google Translate API for language translation
- **pandas**: Data manipulation and result formatting

### Data Requirements
- NLTK corpora downloads (punkt tokenizer, stopwords, NE chunker, POS tagger)
- No persistent database storage required
- Real-time processing of user input

## Deployment Strategy

The application is designed for deployment on cloud platforms with the following characteristics:

### Recommended Platform
- **Replit**: Primary deployment target with built-in Python environment support
- **Alternative Platforms**: Streamlit Cloud, Heroku, or any Python-supporting cloud service

### Configuration Requirements
- Python 3.7+ runtime environment
- Automatic dependency installation via requirements.txt (implied)
- Internet connectivity for Google Translate API and NLTK downloads
- No database setup required (stateless application)

### Scalability Considerations
- Stateless design allows for easy horizontal scaling
- Module-based architecture enables selective feature deployment
- Memory-efficient processing suitable for small to medium-scale usage
- API rate limiting considerations for Google Translate integration

### Security Notes
- No user authentication implemented (public access model)
- No sensitive data storage
- External API dependency on Google Translate (consider rate limits and privacy implications)