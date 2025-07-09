// NLP Virtual Assistant JavaScript
class NLPAssistant {
    constructor() {
        this.currentTool = 'home';
        this.initializeEventListeners();
        this.updateGenerationForm();
        this.updateCurrentDate();
        this.initializeUsageStats();
    }

    initializeEventListeners() {
        // Input method toggles
        this.setupInputMethodToggles();

        // Range slider for summary ratio
        const summaryRatio = document.getElementById('summary-ratio');
        if (summaryRatio) {
            summaryRatio.addEventListener('input', (e) => {
                document.getElementById('ratio-value').textContent = e.target.value + '%';
            });
        }

        // Generation type selector
        const generationSelect = document.getElementById('generation-select');
        if (generationSelect) {
            generationSelect.addEventListener('change', () => {
                this.updateGenerationForm();
            });
        }

        // File upload handlers
        this.setupFileUploads();
    }

    setupInputMethodToggles() {
        const inputMethods = ['classification', 'summarization', 'sentiment'];
        
        inputMethods.forEach(method => {
            const radios = document.querySelectorAll(`input[name="${method}-input"]`);
            radios.forEach(radio => {
                radio.addEventListener('change', (e) => {
                    const section = e.target.closest('.content-section');
                    const textArea = section.querySelector('.text-input-area');
                    const fileArea = section.querySelector('.file-input-area');
                    
                    if (e.target.value === 'text') {
                        textArea.style.display = 'block';
                        fileArea.style.display = 'none';
                    } else {
                        textArea.style.display = 'none';
                        fileArea.style.display = 'block';
                    }
                });
            });
        });
    }

    setupFileUploads() {
        const fileInputs = document.querySelectorAll('input[type="file"]');
        fileInputs.forEach(input => {
            input.addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    const file = e.target.files[0];
                    const reader = new FileReader();
                    reader.onload = (event) => {
                        const textAreaId = e.target.id.replace('-file', '-text');
                        const textArea = document.getElementById(textAreaId);
                        if (textArea) {
                            textArea.value = event.target.result;
                        }
                    };
                    reader.readAsText(file);
                }
            });
        });
    }

    switchTool(tool) {
        // Update select dropdown
        const select = document.getElementById('nlp-tool-select');
        if (select) {
            select.value = tool;
        }

        // Update content sections
        document.querySelectorAll('.content-section').forEach(section => {
            section.classList.remove('active');
        });
        document.getElementById(tool).classList.add('active');

        this.currentTool = tool;
    }

    updateCurrentDate() {
        const dateElement = document.getElementById('last-updated');
        if (dateElement) {
            const today = new Date().toISOString().split('T')[0];
            dateElement.textContent = today;
        }
    }

    initializeUsageStats() {
        this.usageStats = {
            'Text Classification': 0,
            'Text Generation': 0,
            'Sentiment Analysis': 0
        };
    }

    trackUsage(toolName) {
        if (this.usageStats[toolName] !== undefined) {
            this.usageStats[toolName]++;
            this.updateUsageDisplay();
        }
    }

    updateUsageDisplay() {
        const statElements = {
            'Text Classification': 'stat-classification',
            'Text Generation': 'stat-generation',
            'Sentiment Analysis': 'stat-sentiment'
        };

        for (const [tool, elementId] of Object.entries(statElements)) {
            const element = document.getElementById(elementId);
            if (element) {
                element.textContent = this.usageStats[tool];
            }
        }
    }

    showLoading() {
        document.getElementById('loading-overlay').classList.add('show');
    }

    hideLoading() {
        document.getElementById('loading-overlay').classList.remove('show');
    }

    displayResults(containerId, content) {
        const container = document.getElementById(containerId);
        container.innerHTML = content;
        container.classList.add('has-content');
    }

    updateGenerationForm() {
        const select = document.getElementById('generation-select');
        const form = document.getElementById('generation-form');
        
        if (!select || !form) return;

        const type = select.value;
        let formHTML = '';

        switch (type) {
            case 'story':
                formHTML = `
                    <div class="generation-form-group">
                        <div class="generation-form-row">
                            <div>
                                <label for="story-theme">Theme (optional):</label>
                                <input type="text" id="story-theme" placeholder="e.g., friendship, adventure, mystery">
                            </div>
                            <div>
                                <label for="story-length">Story length:</label>
                                <select id="story-length">
                                    <option value="short">Short</option>
                                    <option value="medium">Medium</option>
                                    <option value="long">Long</option>
                                </select>
                            </div>
                        </div>
                    </div>
                `;
                break;
            case 'email':
                formHTML = `
                    <div class="generation-form-group">
                        <div class="generation-form-row">
                            <div>
                                <label for="email-style">Email style:</label>
                                <select id="email-style">
                                    <option value="professional">Professional</option>
                                    <option value="casual">Casual</option>
                                    <option value="formal">Formal</option>
                                </select>
                            </div>
                            <div>
                                <label for="email-recipient">Recipient name:</label>
                                <input type="text" id="email-recipient" value="Recipient">
                            </div>
                        </div>
                        <div class="generation-form-row">
                            <div>
                                <label for="email-sender">Your name:</label>
                                <input type="text" id="email-sender" value="Your Name">
                            </div>
                            <div>
                                <label for="email-purpose">Email purpose:</label>
                                <input type="text" id="email-purpose" placeholder="e.g., schedule a meeting, follow up, thank you">
                            </div>
                        </div>
                    </div>
                `;
                break;
            case 'blog':
                formHTML = `
                    <div class="generation-form-group">
                        <label for="blog-title">Blog post title:</label>
                        <input type="text" id="blog-title" placeholder="e.g., The Future of Technology">
                        
                        <label for="blog-points">Main points (one per line):</label>
                        <textarea id="blog-points" rows="4" placeholder="Point 1&#10;Point 2&#10;Point 3"></textarea>
                    </div>
                `;
                break;
            case 'continuation':
                formHTML = `
                    <div class="generation-form-group">
                        <label for="continuation-text">Text to continue:</label>
                        <textarea id="continuation-text" rows="4" placeholder="Enter the text you want to continue..."></textarea>
                        
                        <label for="continuation-style">Continuation style:</label>
                        <select id="continuation-style">
                            <option value="creative">Creative</option>
                            <option value="informative">Informative</option>
                            <option value="conversational">Conversational</option>
                            <option value="formal">Formal</option>
                        </select>
                    </div>
                `;
                break;
        }

        form.innerHTML = formHTML;
    }

    // Text Classification
    classifyText() {
        const text = this.getInputText('classification');
        if (!text) {
            alert('Please enter some text to classify.');
            return;
        }

        this.showLoading();
        this.trackUsage('Text Classification');
        
        setTimeout(() => {
            const result = this.mockClassifyText(text);
            this.displayClassificationResults(result);
            this.hideLoading();
        }, 1500);
    }

    mockClassifyText(text) {
        const categories = ['technology', 'business', 'sports', 'health', 'education', 'entertainment', 'news', 'personal'];
        const category = categories[Math.floor(Math.random() * categories.length)];
        const confidence = 0.6 + Math.random() * 0.4;
        
        return {
            category: category,
            confidence: confidence,
            word_count: text.split(' ').length,
            text_length: text.length
        };
    }

    displayClassificationResults(result) {
        const html = `
            <h3>Classification Results</h3>
            <div class="metrics-grid">
                <div class="metric-card">
                    <span class="metric-value">${result.category.charAt(0).toUpperCase() + result.category.slice(1)}</span>
                    <div class="metric-label">Category</div>
                </div>
                <div class="metric-card">
                    <span class="metric-value">${(result.confidence * 100).toFixed(1)}%</span>
                    <div class="metric-label">Confidence</div>
                </div>
                <div class="metric-card">
                    <span class="metric-value">${result.word_count}</span>
                    <div class="metric-label">Words</div>
                </div>
                <div class="metric-card">
                    <span class="metric-value">${result.text_length}</span>
                    <div class="metric-label">Characters</div>
                </div>
            </div>
            <div class="mt-2">
                <p><strong>Category Description:</strong> Content related to ${result.category} topics and themes.</p>
            </div>
        `;
        this.displayResults('classification-results', html);
    }

    // Text Generation
    generateText() {
        const type = document.getElementById('generation-select').value;
        
        this.showLoading();
        this.trackUsage('Text Generation');
        
        setTimeout(() => {
            const result = this.mockGenerateText(type);
            this.displayGenerationResults(result);
            this.hideLoading();
        }, 2000);
    }

    mockGenerateText(type) {
        const templates = {
            story: "Once upon a time in a distant galaxy, there lived a brave scientist who embarked on an adventure to discover new technologies. This led to unexpected friendships and great success in their quest to understand the mysteries of the universe.",
            email: "Dear Recipient,\n\nI hope this email finds you well. I am writing to follow up on our previous conversation. I would like to schedule a meeting to discuss this matter further at your earliest convenience.\n\nPlease let me know your availability for next week.\n\nBest regards,\nYour Name",
            blog: "# The Future of Technology\n\nIn this comprehensive post, we'll explore the exciting future of technology and discuss why it matters in today's rapidly evolving world.\n\n## Innovation and Progress\n\nTechnology continues to advance at an unprecedented pace, bringing new opportunities and challenges. From artificial intelligence to renewable energy, innovation drives progress across all sectors.\n\n## Digital Transformation\n\nBusinesses and organizations worldwide are embracing digital transformation to stay competitive and meet evolving customer needs.\n\n## Conclusion\n\nThe future of technology holds immense promise for solving global challenges and improving quality of life worldwide.",
            continuation: "This remarkable discovery sparked a new wave of innovation that would fundamentally change how we approach problem-solving. The implications were far-reaching, influencing not only scientific research but also practical applications across multiple industries."
        };

        const text = templates[type];
        return {
            generated_text: text,
            word_count: text.split(' ').length,
            character_count: text.length,
            type: type
        };
    }

    displayGenerationResults(result) {
        const html = `
            <h3>Generated ${result.type.charAt(0).toUpperCase() + result.type.slice(1)}</h3>
            <div class="metrics-grid">
                <div class="metric-card">
                    <span class="metric-value">${result.word_count}</span>
                    <div class="metric-label">Words</div>
                </div>
                <div class="metric-card">
                    <span class="metric-value">${result.character_count}</span>
                    <div class="metric-label">Characters</div>
                </div>
            </div>
            <div class="mt-2" style="background: #f8f9fa; padding: 1.5rem; border-radius: 8px; white-space: pre-wrap;">${result.generated_text}</div>
            <button class="primary-btn mt-1" onclick="downloadText('${result.generated_text.replace(/'/g, "\\'")}', 'generated_${result.type}.txt')">
                <i class="fas fa-download"></i> Download
            </button>
        `;
        this.displayResults('generation-results', html);
    }

    // Text Summarization
    summarizeText() {
        const text = this.getInputText('summarization');
        if (!text) {
            alert('Please enter some text to summarize.');
            return;
        }

        this.showLoading();
        
        setTimeout(() => {
            const result = this.mockSummarizeText(text);
            this.displaySummarizationResults(result);
            this.hideLoading();
        }, 2000);
    }

    mockSummarizeText(text) {
        const sentences = text.split('.').filter(s => s.trim().length > 0);
        const summaryLength = Math.min(3, sentences.length);
        const summary = sentences.slice(0, summaryLength).join('. ') + '.';
        
        return {
            summary: summary,
            original_length: text.split(' ').length,
            summary_length: summary.split(' ').length,
            compression_ratio: summary.length / text.length,
            sentences_used: summaryLength,
            total_sentences: sentences.length
        };
    }

    displaySummarizationResults(result) {
        const html = `
            <h3>Summary</h3>
            <div style="background: #e8f5e8; padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem;">
                ${result.summary}
            </div>
            <div class="metrics-grid">
                <div class="metric-card">
                    <span class="metric-value">${result.original_length}</span>
                    <div class="metric-label">Original Words</div>
                </div>
                <div class="metric-card">
                    <span class="metric-value">${result.summary_length}</span>
                    <div class="metric-label">Summary Words</div>
                </div>
                <div class="metric-card">
                    <span class="metric-value">${(result.compression_ratio * 100).toFixed(1)}%</span>
                    <div class="metric-label">Compression</div>
                </div>
                <div class="metric-card">
                    <span class="metric-value">${result.sentences_used}/${result.total_sentences}</span>
                    <div class="metric-label">Sentences</div>
                </div>
            </div>
        `;
        this.displayResults('summarization-results', html);
    }

    // Sentiment Analysis
    analyzeSentiment() {
        const text = this.getInputText('sentiment');
        if (!text) {
            alert('Please enter some text to analyze.');
            return;
        }

        this.showLoading();
        this.trackUsage('Sentiment Analysis');
        
        setTimeout(() => {
            const result = this.mockAnalyzeSentiment(text);
            this.displaySentimentResults(result);
            this.hideLoading();
        }, 1500);
    }

    mockAnalyzeSentiment(text) {
        const polarity = (Math.random() - 0.5) * 2;
        const sentiment = polarity > 0.1 ? 'Positive' : polarity < -0.1 ? 'Negative' : 'Neutral';
        const confidence = Math.abs(polarity);
        
        return {
            sentiment: sentiment,
            polarity: polarity,
            confidence: confidence,
            subjectivity: Math.random(),
            word_count: text.split(' ').length,
            emotions: {
                joy: Math.random() * 0.5,
                sadness: Math.random() * 0.3,
                anger: Math.random() * 0.2,
                fear: Math.random() * 0.1
            }
        };
    }

    displaySentimentResults(result) {
        const sentimentClass = result.sentiment.toLowerCase();
        const emotionCards = Object.entries(result.emotions)
            .filter(([emotion, score]) => score > 0.1)
            .map(([emotion, score]) => `
                <div class="entity-card">
                    <div class="entity-type">${emotion.charAt(0).toUpperCase() + emotion.slice(1)}</div>
                    <div style="color: #667eea; font-weight: 600;">${(score * 100).toFixed(1)}%</div>
                </div>
            `).join('');

        const html = `
            <h3>Sentiment Analysis Results</h3>
            <div class="metrics-grid">
                <div class="metric-card">
                    <span class="metric-value sentiment-${sentimentClass}">${result.sentiment}</span>
                    <div class="metric-label">Overall Sentiment</div>
                </div>
                <div class="metric-card">
                    <span class="metric-value">${result.polarity.toFixed(3)}</span>
                    <div class="metric-label">Polarity</div>
                </div>
                <div class="metric-card">
                    <span class="metric-value">${(result.confidence * 100).toFixed(1)}%</span>
                    <div class="metric-label">Confidence</div>
                </div>
                <div class="metric-card">
                    <span class="metric-value">${(result.subjectivity * 100).toFixed(1)}%</span>
                    <div class="metric-label">Subjectivity</div>
                </div>
            </div>
            <div class="mt-2">
                <h4>Emotion Analysis</h4>
                <div class="entity-grid">
                    ${emotionCards}
                </div>
            </div>
        `;
        this.displayResults('sentiment-results', html);
    }

    // Language Translation
    translateText() {
        const text = document.getElementById('translation-text').value;
        if (!text.trim()) {
            alert('Please enter some text to translate.');
            return;
        }

        this.showLoading();
        
        setTimeout(() => {
            const result = this.mockTranslateText(text);
            this.displayTranslationResults(result);
            this.hideLoading();
        }, 1500);
    }

    mockTranslateText(text) {
        const translations = {
            'en': 'Hello, how are you today? I hope you are doing well.',
            'es': 'Hola, ¿cómo estás hoy? Espero que estés bien.',
            'fr': 'Bonjour, comment allez-vous aujourd\'hui? J\'espère que vous allez bien.',
            'de': 'Hallo, wie geht es dir heute? Ich hoffe, es geht dir gut.',
            'it': 'Ciao, come stai oggi? Spero che tu stia bene.',
            'pt': 'Olá, como você está hoje? Espero que você esteja bem.',
            'ru': 'Привет, как дела сегодня? Надеюсь, у тебя все хорошо.',
            'ja': 'こんにちは、今日はいかがですか？元気でいることを願っています。',
            'ko': '안녕하세요, 오늘 어떻게 지내세요? 잘 지내고 계시길 바랍니다.',
            'zh': '你好，你今天好吗？我希望你一切都好。'
        };
        
        const targetLang = document.getElementById('target-lang').value;
        const translated = translations[targetLang] || 'Translation would appear here';
        
        return {
            original_text: text,
            translated_text: translated,
            source_language: 'English',
            target_language: document.getElementById('target-lang').options[document.getElementById('target-lang').selectedIndex].text,
            confidence: 0.95
        };
    }

    displayTranslationResults(result) {
        const html = `
            <h3>Translation Result</h3>
            <div style="background: #e8f5e8; padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem;">
                <strong>Translated Text:</strong><br>
                ${result.translated_text}
            </div>
            <div class="metrics-grid">
                <div class="metric-card">
                    <span class="metric-value">${result.source_language}</span>
                    <div class="metric-label">From</div>
                </div>
                <div class="metric-card">
                    <span class="metric-value">${result.target_language}</span>
                    <div class="metric-label">To</div>
                </div>
                <div class="metric-card">
                    <span class="metric-value">${(result.confidence * 100).toFixed(1)}%</span>
                    <div class="metric-label">Confidence</div>
                </div>
            </div>
            <div class="mt-2" style="background: #f8f9fa; padding: 1rem; border-radius: 8px;">
                <strong>Original:</strong><br>
                ${result.original_text}
            </div>
        `;
        this.displayResults('translation-results', html);
    }

    // Question Answering
    answerQuestion() {
        const context = document.getElementById('qa-context').value;
        const question = document.getElementById('qa-question').value;
        
        if (!context.trim() || !question.trim()) {
            alert('Please provide both context and question.');
            return;
        }

        this.showLoading();
        
        setTimeout(() => {
            const result = this.mockAnswerQuestion(context, question);
            this.displayQAResults(result);
            this.hideLoading();
        }, 2000);
    }

    mockAnswerQuestion(context, question) {
        const sentences = context.split('.').filter(s => s.trim().length > 0);
        const answer = sentences[0] || 'Based on the provided context, the answer would be found here.';
        
        return {
            question: question,
            answer: answer,
            confidence: 0.75 + Math.random() * 0.2,
            question_type: question.toLowerCase().includes('what') ? 'what' : 
                          question.toLowerCase().includes('who') ? 'who' : 
                          question.toLowerCase().includes('when') ? 'when' : 'general',
            context_length: context.length
        };
    }

    displayQAResults(result) {
        const html = `
            <h3>Answer</h3>
            <div style="background: #e8f5e8; padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem;">
                <strong>Q:</strong> ${result.question}<br><br>
                <strong>A:</strong> ${result.answer}
            </div>
            <div class="metrics-grid">
                <div class="metric-card">
                    <span class="metric-value">${(result.confidence * 100).toFixed(1)}%</span>
                    <div class="metric-label">Confidence</div>
                </div>
                <div class="metric-card">
                    <span class="metric-value">${result.question_type.charAt(0).toUpperCase() + result.question_type.slice(1)}</span>
                    <div class="metric-label">Question Type</div>
                </div>
                <div class="metric-card">
                    <span class="metric-value">${result.context_length}</span>
                    <div class="metric-label">Context Length</div>
                </div>
            </div>
        `;
        this.displayResults('qa-results', html);
    }

    // Named Entity Recognition
    extractEntities() {
        const text = document.getElementById('ner-text').value;
        if (!text.trim()) {
            alert('Please enter some text to analyze.');
            return;
        }

        this.showLoading();
        
        setTimeout(() => {
            const result = this.mockExtractEntities(text);
            this.displayNERResults(result);
            this.hideLoading();
        }, 1500);
    }

    mockExtractEntities(text) {
        const entities = {
            PERSON: ['John Smith', 'Mary Johnson', 'Dr. Williams'],
            ORGANIZATION: ['Microsoft', 'Google', 'Apple Inc.'],
            LOCATION: ['New York', 'California', 'London'],
            DATE: ['2024', 'January', 'Monday'],
            MONEY: ['$100', '$1,000', '€500']
        };

        return {
            entities: entities,
            total_entities: Object.values(entities).flat().length,
            text_length: text.length
        };
    }

    displayNERResults(result) {
        const entityCards = Object.entries(result.entities)
            .filter(([type, entities]) => entities.length > 0)
            .map(([type, entities]) => `
                <div class="entity-card">
                    <div class="entity-type">${type}</div>
                    <ul class="entity-list">
                        ${entities.map(entity => `<li>${entity}</li>`).join('')}
                    </ul>
                </div>
            `).join('');

        const html = `
            <h3>Named Entities Found</h3>
            <div class="metrics-grid">
                <div class="metric-card">
                    <span class="metric-value">${result.total_entities}</span>
                    <div class="metric-label">Total Entities</div>
                </div>
                <div class="metric-card">
                    <span class="metric-value">${Object.keys(result.entities).length}</span>
                    <div class="metric-label">Entity Types</div>
                </div>
                <div class="metric-card">
                    <span class="metric-value">${result.text_length}</span>
                    <div class="metric-label">Text Length</div>
                </div>
            </div>
            <div class="mt-2">
                <h4>Extracted Entities</h4>
                <div class="entity-grid">
                    ${entityCards}
                </div>
            </div>
        `;
        this.displayResults('ner-results', html);
    }

    getInputText(type) {
        const method = document.querySelector(`input[name="${type}-input"]:checked`);
        if (method && method.value === 'text') {
            return document.getElementById(`${type}-text`).value.trim();
        } else {
            return document.getElementById(`${type}-text`).value.trim();
        }
    }
}

// Utility Functions
function downloadText(content, filename) {
    const element = document.createElement('a');
    const file = new Blob([content], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = filename;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
}

// Global Functions for onclick handlers
function classifyText() {
    nlpAssistant.classifyText();
}

function generateText() {
    nlpAssistant.generateText();
}

function summarizeText() {
    nlpAssistant.summarizeText();
}

function analyzeSentiment() {
    nlpAssistant.analyzeSentiment();
}

function translateText() {
    nlpAssistant.translateText();
}

function answerQuestion() {
    nlpAssistant.answerQuestion();
}

function extractEntities() {
    nlpAssistant.extractEntities();
}

function updateGenerationForm() {
    nlpAssistant.updateGenerationForm();
}

function switchTool(tool) {
    nlpAssistant.switchTool(tool);
}

function toggleSection(sectionId) {
    const section = document.getElementById(sectionId);
    const header = section.previousElementSibling;
    
    if (section.classList.contains('expanded')) {
        section.classList.remove('expanded');
        header.classList.remove('expanded');
    } else {
        section.classList.add('expanded');
        header.classList.add('expanded');
    }
}

function showTab(tabName) {
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.querySelectorAll('.tab-panel').forEach(panel => {
        panel.classList.remove('active');
    });
    
    event.target.classList.add('active');
    document.getElementById(tabName + '-tab').classList.add('active');
}

// Initialize the application
let nlpAssistant;
document.addEventListener('DOMContentLoaded', function() {
    nlpAssistant = new NLPAssistant();
});

// Mobile menu toggle
function toggleMobileMenu() {
    const sidebar = document.querySelector('.sidebar');
    sidebar.classList.toggle('open');
}