# 🤖 NLP Virtual Assistant

<div align="center">


**🤖See the virtual Assistant on Streamlit https://natural-language-ai-gwrfrjcjl8f62rmpgfay45.streamlit.app/**

**Web Interface on https://reaishma.github.io/Natural-language-AI/**


This a comprehensive Natural Language Processing (NLP) built with Streamlit. The application provides multiple NLP capabilities including text classification, sentiment analysis, text generation, summarization, named entity recognition, question answering, and language translation. The system is designed as a modular web application that allows users to interact with various NLP tools through a unified interface.

![Overview](https://github.com/Reaishma/Natural-language-AI/blob/main/Nlp%20assistant.png)

## 🛠️ System Architecture

The application follows a modular architecture with clear separation of concerns:

- **Frontend**: Streamlit-based web interface providing an interactive user experience
- **Backend**: Python-based NLP processing modules using libraries like TextBlob, NLTK, and googletrans
- **Module Structure**: Each NLP capability is implemented as a separate module in the `nlp_modules` package
- **Utilities**: Helper functions for result display and data formatting

## ✅ Key Components

### Frontend Layer
- **Main Application** (`app.py`): Streamlit-based web interface with sidebar navigation and responsive layout
- **UI Configuration**: Wide layout with expandable sidebar, custom CSS styling, and placeholder branding

### 📌 NLP Processing Modules

![NLP modules](https://github.com/Reaishma/Natural-language-AI/blob/main/Text%20classification.png)

- **Text Classifier** (`text_classifier.py`): Categorizes text into predefined topics (technology, business, sports, health, education, entertainment, news, personal)
- **Sentiment Analyzer** (`sentiment_analyzer.py`): Analyzes emotional tone using TextBlob with detailed emotion keyword detection
- **Text Generator** (`text_generator.py`): Creates content using template-based generation for stories, emails, and blog posts
- **Text Summarizer** (`summarizer.py`): Performs extractive summarization using NLTK with TF-IDF scoring
- **Named Entity Recognizer** (`ner_extractor.py`): Extracts entities using rule-based patterns and NLTK
- **Question Answerer** (`question_answerer.py`): Basic Q&A using pattern matching and text search
- **Language Translator** (`translator.py`): Multi-language translation using Google Translate API

### Utility Layer
- **Helper Functions** (`utils/helpers.py`): Display formatting and result presentation utilities

## 📍 Data Flow

1. **User Input**: Text input through Streamlit interface
2. **Module Selection**: User selects specific NLP capability from sidebar navigation
3. **Processing**: Selected module processes input using appropriate NLP libraries
4. **Result Generation**: Processed data is formatted into structured results
5. **Display**: Results are presented through utility functions with appropriate visualizations

### 🚀 Quick Start Guide

1. **Select a Tool**: Use the sidebar to choose the NLP feature you want to use
2. **Input Your Text**: Either type directly or upload a text file
3. **Configure Options**: Adjust settings based on your needs
4. **Get Results**: View comprehensive analysis and download results

## ✅ Features 

#### Text Classification

![Text classification](https://github.com/Reaishma/Natural-language-AI/blob/main/Screenshot_20250904-162236_1.jpg)

- Automatically categorize text content
- Supports multiple categories: technology, business, sports, health, education, entertainment, news, personal
- Provides confidence scores and detailed analysis

#### Text Generation

![Text Generation](https://github.com/Reaishma/Natural-language-AI/blob/main/Screenshot_20250904-162301_1.jpg)

- **Story Generation**: Create creative stories with themes and length options
- **Email Writing**: Generate professional, casual, or formal emails
- **Blog Post Creation**: Create structured blog posts with main points
- **Text Continuation**: Extend existing text in various styles

#### Text Summarization
- **Extractive Summary**: Select key sentences from original text
- **Bullet Points**: Create concise bullet-point summaries
- **Keywords & Phrases**: Extract important terms and concepts
- Adjustable summary length (10-80% of original)

#### Sentiment Analysis

![Sentiment Analysis](https://github.com/Reaishma/Natural-language-AI/blob/main/Screenshot_20250904-162508_1.jpg)

- Overall sentiment classification (Positive/Negative/Neutral)
- Polarity and subjectivity scores
- Emotion detection (joy, sadness, anger, fear, surprise, disgust)
- Intensity analysis with confidence metrics

#### Language Translation

![Language Translation](https://github.com/Reaishma/Natural-language-AI/blob/main/Screenshot_20250904-162547_1.jpg)

- Support for 20+ languages
- Automatic language detection
- Popular languages: English, Spanish, French, German, Italian, Portuguese, Russian, Japanese, Korean, Chinese, Arabic, Hindi
- Real-time translation with confidence scores

#### Question Answering
- Context-based question answering
- Support for various question types (who, what, when, where, why, how)
- Confidence scoring and relevant context highlighting
- Keyword extraction and analysis

#### Named Entity Recognition
- Extract people, organizations, locations, dates, times, money, emails, phone numbers, URLs
- Entity relationship analysis
- Custom pattern extraction
- Batch processing capabilities



### ✅ For Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/Reaishma/Natural-language-AI.git
   cd Natural-language-AI
   ```

2. **Open with a local server**
   ```bash
   # Using Python
   python -m http.server 8000
   
   # Using Node.js
   npx serve .
   
   # Or simply open index.html in your browser
   ```

3. **Access locally**
   - Open `http://localhost:8000` in your browser

## ✅ External Dependencies

### 📍Core Libraries
- **Streamlit**: Web application framework for the frontend interface
- **TextBlob**: Primary NLP library for sentiment analysis and basic text processing
- **NLTK**: Advanced NLP processing for tokenization, stopwords, and entity recognition
- **googletrans**: Google Translate API for language translation
- **pandas**: Data manipulation and result formatting

### 📍Data Requirements
- NLTK corpora downloads (punkt tokenizer, stopwords, NE chunker, POS tagger)

- Real-time processing of user input

## Deployment Strategy

The application is designed for deployment on cloud platforms with the following characteristics:

### ✅ Recommended Platform

- Platforms: Streamlit Cloud, Heroku, or any Python-supporting cloud service
- GitHub 

## Configuration Requirements
- Python 3.7+ runtime environment
- Automatic dependency installation via requirements.txt (implied)
- Internet connectivity for Google Translate API and NLTK downloads

## 🚀 NLP Processing 

- **Text Processing APIs**: Google Cloud Natural Language, AWS Comprehend, Azure Text Analytics
- **Translation Services**: Google Translate API, Azure Translator
- **Machine Learning Models**: Hugging Face transformers, OpenAI API
- **Custom Models**: TensorFlow.js, PyTorch models

## Browser Compatibility
- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

### Integration with Real APIs
Replace mock functions in `script.js` with actual API calls:

```javascript
// Example: Real API integration
async function classifyText() {
    const text = this.getInputText('classification');
    const response = await fetch('/api/classify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
    });
    const result = await response.json();
    this.displayClassificationResults(result);
}
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Support

For support, please open an issue in the GitHub repository or contact [vra.9618@gmail.com].

## Author 
   Reaishma N 🧑‍💻
   [GitHub](https://github.com/Reaishma)


## ✅ Scalability Considerations
- Stateless design allows for easy horizontal scaling
- Module-based architecture enables selective feature deployment
- Memory-efficient processing suitable for small to medium-scale usage
- API rate limiting considerations for Google Translate integration


---
**Built with ❤️ using Streamlit | Powered by Advanced NLP Libraries** 
