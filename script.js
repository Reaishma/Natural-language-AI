/**
 * Main Application Script
 * Handles UI interactions and NLP processing
 */

// Initialize NLP processor
const nlp = new NLPProcessor();

// Chat history
let chatHistory = [];

// DOM elements
const navItems = document.querySelectorAll('.nav-item');
const featureSections = document.querySelectorAll('.feature-section');

// Navigation: show feature, update active, and close mobile menu on nav item click
navItems.forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        const feature = item.dataset.feature;
        showFeature(feature);

        // Update active nav item
        navItems.forEach(nav => nav.classList.remove('active'));
        item.classList.add('active');

        // Close the mobile menu on nav click (for mobile view)
        closeMobileMenu();
    });
});

function showFeature(feature) {
    featureSections.forEach(section => {
        section.classList.remove('active');
        if (section.id === feature) {
            section.classList.add('active');
        }
    });
}

// Chatbot Functions
function sendMessage() {
    const input = document.getElementById('chatInput');
    const message = input.value.trim();

    if (message === '') return;

    // Add user message
    addChatMessage(message, 'user');

    // Generate bot response
    const result = nlp.generateChatResponse(message);
    addChatMessage(result.response, 'bot', result.analysis);

    // Clear input
    input.value = '';

    // Store in history
    chatHistory.push({ user: message, bot: result.response, analysis: result.analysis });
}

function addChatMessage(message, sender, analysis = null) {
    const messagesContainer = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.textContent = message;

    messageDiv.appendChild(messageContent);
    messagesContainer.appendChild(messageDiv);

    // Add analysis for bot messages
    if (sender === 'bot' && analysis) {
        const analysisDiv = document.createElement('div');
        analysisDiv.className = 'analysis-info';
        analysisDiv.innerHTML = `
            <small><strong>Analysis:</strong> Sentiment: ${analysis.sentiment} | 
            Entities: ${analysis.entities.length}</small>
        `;
        messageDiv.appendChild(analysisDiv);
    }

    // Scroll to bottom
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

function clearChat() {
    const messagesContainer = document.getElementById('chatMessages');
    messagesContainer.innerHTML = `
        <div class="message bot-message">
            <div class="message-content">
                Hello! I'm an AI assistant with NLP capabilities. How can I help you today?
            </div>
        </div>
    `;
    chatHistory = [];
}

// Chat input enter key
document.getElementById('chatInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Sentiment Analysis
function analyzeSentiment() {
    const text = document.getElementById('sentimentText').value.trim();
    const resultsDiv = document.getElementById('sentimentResults');

    if (!text) {
        showError(resultsDiv, 'Please enter some text to analyze.');
        return;
    }

    const result = nlp.analyzeSentiment(text);

    resultsDiv.innerHTML = `
        <div class="result-card">
            <div class="result-title">📊 Sentiment Analysis Results</div>
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-value sentiment-${result.label.toLowerCase()}">${result.label}</div>
                    <div class="metric-label">Overall Sentiment</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${result.polarity.toFixed(3)}</div>
                    <div class="metric-label">Polarity Score</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${result.subjectivity.toFixed(3)}</div>
                    <div class="metric-label">Subjectivity</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${result.positiveWords}</div>
                    <div class="metric-label">Positive Words</div>
                </div>
            </div>
        </div>
    `;

    // Create sentiment gauge
    createSentimentGauge(result.polarity);

    resultsDiv.classList.add('show');
}

function createSentimentGauge(polarity) {
    const data = [{
        type: "indicator",
        mode: "gauge+number",
        value: polarity,
        title: { text: "Sentiment Score" },
        gauge: {
            axis: { range: [-1, 1] },
            bar: { color: "darkblue" },
            steps: [
                { range: [-1, -0.5], color: "lightcoral" },
                { range: [-0.5, 0], color: "lightyellow" },
                { range: [0, 0.5], color: "lightgreen" },
                { range: [0.5, 1], color: "darkgreen" }
            ]
        }
    }];

    const layout = { width: 400, height: 300, margin: { t: 0, b: 0 } };

    const gaugeDiv = document.createElement('div');
    gaugeDiv.className = 'chart-container';
    gaugeDiv.id = 'sentimentGauge';

    document.getElementById('sentimentResults').appendChild(gaugeDiv);

    Plotly.newPlot('sentimentGauge', data, layout);
}

// Named Entity Recognition
function extractEntities() {
    const text = document.getElementById('nerText').value.trim();
    const resultsDiv = document.getElementById('nerResults');

    if (!text) {
        showError(resultsDiv, 'Please enter some text to analyze.');
        return;
    }

    const entities = nlp.extractEntities(text);

    if (entities.length === 0) {
        resultsDiv.innerHTML = `
            <div class="warning-message">
                No entities detected in the provided text.
            </div>
        `;
    } else {
        const entityList = entities.map(entity => `
            <div class="entity-item">
                <span class="entity-highlight entity-${entity.label.toLowerCase()}">
                    ${entity.text}
                </span>
                <span class="entity-type">(${entity.label})</span>
                <span class="entity-desc">${entity.description}</span>
            </div>
        `).join('');

        resultsDiv.innerHTML = `
            <div class="result-card">
                <div class="result-title">🎯 Detected Entities</div>
                <div class="entity-list">
                    ${entityList}
                </div>
            </div>
            <div class="result-card">
                <div class="result-title">📝 Highlighted Text</div>
                <div class="highlighted-text">
                    ${highlightEntities(text, entities)}
                </div>
            </div>
        `;

        // Create entity distribution chart
        createEntityChart(entities);
    }

    resultsDiv.classList.add('show');
}

function highlightEntities(text, entities) {
    let highlightedText = text;

    // Sort entities by last occurrence position (reverse order for safe replacement)
    entities.sort((a, b) => text.lastIndexOf(b.text) - text.lastIndexOf(a.text));

    entities.forEach(entity => {
        const regex = new RegExp(`\\b${entity.text.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}\\b`, 'gi');
        highlightedText = highlightedText.replace(regex,
            `<span class="entity-highlight entity-${entity.label.toLowerCase()}" title="${entity.description}">${entity.text}</span>`
        );
    });

    return highlightedText;
}

function createEntityChart(entities) {
    const entityCounts = {};
    entities.forEach(entity => {
        entityCounts[entity.label] = (entityCounts[entity.label] || 0) + 1;
    });

    const data = [{
        type: 'pie',
        labels: Object.keys(entityCounts),
        values: Object.values(entityCounts),
        hole: 0.3
    }];

    const layout = {
        title: 'Entity Types Distribution',
        height: 400
    };

    const chartDiv = document.createElement('div');
    chartDiv.className = 'chart-container';
    chartDiv.id = 'entityChart';

    document.getElementById('nerResults').appendChild(chartDiv);

    Plotly.newPlot('entityChart', data, layout);
}

// Text Generation
function generateText() {
    const prompt = document.getElementById('generationPrompt').value.trim();
    const maxLength = parseInt(document.getElementById('maxLength').value);
    const resultsDiv = document.getElementById('generationResults');

    if (!prompt) {
        showError(resultsDiv, 'Please provide a prompt for text generation.');
        return;
    }

    const generatedText = nlp.generateText(prompt, maxLength);

    // Analyze generated text
    const sentiment = nlp.analyzeSentiment(generatedText);
    const entities = nlp.extractEntities(generatedText);

    resultsDiv.innerHTML = `
        <div class="result-card">
            <div class="result-title">📖 Generated Text</div>
            <div class="result-content">
                ${generatedText}
            </div>
        </div>
        <div class="result-card">
            <div class="result-title">🔍 Generated Text Analysis</div>
            <div class="metric-grid">
                <div class="metric-card">
                    <div class="metric-value sentiment-${sentiment.label.toLowerCase()}">${sentiment.label}</div>
                    <div class="metric-label">Sentiment</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${generatedText.split(' ').length}</div>
                    <div class="metric-label">Word Count</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">${entities.length}</div>
                    <div class="metric-label">Entities Found</div>
                </div>
            </div>
            ${entities.length > 0 ? `
                <div class="entity-preview">
                    <strong>Key Entities:</strong>
                    ${entities.slice(0, 3).map(e => `<span class="entity-highlight entity-${e.label.toLowerCase()}">${e.text}</span>`).join(', ')}
                </div>
            ` : ''}
        </div>
    `;

    resultsDiv.classList.add('show');
}

// Update range input displays
document.getElementById('maxLength').addEventListener('input', (e) => {
    document.getElementById('maxLengthValue').textContent = e.target.value;
});

document.getElementById('creativity').addEventListener('input', (e) => {
    document.getElementById('creativityValue').textContent = e.target.value;
});

// Question Answering
function answerQuestion() {
    const context = document.getElementById('qaContext').value.trim();
    const question = document.getElementById('qaQuestion').value.trim();
    const resultsDiv = document.getElementById('qaResults');

    if (!context || !question) {
        showError(resultsDiv, 'Please provide both context and a question.');
        return;
    }

    const result = nlp.answerQuestion(question, context);

    resultsDiv.innerHTML = `
        <div class="result-card">
            <div class="result-title">💡 Answer</div>
            <div class="result-content">
                <div class="answer-text">${result.answer}</div>
                <div class="confidence-score">
                    <strong>Confidence:</strong> ${(result.confidence * 100).toFixed(1)}%
                </div>
            </div>
        </div>
        ${result.context ? `
            <div class="result-card">
                <div class="result-title">📝 Relevant Context</div>
                <div class="result-content">
                    ${result.context}
                </div>
            </div>
        ` : ''}
    `;

    resultsDiv.classList.add('show');
}

// Utility Functions
function showError(container, message) {
    container.innerHTML = `
        <div class="error-message">
            ${message}
        </div>
    `;
    container.classList.add('show');
}

function showSuccess(container, message) {
    container.innerHTML = `
        <div class="success-message">
            ${message}
        </div>
    `;
    container.classList.add('show');
}

// Mobile Menu Functions
function toggleMobileMenu() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.querySelector('.sidebar-overlay');

    sidebar.classList.toggle('mobile-open');
    overlay.classList.toggle('show');
}

function closeMobileMenu() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.querySelector('.sidebar-overlay');

    sidebar.classList.remove('mobile-open');
    overlay.classList.remove('show');
}

// Note: The navigation event listener is combined and already included above.
// So remove any duplicate listeners that only close mobile menu on nav click.

// Initialize the application
document.addEventListener('DOMContentLoaded', () => {
    console.log('NLP Platform initialized successfully!');

    // Show home section by default
    showFeature('home');
});
