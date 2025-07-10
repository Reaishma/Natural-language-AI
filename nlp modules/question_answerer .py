"""
Question Answering Module
Provides basic question answering using text search and pattern matching
"""
import streamlit as st
from textblob import TextBlob
import re
from typing import Dict, Any, List, Tuple
import pandas as pd

class QuestionAnswerer:
    def __init__(self):
        # Question type patterns
        self.question_patterns = {
            'who': [r'\bwho\b', r'\bperson\b', r'\bpeople\b', r'\bauthor\b', r'\bwriter\b'],
            'what': [r'\bwhat\b', r'\bthing\b', r'\bobject\b', r'\bitem\b'],
            'when': [r'\bwhen\b', r'\btime\b', r'\bdate\b', r'\byear\b', r'\bday\b'],
            'where': [r'\bwhere\b', r'\bplace\b', r'\blocation\b', r'\bcity\b', r'\bcountry\b'],
            'why': [r'\bwhy\b', r'\breason\b', r'\bcause\b', r'\bbecause\b'],
            'how': [r'\bhow\b', r'\bmethod\b', r'\bway\b', r'\bprocess\b']
        }
        
        # Answer extraction patterns
        self.answer_patterns = {
            'who': [
                r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # Person names
                r'\b(?:Dr|Mr|Mrs|Ms)\. [A-Z][a-z]+\b',  # Titles with names
                r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b'  # Proper nouns
            ],
            'when': [
                r'\b(?:19|20)\d{2}\b',  # Years
                r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b',  # Months
                r'\b\d{1,2}(?:st|nd|rd|th)?\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\b',  # Dates
                r'\b(?:Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b',  # Days
                r'\b\d{1,2}:\d{2}(?:\s*(?:AM|PM))?\b'  # Times
            ],
            'where': [
                r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+(?:City|State|Country|Street|Avenue|Road|Boulevard))\b',  # Places
                r'\bin\s+[A-Z][a-z]+\b',  # "in Location"
                r'\bat\s+[A-Z][a-z]+\b'   # "at Location"
            ]
        }
    
    def classify_question(self, question: str) -> str:
        """
        Classify the type of question (who, what, when, where, why, how)
        """
        question_lower = question.lower()
        
        for q_type, patterns in self.question_patterns.items():
            for pattern in patterns:
                if re.search(pattern, question_lower):
                    return q_type
        
        return 'general'
    
    def extract_keywords(self, question: str) -> List[str]:
        """
        Extract keywords from the question for context matching
        """
        blob = TextBlob(question)
        
        # Remove question words and common words
        stop_words = {'what', 'who', 'when', 'where', 'why', 'how', 'is', 'are', 'was', 'were', 'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        
        # Extract significant words
        words = [word.lower() for word in blob.words if len(word) > 2 and word.lower() not in stop_words]
        
        # Also extract noun phrases
        noun_phrases = [phrase.lower() for phrase in blob.noun_phrases if len(phrase) > 2]
        
        return list(set(words + noun_phrases))
    
    def find_relevant_sentences(self, context: str, keywords: List[str], top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Find sentences in context that are most relevant to the keywords
        """
        blob = TextBlob(context)
        sentences = [str(sentence) for sentence in blob.sentences]
        
        sentence_scores = []
        
        for sentence in sentences:
            sentence_lower = sentence.lower()
            score = 0
            
            # Score based on keyword matches
            for keyword in keywords:
                # Exact matches get higher score
                if keyword in sentence_lower:
                    score += 2
                
                # Partial matches get lower score
                for word in keyword.split():
                    if word in sentence_lower:
                        score += 1
            
            # Normalize by sentence length
            if len(sentence.split()) > 0:
                score = score / len(sentence.split())
            
            sentence_scores.append((sentence, score))
        
        # Sort by score and return top k
        sentence_scores.sort(key=lambda x: x[1], reverse=True)
        return sentence_scores[:top_k]
    
    def extract_answer_by_type(self, sentences: List[str], question_type: str) -> str:
        """
        Extract specific answer based on question type
        """
        all_text = " ".join(sentences)
        
        if question_type in self.answer_patterns:
            for pattern in self.answer_patterns[question_type]:
                matches = re.findall(pattern, all_text)
                if matches:
                    return matches[0] if isinstance(matches[0], str) else " ".join(matches[0])
        
        # Fallback: return first relevant sentence
        return sentences[0] if sentences else "No specific answer found."
    
    def answer_question(self, question: str, context: str) -> Dict[str, Any]:
        """
        Answer a question based on the provided context
        """
        try:
            if not question or not context:
                return {"error": "Both question and context are required"}
            
            if len(context.strip()) < 20:
                return {"error": "Context too short to provide meaningful answers"}
            
            # Classify question type
            question_type = self.classify_question(question)
            
            # Extract keywords from question
            keywords = self.extract_keywords(question)
            
            # Find relevant sentences
            relevant_sentences = self.find_relevant_sentences(context, keywords)
            
            if not relevant_sentences:
                return {
                    "answer": "I couldn't find relevant information in the provided context.",
                    "confidence": 0.1,
                    "question_type": question_type,
                    "keywords": keywords,
                    "context_length": len(context)
                }
            
            # Extract answer based on question type
            best_sentences = [sent for sent, score in relevant_sentences]
            
            if question_type in ['who', 'when', 'where']:
                answer = self.extract_answer_by_type(best_sentences, question_type)
            else:
                # For what, why, how questions, provide the most relevant sentence(s)
                answer = best_sentences[0]
                if len(best_sentences) > 1 and len(answer.split()) < 15:
                    answer += " " + best_sentences[1]
            
            # Calculate confidence based on keyword matches and sentence relevance
            top_score = relevant_sentences[0][1] if relevant_sentences else 0
            confidence = min(top_score * 2, 1.0)  # Scale to 0-1
            
            return {
                "answer": answer,
                "confidence": confidence,
                "question_type": question_type,
                "keywords": keywords,
                "relevant_sentences": [{"sentence": sent, "score": score} for sent, score in relevant_sentences],
                "context_length": len(context),
                "answer_length": len(answer)
            }
            
        except Exception as e:
            return {"error": f"Question answering failed: {str(e)}"}
    
    def answer_multiple_questions(self, questions: List[str], context: str) -> Dict[str, Any]:
        """
        Answer multiple questions based on the same context
        """
        try:
            results = []
            
            for i, question in enumerate(questions):
                if question and len(question.strip()) > 3:
                    answer_result = self.answer_question(question, context)
                    
                    if "error" not in answer_result:
                        results.append({
                            "question_id": i + 1,
                            "question": question,
                            "answer": answer_result["answer"],
                            "confidence": answer_result["confidence"],
                            "question_type": answer_result["question_type"]
                        })
                    else:
                        results.append({
                            "question_id": i + 1,
                            "question": question,
                            "answer": "Error: " + answer_result["error"],
                            "confidence": 0.0,
                            "question_type": "error"
                        })
            
            return {
                "qa_results": results,
                "total_questions": len(questions),
                "successful_answers": len([r for r in results if r["confidence"] > 0.3]),
                "average_confidence": sum(r["confidence"] for r in results) / len(results) if results else 0
            }
            
        except Exception as e:
            return {"error": f"Multiple question answering failed: {str(e)}"}
    
    def generate_questions(self, context: str, num_questions: int = 5) -> Dict[str, Any]:
        """
        Generate potential questions from the context
        """
        try:
            blob = TextBlob(context)
            sentences = [str(sentence) for sentence in blob.sentences]
            
            if len(sentences) < 2:
                return {"error": "Context too short to generate questions"}
            
            generated_questions = []
            
            # Extract named entities and important terms
            words = blob.words
            noun_phrases = list(blob.noun_phrases)
            
            # Generate who questions for proper nouns (names)
            proper_nouns = [word for word in words if word[0].isupper() and len(word) > 2]
            if proper_nouns:
                generated_questions.append(f"Who is {proper_nouns[0]}?")
            
            # Generate what questions for noun phrases
            if noun_phrases:
                for phrase in noun_phrases[:2]:
                    generated_questions.append(f"What is {phrase}?")
            
            # Generate when questions if years are found
            years = re.findall(r'\b(?:19|20)\d{2}\b', context)
            if years:
                generated_questions.append(f"When did this happen?")
            
            # Generate where questions if locations might be present
            location_words = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', context)
            if location_words:
                generated_questions.append(f"Where did this take place?")
            
            # Generate why/how questions based on context
            if any(word in context.lower() for word in ['because', 'reason', 'cause']):
                generated_questions.append("Why did this happen?")
            
            if any(word in context.lower() for word in ['method', 'process', 'way', 'procedure']):
                generated_questions.append("How does this work?")
            
            # Limit to requested number
            generated_questions = generated_questions[:num_questions]
            
            return {
                "generated_questions": generated_questions,
                "question_count": len(generated_questions),
                "context_analysis": {
                    "sentences": len(sentences),
                    "proper_nouns": len(set(proper_nouns)),
                    "noun_phrases": len(noun_phrases),
                    "years_found": len(years)
                }
            }
            
        except Exception as e:
            return {"error": f"Question generation failed: {str(e)}"}

# Streamlit interface for question answering
def create_question_answering_interface():
    """
    Create the Streamlit interface for question answering
    """
    st.header("❓ Question Answering")
    st.write("Ask questions about your text and get intelligent answers based on the content.")
    
    qa_system = QuestionAnswerer()
    
    # QA mode selection
    qa_mode = st.selectbox(
        "Choose QA mode:",
        ["Single Question", "Multiple Questions", "Question Generation", "Interactive QA"]
    )
    
    # Context input (common for all modes)
    st.subheader("📄 Context Document")
    
    context_method = st.radio("Choose context input method:", ["Text Input", "File Upload"])
    
    context = ""
    
    if context_method == "Text Input":
        context = st.text_area(
            "Enter context document:",
            height=200,
            placeholder="Paste your document or text here..."
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload context document:",
            type=['txt'],
            help="Upload a .txt file containing the context"
        )
        if uploaded_file:
            from utils.helpers import handle_file_upload
            context = handle_file_upload(uploaded_file)
    
    if context:
        # Show context statistics
        st.info(f"Context loaded: {len(context)} characters, {len(context.split())} words")
        
        if qa_mode == "Single Question":
            st.subheader("❓ Ask a Question")
            
            question = st.text_input(
                "Enter your question:",
                placeholder="e.g., What is the main topic? Who are the key people mentioned?"
            )
            
            if st.button("Get Answer", type="primary"):
                if question:
                    with st.spinner("Finding answer..."):
                        result = qa_system.answer_question(question, context)
                        
                        if "error" not in result:
                            # Display answer
                            st.subheader("🎯 Answer")
                            st.success(result["answer"])
                            
                            # Display confidence and metadata
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Confidence", f"{result['confidence']:.1%}")
                            with col2:
                                st.metric("Question Type", result["question_type"].title())
                            with col3:
                                st.metric("Answer Length", f"{result['answer_length']} chars")
                            
                            # Show relevant sentences
                            if result.get("relevant_sentences"):
                                st.subheader("📝 Relevant Context")
                                for i, sent_data in enumerate(result["relevant_sentences"][:3], 1):
                                    with st.expander(f"Relevant Sentence {i} (Score: {sent_data['score']:.2f})"):
                                        st.write(sent_data["sentence"])
                            
                            # Show extracted keywords
                            if result.get("keywords"):
                                st.subheader("🔑 Keywords Used")
                                st.write(", ".join(result["keywords"]))
                        
                        else:
                            from utils.helpers import display_error
                            display_error(result["error"])
                else:
                    from utils.helpers import display_error
                    display_error("Please enter a question.")
        
        elif qa_mode == "Multiple Questions":
            st.subheader("❓ Multiple Questions")
            
            num_questions = st.slider("Number of questions:", min_value=2, max_value=8, value=3)
            
            questions = []
            for i in range(num_questions):
                question = st.text_input(f"Question {i+1}:", key=f"multi_q_{i}")
                if question:
                    questions.append(question)
            
            if st.button("Answer All Questions", type="primary"):
                if questions:
                    with st.spinner(f"Answering {len(questions)} questions..."):
                        result = qa_system.answer_multiple_questions(questions, context)
                        
                        if "error" not in result:
                            # Summary
                            st.subheader("📊 QA Summary")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Total Questions", result["total_questions"])
                            with col2:
                                st.metric("Successful Answers", result["successful_answers"])
                            with col3:
                                st.metric("Average Confidence", f"{result['average_confidence']:.1%}")
                            
                            # Individual Q&A results
                            st.subheader("🎯 Questions & Answers")
                            
                            for qa_result in result["qa_results"]:
                                with st.expander(f"Q{qa_result['question_id']}: {qa_result['question'][:50]}..."):
                                    st.write(f"**Question:** {qa_result['question']}")
                                    
                                    if qa_result["confidence"] > 0.3:
                                        st.success(f"**Answer:** {qa_result['answer']}")
                                    else:
                                        st.warning(f"**Answer:** {qa_result['answer']}")
                                    
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.caption(f"Confidence: {qa_result['confidence']:.1%}")
                                    with col2:
                                        st.caption(f"Type: {qa_result['question_type']}")
                            
                            # Download Q&A results
                            qa_content = ""
                            for qa_result in result["qa_results"]:
                                qa_content += f"Q{qa_result['question_id']}: {qa_result['question']}\n"
                                qa_content += f"A{qa_result['question_id']}: {qa_result['answer']}\n"
                                qa_content += f"Confidence: {qa_result['confidence']:.1%}\n\n"
                            
                            from utils.helpers import create_download_link
                            create_download_link(
                                qa_content,
                                "qa_results.txt",
                                "📥 Download Q&A Results"
                            )
                        
                        else:
                            from utils.helpers import display_error
                            display_error(result["error"])
                else:
                    from utils.helpers import display_error
                    display_error("Please enter at least one question.")
        
        elif qa_mode == "Question Generation":
            st.subheader("🎲 Question Generation")
            st.info("Generate potential questions from your context document.")
            
            num_questions = st.slider("Number of questions to generate:", min_value=3, max_value=10, value=5)
            
            if st.button("Generate Questions", type="primary"):
                with st.spinner("Generating questions..."):
                result = qa_system.generate_questions(context, num_questions)
                    
                    if "error" not in result:
                        st.subheader("🎯 Generated Questions")
                        
                        if result["generated_questions"]:
                            for i, question in enumerate(result["generated_questions"], 1):
                                st.write(f"**{i}.** {question}")
                            
                            # Context analysis
                            st.subheader("📊 Context Analysis")
                            analysis = result["context_analysis"]
                            col1, col2, col3, col4 = st.columns(4)
                            
                            with col1:
                                st.metric("Sentences", analysis["sentences"])
                            with col2:
                                st.metric("Proper Nouns", analysis["proper_nouns"])
                            with col3:
                                st.metric("Noun Phrases", analysis["noun_phrases"])
                            with col4:
                                st.metric("Years Found", analysis["years_found"])
                            
                            # Download questions
                            questions_content = "Generated Questions:\n\n"
                            for i, question in enumerate(result["generated_questions"], 1):
                                questions_content += f"{i}. {question}\n"
                            
                            from utils.helpers import create_download_link
                            create_download_link(
                                questions_content,
                                "generated_questions.txt",
                                "📥 Download Questions"
                            )
                        else:
                            st.warning("No questions could be generated from this context.")
                    
                    else:
                        from utils.helpers import display_error
                        display_error(result["error"])
        
        elif qa_mode == "Interactive QA":
            st.subheader("💬 Interactive Q&A Session")
            st.info("Ask questions one by one and build up your understanding.")
            
            # Initialize session state for Q&A history
            if "qa_history" not in st.session_state:
                st.session_state.qa_history = []
            
            # Question input
            question = st.text_input(
                "Ask a question:",
                placeholder="Type your question here...",
                key="interactive_question"
            )
            
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button("Ask Question", type="primary"):
                    if question:
                        with st.spinner("Finding answer..."):
                            result = qa_system.answer_question(question, context)
                            
                            if "error" not in result:
                                # Add to history
                                st.session_state.qa_history.append({
                                    "question": question,
                                    "answer": result["answer"],
                                    "confidence": result["confidence"],
                                    "question_type": result["question_type"]
                                })
                                
                                             # Clear input
                                st.rerun()
                            else:
                                from utils.helpers import display_error
                                display_error(result["error"])
                    else:
                        from utils.helpers import display_error
                        display_error("Please enter a question.")
            
            with col2:
                if st.button("Clear History"):
                    st.session_state.qa_history = []
                    st.rerun()
            
            # Display Q&A history
            if st.session_state.qa_history:
                st.subheader("💬 Q&A History")
                
                for i, qa in enumerate(reversed(st.session_state.qa_history), 1):
                    with st.container():
                        st.markdown(f"**Q{len(st.session_state.qa_history) - i + 1}:** {qa['question']}")
                        
                        if qa["confidence"] > 0.5:
                            st.success(f"**A:** {qa['answer']}")
                        elif qa["confidence"] > 0.3:
                            st.info(f"**A:** {qa['answer']}")
                        else:
                            st.warning(f"**A:** {qa['answer']}")
                        
                        st.caption(f"Confidence: {qa['confidence']:.1%} | Type: {qa['question_type']}")
                        st.markdown("---")
                
                # Download session
                if len(st.session_state.qa_history) > 0:
                    session_content = "Interactive Q&A Session\n\n"
                    for i, qa in enumerate(st.session_state.qa_history, 1):
                        session_content += f"Q{i}: {qa['question']}\n"
                        session_content += f"A{i}: {qa['answer']}\n"
                        session_content += f"Confidence: {qa['confidence']:.1%}\n\n"
                    
                    from utils.helpers import create_download_link
                    create_download_link(
                        session_content,
                        "interactive_qa_session.txt",
                        "📥 Download Session"
                    )

if __name__ == "__main__":
    create_question_answering_interface()
